import json
import os
from datetime import datetime
import time
import socket

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
    def run_docker_image_from_container_registry(logger, docker_client, image_location, container_name, env_vars,
                                                 detach=True):
        container_logs = []
        try:

            logger.info(f"Pulling Docker image: {image_location}")
            image = docker_client.images.pull(image_location)
            logger.info(f"Successfully pulled Docker image: {image.tags}")

            container = docker_client.containers.run(image=image_location, name=container_name, environment=env_vars,
                                                     detach=detach, ports={'9000/tcp': ('127.0.0.1', 9000)})
            logger.info(f"Container {container_name} is running.")

            # If not detached, wait for the container to finish
            if not detach:
                container.wait()

            json_data = '''
{
  "order_number": "ORD12345",
  "datetime": "2024-05-17T15:45:00",
  "customer": {
    "name": "Max Mustermann",
    "email": "max.mustermann@example.com",
    "address": {
      "country": "Germany",
      "street": "Sample Street 123",
      "city": "Example City",
      "zip_code": "12345"
    }
  },
  "products": [
    {
      "product_id": "PROD00100",
      "name": "Beer",
      "quantity": 2,
      "price": 2.5
    },
    {
      "product_id": "PROD002",
      "name": "Wine",
      "quantity": 2,
      "price": 15
    },
    {
      "product_id": "PROD003",
      "name": "Water",
      "quantity": 6,
      "price": 1
    }
  ],
  "total_price": 41,
  "payment_method": "Credit Card"
}
'''
            DockerHelper.send_json_over_tcp(logger=logger, host='localhost', port=9000, json_data=json_data)

            # Add a delay to allow the container to execute necessary operations
            time.sleep(5)

            # Execute a shell command within the container to search for the file recursively
            exec_result = container.exec_run(['find', '/', '-name', '*.json'])
            if exec_result.exit_code == 0:
                # Split the output into lines and iterate over each line
                for line in exec_result.output.decode('utf-8').split('\n'):
                    # Check if the line contains the JSON file
                    if line.endswith('.json'):
                        logger.info(f"JSON file found: {line}")
            else:
                logger.info("No JSON files found in the container.")

            # Fetch and log the container logs
            logs = container.logs()
            decoded_logs = logs.decode('utf-8')
            for log in decoded_logs.splitlines():
                container_logs.append(log)
                logger.info(log)

            container.stop()
            container.remove()

            return container_logs

        except docker.errors.BuildError as build_err:
            logger.error(f"Error building Docker image: {build_err}")
        except docker.errors.APIError as api_err:
            logger.error(f"Error running Docker container: {api_err}")
