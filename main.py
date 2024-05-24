import csv
import os
import subprocess
import warnings

import git
import docker
import shutil
import gitlab
import logging
import datetime

from git import Repo

from models.ResultReport import ResultReport
from src.BuildPipelineHelper import BuildPipelineHelper
from src.DockerHelper import DockerHelper
from src.GitHelper import GitHelper

# Personal Configuration
GITLAB_USER_NAME = os.getenv('GITLAB_USER_NAME')
GITLAB_PRIVATE_TOKEN = os.getenv('GITLAB_PRIVATE_TOKEN')

# Configuration

current_year = datetime.datetime.now().year % 100  #only last two digits
GITLAB_URL = 'https://inf-git.fh-rosenheim.de/'
GITLAB_GROUP_ID = f'vv-inf-sose{current_year}'

CLONING_REPOS_LOCALLY = False
LOCAL_REPO_DIR = f'sose{current_year}repositories'
LOCAL_RESULT_DIR = f'/app/results/sose{current_year}results'
CSV_FILENAME = 'all_reports.csv'

EXERCISE = os.getenv('EXERCISE')

# Exercise Settings
REQUIRED_REPO_FILES = ['.GITIGNORE', f'{EXERCISE.upper()}/DOC/ANALYSE.MD', f'{EXERCISE.upper()}/.GITLAB-CI.YML',
                       'README.MD',
                       f'{EXERCISE.upper()}/DOCKERFILE', f'{EXERCISE.upper()}/BUILD.GRADLE',
                       f'{EXERCISE.upper()}/DOCKER-COMPOSE.YML']
GITLAB_CI_PATH = f'{EXERCISE}/.gitlab-ci.yml'
DOCKERFILE_PATH = f'{EXERCISE}/Dockerfile'
GITLAB_CI_REQUIRED_KEYWORDS = ['build', 'docker', 'push', 'test', 'sonarqube ']
ANALYSE_FILE_NAME = "Analyse.md"

# Initialize GitLab and Docker clients
gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_PRIVATE_TOKEN)
docker_client = docker.DockerClient(base_url='tcp://host.docker.internal:2375')  # access docker from host machine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress warnings in output log
warnings.filterwarnings(action="ignore")


def list_project_files_recursive(project, branch='main', path=''):
    """
    Recursively lists files in a GitLab project repository.

    Args:
        project (project): The Gitlab Project
        branch (str): The branch to list files from. Defaults to 'main'.
        path (str): The path to list files from. Defaults to the root directory.

    Returns:
        list: A list of file paths in the repository.

    """

    try:
        # List files in the repository tree
        items = project.repository_tree(ref=branch, path=path)
        file_paths = []
        for item in items:
            if item['type'] == 'blob':  # 'blob' indicates a file
                file_paths.append(item['path'])
            elif item['type'] == 'tree':  # 'tree' indicates a directory
                # Recursively list files in subdirectory
                subdirectory_files = list_project_files_recursive(project, branch, item['path'])
                file_paths.extend(subdirectory_files)
        return file_paths
    except gitlab.exceptions.GitlabGetError as e:
        logger.warning(f"Error retrieving repository tree: {e}")
        return []


