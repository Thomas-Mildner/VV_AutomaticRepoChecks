import json
import os
from datetime import datetime
import time
import socket

import docker
import gitlab
import importlib.resources as pkg_resources

from models.ResultReport import ResultReport


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
        login_command = f'docker login {registry_url} -u {username} -p {access_token} >/dev/null 2>&1'
        response = os.system(login_command)
        if response != 0:
            raise Exception("Docker login failed")

    @staticmethod
    def send_json_over_tcp(logger, host, port, json_data):
        logger.info("Sending Json Data via TCP Socket...")
        try:
            # Create a socket object
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Connect to the server
                s.connect((host, port))

                # Serialize the JSON data
                json_str = json.dumps(json_data)

                # Send the serialized JSON data over the socket
                s.sendall(json_str.encode())

                logger.info("JSON data sent successfully.")

        except Exception as e:
            logger.error(f"Error sending JSON data: {e}")

    @staticmethod
    def read_json_from_folder(logger, package, filename):
        """
        Reads a JSON file from a specified folder.

        Args:
            logger (logger): Instance of logger
            package (str): The package where the resource is located.
            filename (str): Filename which should be read from resources

        Returns:
            dict: The contents of the JSON file as a dictionary.
        """
        try:
            # Open the resource file within the package
            with pkg_resources.open_text(package, filename) as file:
                data = json.load(file)
            return data

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None

    @staticmethod
    def send_json_file_to_docker_container_and_check_result(logger, filename, host_name, port, container, json_path_containing_keywords):
        json_data = DockerHelper.read_json_from_folder(logger=logger, package='resources', filename=filename)
        DockerHelper.send_json_over_tcp(logger=logger, host=host_name, port=port, json_data=json_data)

        # Add a delay to allow the container to execute necessary operations
        logger.info('Sleeping for 2 Seconds to allow container to execute necessary operations...')
        time.sleep(2)
        logger.info('Continue checking for written Json File')

        test_successful: bool = False

        # Execute a shell command within the container to search for the file recursively
        exec_result = container.exec_run(['find', '/', '-name', '*.json'])
        if exec_result.exit_code == 0:
            # Split the output into lines and iterate over each line
            for line in exec_result.output.decode('utf-8').split('\n'):
                # Check if the line contains the JSON file
                if line.endswith('.json'):
                    logger.info(f"JSON file found: {line}")
                    if all(keyword in line for keyword in json_path_containing_keywords):
                        logger.info(f"JSON file matching all keywords found: {line}")
                        test_successful = True
        else:
            logger.info("No JSON files found in the container.")

        return test_successful

    @staticmethod
    def run_docker_image_from_container_registry(logger, docker_client, image_location, container_name, container_port, env_vars, result_report: ResultReport,
                                                 detach=True):
        container_logs = []
        try:

            logger.info(f"Pulling Docker image: {image_location}")
            image = docker_client.images.pull(image_location)
            logger.info(f"Successfully pulled Docker image: {image.tags}")

            container = docker_client.containers.run(image=image_location, name=container_name, environment=env_vars,
                                                     detach=detach, ports={f'{container_port}/tcp': ('host.docker.internal', container_port)})
            logger.info(f"Container {container_name} is running.")

            # Check if the container is running
            container.reload()  # Refresh the container's attributes
            if container.status == 'running':
                result_report.container_started_successfully = True
                logger.info(f"Container {container_name} is confirmed running.")
            else:
                result_report.container_started_successfully = False
                logger.warning(f"Container {container_name} failed to start. Status: {container.status}")

            # If not detached, wait for the container to finish
            if not detach:
                container.wait()

            logger.info('Sleeping for 2 Seconds to startup Container...')
            time.sleep(2)
            logger.info('Continue working with Container')

            good_order_test_successful = DockerHelper.send_json_file_to_docker_container_and_check_result(logger=logger, filename='Exercise01_GoodOrder.json', host_name='host.docker.internal', port=container_port, container=container, json_path_containing_keywords=['Mustermann', 'success'])
            bad_order_test_successful = DockerHelper.send_json_file_to_docker_container_and_check_result(logger=logger, filename='Exercise01_BadOrder.json', host_name='host.docker.internal', port=container_port, container=container, json_path_containing_keywords=['failed'])

            result_report.container_test_exercise01_good_order_successful = good_order_test_successful
            result_report.container_test_exercise01_bad_order_successful = bad_order_test_successful

            logger.info(f'Good Order Json Test Result: {good_order_test_successful}')
            logger.info(f'Bad Order Json Test Result: {bad_order_test_successful}')

            # Fetch and log the container logs
            logs = container.logs()
            decoded_logs = logs.decode('utf-8')
            for log in decoded_logs.splitlines():
                container_logs.append(log)

            logger.info('Stopping Container and Remove it')
            container.stop()
            container.remove()

            return container_logs

        except docker.errors.BuildError as build_err:
            logger.error(f"Error building Docker image: {build_err}")
        except docker.errors.APIError as api_err:
            logger.error(f"Error running Docker container: {api_err}")
