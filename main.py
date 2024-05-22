import os
import subprocess
import git
import docker
import shutil
import gitlab
import logging
import datetime

from git import Repo

from models.ResultReport import ResultReport

# Personal Configuration
GITLAB_PRIVATE_TOKEN = 'xeyi4xobsH31FC833m-M'  # Replace with your GitLab private token

# Configuration
current_year = datetime.datetime.now().year % 100  #only last two digits
GITLAB_URL = 'https://inf-git.fh-rosenheim.de/'
GITLAB_GROUP_ID = f'vv-inf-sose{current_year}'
DOCKER_IMAGE_PREFIX = 'your-docker-registry/your-image-prefix'
LOCAL_REPO_DIR = f'sose{current_year}repositories'
LOCAL_RESULT_DIR = f'sose{current_year}results'

# Exercise Settings
REQUIRED_REPO_FILES = ['.GITIGNORE', 'ANALYSE.MD', '.GITLAB-CI.YML', 'README.MD', 'DOCKERFILE', 'BUILD.GRADLE', 'DOCKER-COMPOSE.YML']
ANALYSE_FILE_NAME = "Analyse.md"


# Initialize GitLab and Docker clients
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_PRIVATE_TOKEN)
#client = docker.from_env()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_repositories():
    try:
        logger.info(f'Starting to Crawl Repos for GroupId: {GITLAB_GROUP_ID}')
        group = gl.groups.get(GITLAB_GROUP_ID)
        projects = group.projects.list(all=True)
        repo_info = [{'path_with_namespace': project.path_with_namespace, 'id': project.id} for project in projects]
        logger.info(f"Found {len(repo_info)} repositories in the group.")
        return repo_info
    except Exception as e:
        logger.error(f"Error fetching repositories: {e}")
        return []


def clone_or_update_repositories(repo_names):
    """Clones or updates repositories based on their existence.

    Args:
      repo_names: A list of repository names.
    """

    os.makedirs(LOCAL_REPO_DIR, exist_ok=True)
    for repo in repo_names:
        repo_name = repo['path_with_namespace']
        repo_url = f"{GITLAB_URL}/{repo_name}.git"
        local_path = os.path.join(LOCAL_REPO_DIR, repo_name.replace('/', '_'))

        if os.path.exists(local_path):
            # Check if it's a Git repository
            if os.path.isdir(os.path.join(local_path, '.git')):
                logger.info(f"Updating existing repository {repo_name}")
                try:
                    # Open the existing repository
                    repo = Repo(local_path)
                    # Perform a pull to fetch and merge changes
                    repo.git.pull()
                    logger.info(f"Successfully updated repository {repo_name}")
                except Exception as e:
                    logger.error(f"Error updating repository {repo_name}: {e}")
            else:
                # Not a Git repository, remove the directory and clone
                logger.warning(f"Directory {local_path} exists but is not a Git repository. Removing and cloning.")
                shutil.rmtree(local_path)
                try:
                    logger.info(f"Cloning {repo_url} into {local_path}")
                    git.Repo.clone_from(repo_url, local_path)
                except Exception as e:
                    logger.error(f"Error cloning repository {repo_url}: {e}")
        else:
            # Repository doesn't exist, clone it
            logger.info(f"Cloning {repo_url} into {local_path}")
            try:
                git.Repo.clone_from(repo_url, local_path)
            except Exception as e:
                logger.error(f"Error cloning repository {repo_url}: {e}")


def check_if_there_are_all_required_files_existing(repo_path):
    """
    Checks if all required files exist in the given repository path (excluding .git and .idea directories).

    Args:
        repo_path (str): The path to the repository directory.

    Returns:
        list: A list of missing files (empty list if all files are found).
    """
    existing_files = set()
    missing_files = []

    # Use os.walk for recursive search
    for root, dirs, files in os.walk(repo_path):
        # Skip .git and .idea directories
        dirs[:] = [d for d in dirs if d not in {'.git', '.idea', 'gradle'}]

        for filename in files:
            # Normalize filename to uppercase for case-insensitive comparison
            normalized_filename = filename.upper()
            if normalized_filename in (name.upper() for name in REQUIRED_REPO_FILES):
                # Combine path with filename and add to existing files set
                filepath = os.path.relpath(os.path.join(root, filename), repo_path)
                existing_files.add(filepath.upper())

    # Check for missing files
    for required_file in REQUIRED_REPO_FILES:
        if required_file not in existing_files:
            missing_files.append(required_file)
            logger.warning(f"Required file {required_file} not found in repository path {repo_path}.")

    return missing_files


