import os
from datetime import datetime

import docker
import gitlab


class DockerHelper:

    @staticmethod
    def contains_latest_and_date(strings):
        has_latest = 'latest' in strings
        has_valid_date = any(DockerHelper.is_valid_date(s) for s in strings)
        return has_latest and has_valid_date

    @staticmethod
    def is_valid_date(date_string):
        try:
            datetime.strptime(date_string, '%Y%m%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def check_if_docker_image_tags_exists_in_registry(logger, project):
        try:
            repositories = project.repositories.list()
            if repositories:
                for repo in repositories:
                    tags = repo.tags.list()
                    tag_names = [s.name for s in tags]

                    latest_image_tag = next((tag for tag in tags if 'latest' in tag.name), None)
                    latest_image_tag_location = ''
                    if latest_image_tag:
                        latest_image_tag_location = latest_image_tag.attributes['location']
                    return DockerHelper.contains_latest_and_date(tag_names), tag_names, latest_image_tag_location
            else:
                return False, None, None
        except gitlab.exceptions.GitlabGetError as e:
            logger.warning(f"Error fetching registry information: {e}")
            return False, None

    @staticmethod
    def authenticate_docker_with_gitlab(registry_url, username, access_token):
        login_command = f'docker login {registry_url} -u {username} -p {access_token}'
        response = os.system(login_command)
        if response != 0:
            raise Exception("Docker login failed")

    @staticmethod
    def run_docker_image_from_container_registry(logger, docker_client, image_location, container_name, env_vars,
                                                 detach=True):
        container_logs = []
        try:

            logger.info(f"Pulling Docker image: {image_location}")
            image = docker_client.images.pull(image_location)
            logger.info(f"Successfully pulled Docker image: {image.tags}")

            container = docker_client.containers.run(image=image_location, name=container_name, environment=env_vars,
                                                     detach=detach)
            logger.info(f"Container {container_name} is running.")

            # If not detached, wait for the container to finish
            if not detach:
                container.wait()

            # Fetch and log the container logs
            logs = container.logs(stream=True)
            for log in logs:
                decoded_log = log.decode('utf-8')
                container_logs.append(decoded_log)
                logger.info(decoded_log)

            container.stop()
            container.remove()

            return container_logs

        except docker.errors.BuildError as build_err:
            logger.error(f"Error building Docker image: {build_err}")
        except docker.errors.APIError as api_err:
            logger.error(f"Error running Docker container: {api_err}")