def check_if_there_are_all_required_files_existing(repo_files, folder_to_be_searched):
    """
    Checks if all required files exist in the given repository path (excluding .git and .idea directories).

    Args:
        repo_path (str): The path to the repository directory.

    Returns:
        list: A list of missing files (empty list if all files are found).
    """
    try:

        missing_files = []

        # Check if all required files exist
        for required_file in REQUIRED_REPO_FILES:
            if required_file.upper() not in [file.upper() for file in repo_files]:
                logger.warning(f"Required file '{required_file}' not found in the repository.")
                missing_files.append(required_file)

        return missing_files
    except gitlab.exceptions.GitlabGetError as e:
        logger.warning(f"Error retrieving repository tree: {e}")
        return REQUIRED_REPO_FILES


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
    logger.info("=== Writing Results ===")
    logger.info(f'Generating ResultReport in Folder {LOCAL_RESULT_DIR}')
    markdown = report.generate_markdown()
    os.makedirs(LOCAL_RESULT_DIR, exist_ok=True)
    repo_name = report.repo_name.replace(f'{GITLAB_GROUP_ID}/', '')
    filename = f'{repo_name}_Result.md'
    filepath = os.path.join(LOCAL_RESULT_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(markdown)
        logger.info(f"Result Report file saved: {filepath}")


def generate_csv_for_all_reports(reports):
    csv_filepath = os.path.join(LOCAL_RESULT_DIR, CSV_FILENAME)
    with open(csv_filepath, 'w', newline='') as csvfile:
        fieldnames = [
            'repo_name', 'is_successfulCrawled', 'repo_has_multiple_branches', 'branch_names', 'missing_files',
            'analyse_markdown_character_count', 'counted_commits', 'git_repo_last_updated_at', 'pipeline_running_successful',
            'pipeline_job_details', 'missing_keywords_in_pipeline', 'container_image_tag_names', 'container_registry_contains_all_necessary_tags',
            'container_started_successfully', 'container_logs', 'container_test_exercise01_good_order_successful',
            'container_test_exercise01_bad_order_successful', 'error_message'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for report in reports:
            writer.writerow(report.to_csv_row())

    logger.info(f"CSV file for all reports saved: {csv_filepath}")


def main():
    #repo_infos = GitHelper.get_repositories(logger=logger, gl=gl, gitlab_group_id=GITLAB_GROUP_ID)
    #repo_infos = repo_infos[1:5]  # remove me

    repo_infos = []
    repo_infos.append({'path_with_namespace': 'Adamer', 'id': 15535})  #todo remove me

    if repo_infos:
        if CLONING_REPOS_LOCALLY:
            GitHelper.clone_or_update_repositories(logger=logger, local_repo_dir=LOCAL_REPO_DIR, gitlab_url=GITLAB_URL,
                                                   repo_names=repo_infos)
        result_reports = []
        for repo in repo_infos:
            logger.info('---------------------')
            repo_name = repo['path_with_namespace']
            logger.info(f'Start analyzing Repo {repo_name}...')

            repo_project_id = repo['id']
            result_report = ResultReport(repo_name=repo_name, is_successful_crawled=True)

            project = gl.projects.get(repo_project_id)
            logger.info("=== Git Checks ===")

            result_report.counted_commits, result_report.git_repo_last_updated_at = GitHelper.count_git_commits(gl=gl,
                                                                                                                project=project)
            result_report.branch_names = GitHelper.git_get_branch_names(logger=logger, project=project)
            result_report.repo_has_multiple_branches = len(result_report.branch_names)

            logger.info('Searching for all Files in Repository')
            project_files = list_project_files_recursive(project=project)
            logger.info(f'Found {len(project_files)} Files to process')

            result_report.pipeline_running_successful, result_report.pipeline_job_details = BuildPipelineHelper.check_pipeline_status(
                project=project)

            pipeline_path = next((path for path in project_files if GITLAB_CI_PATH in path), None)
            if pipeline_path:
                result_report.missing_keywords_in_pipeline = BuildPipelineHelper.search_keywords_in_pipeline_file(
                    logger=logger, project=project,
                    pipeline_path=pipeline_path,
                    keywords=GITLAB_CI_REQUIRED_KEYWORDS)
            else:
                result_report.missing_keywords_in_pipeline = GITLAB_CI_REQUIRED_KEYWORDS

            logger.info("=== File Checking ===")

            repo_path = os.path.join(LOCAL_REPO_DIR, repo_name.replace('/', '_'))

            result_report.missing_files = check_if_there_are_all_required_files_existing(repo_files=project_files,
                                                                                         folder_to_be_searched=EXERCISE)
            result_report.analyse_markdown_character_count = check_if_analyse_md_seems_valid(repo_path,
                                                                                             ANALYSE_FILE_NAME)

            result_report.container_registry_contains_all_necessary_tags, result_report.container_image_tag_names, latest_image_tag_location = DockerHelper.check_if_docker_image_tags_exists_in_registry(
                logger=logger, project=project)

            dockerfile_path = next((path for path in project_files if DOCKERFILE_PATH in path), None)
            if dockerfile_path:
                logger.info("=== Docker Checks ===")
                DockerHelper.authenticate_docker_with_gitlab(latest_image_tag_location, GITLAB_USER_NAME,
                                                             GITLAB_PRIVATE_TOKEN)
                container_port = 9500

                env_vars = {'PATH_ORDER_SUCCESS': 'orders/success/', 'PATH_ORDER_FAILED': 'orders/failed/',
                            'PORT': f'{container_port}', 'ORDER_AMOUNT_PROMOTION': '100'}
                container_name = f'{current_year}_{EXERCISE}_{project.name}1'
                result_report.container_logs = DockerHelper.run_docker_image_from_container_registry(logger=logger,
                                                                                                     docker_client=docker_client,
                                                                                                     image_location=latest_image_tag_location,
                                                                                                     container_name=container_name,
                                                                                                     env_vars=env_vars,
                                                                                                     result_report=result_report,
                                                                                                     container_port=container_port)
            else:
                logger.warning('No Dockerfile found!')

            generate_report_foreach_repo(result_report)
            result_reports.append(result_report)
            logger.info('---------------------')

        generate_csv_for_all_reports(result_reports)
    else:
        logger.error("No repositories to process")


if __name__ == "__main__":
    main()