def check_if_analyse_md_seems_valid(repo_path, filename):
    """
     Searches a directory recursively for "analyse.md" file, opens it, counts characters, and closes it.

     Args:
         repo_path (str): The path to the directory to start searching.
         filename (str): the name of the file

     Returns:
         int: The number of characters in the file (or 0 if not found).
     """

    for root, _, files in os.walk(repo_path):
        for folder_file_name in files:
            if folder_file_name == filename:
                filepath = os.path.join(root, folder_file_name)
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Count characters (excluding newline characters)
                    character_count = len(content.replace('\n', ''))
                    return character_count
    else:
        logger.warning(f"File 'analyse.md' not found in directory or its subdirectories: {repo_path}")
        return 0


def generate_report_foreach_repo(report: ResultReport):
    logger.info(f'Generating ResultReport in Folder {LOCAL_RESULT_DIR}')
    markdown = report.generate_markdown()
    os.makedirs(LOCAL_RESULT_DIR, exist_ok=True)
    repo_name = report.repo_name.replace(f'{GITLAB_GROUP_ID}/', '')
    filename = f'{repo_name}_Result.md'
    filepath = os.path.join(LOCAL_RESULT_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(markdown)
        logger.info(f"Result Report file saved: {filepath}")


def check_pipeline_status(project_id, pipeline_id):
    """
    Checks if a GitLab pipeline is running successfully.

    Args:
        project_id (int): The ID of the GitLab project.
        pipeline_id (int): The ID of the pipeline to check.
        private_token (str): Personal access token for GitLab.

    Returns:
        str: The status of the pipeline.
    """

    # Get the project
    project = gl.projects.get(project_id)

    # Get the pipeline
    pipeline = project.pipelines.get(pipeline_id)

    return pipeline.status

def run_docker_tests(repo_name, repo_path):
    docker_image = f"{DOCKER_IMAGE_PREFIX}/{repo_name.replace('/', '_')}:latest"
    try:
        logger.info(f"Pulling Docker image {docker_image}")
        #  client.images.pull(docker_image)

        logger.info(f"Running Docker container for {repo_name}")
        # container = client.containers.run(
        #     docker_image,
        #     command=DOCKER_TEST_COMMAND,
        #     volumes={repo_path: {'bind': '/repo', 'mode': 'rw'}},
        #     working_dir='/repo',
        #     detach=True
        # )

    # logs = container.logs(stream=True)
    #   for log in logs:
    #       logger.info(log.strip())

    #   container.wait()
    #    logger.info(f"Tests completed for {repo_name}")
    #   container.remove()
    except Exception as e:
        logger.error(f"Error running Docker tests for {repo_name}: {e}")


def main():
    repo_infos = get_repositories()
    repo_infos = repo_infos[:5]  # remove me
    if repo_infos:
        clone_or_update_repositories(repo_infos)
        for repo in repo_infos:
            repo_name = repo['path_with_namespace']
            repo_project_id = repo['id']
            repo_path = os.path.join(LOCAL_REPO_DIR, repo_name.replace('/', '_'))
            result_report = ResultReport(repo_name=repo_name,is_successful_crawled=True)
            result_report.missing_files = check_if_there_are_all_required_files_existing(repo_path)
            result_report.analyse_markdown_character_count = check_if_analyse_md_seems_valid(repo_path, ANALYSE_FILE_NAME)
            result_report.pipeline_running_successful = check_pipeline_status(repo_project_id, 'FIX ME')
            logger.info(f'Found {len(result_report.missing_files)} Missing Files')

            generate_report_foreach_repo(result_report)
    else:
        logger.error("No repositories to process")


if __name__ == "__main__":
    main()
