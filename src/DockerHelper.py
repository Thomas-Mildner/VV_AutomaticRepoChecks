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
                    return DockerHelper.contains_latest_and_date(tag_names), tag_names
            else:
                return False, None
        except gitlab.exceptions.GitlabGetError as e:
            logger.warning(f"Error fetching registry information: {e}")
            return False, None

    @staticmethod
    def run_local_docker_image(logger, docker_client, dockerfile_path, image_name,container_name, detach=True):
        """
        Runs a Docker image as a container.

        Args:
            image_tag (str): The tag of the Docker image to run.
            container_name (str): The name to assign to the running container. Defaults to 'my-container'.
            detach (bool): Whether to run the container in detached mode. Defaults to True.
        """
        try:
            print(f"Building Docker image: {image_name}")
            image, build_logs = docker_client.images.build(path=dockerfile_path, tag=image_name)
            print(build_logs)
            container = docker_client.containers.run(image=image_name, name=container_name, detach=detach)
            print(f"Container {container_name} is running.")

        except docker.errors.BuildError as build_err:
            print(f"Error building Docker image: {build_err}")
        except docker.errors.APIError as api_err:
            print(f"Error running Docker container: {api_err}")
