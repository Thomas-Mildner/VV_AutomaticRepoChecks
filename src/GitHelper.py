import os
import shutil

import git
import gitlab
from git import Repo


class GitHelper:

    @staticmethod
    def get_repositories(logger, gl, gitlab_group_id):
        try:
            logger.info(f'Starting to Crawl Repos for GroupId: {gitlab_group_id}')
            group = gl.groups.get(gitlab_group_id)
            projects = group.projects.list(all=True)
            repo_info = [{'path_with_namespace': project.path_with_namespace, 'id': project.id} for project in projects]
            logger.info(f"Found {len(repo_info)} repositories in the group.")
            return repo_info
        except Exception as e:
            logger.error(f"Error fetching repositories: {e}")
            return []

    @staticmethod
    def clone_or_update_repositories(logger, local_repo_dir, gitlab_url, repo_names):
        os.makedirs(local_repo_dir, exist_ok=True)
        for repo in repo_names:
            repo_name = repo['path_with_namespace']
            repo_url = f"{gitlab_url}/{repo_name}.git"
            local_path = os.path.join(local_repo_dir, repo_name.replace('/', '_'))
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

    @staticmethod
    def count_git_commits(gl, project):
        try:
            commits = project.commits.list(all=True)
            if commits:
                last_commit = commits[0]
                last_commit_date = last_commit.committed_date
                return len(commits), last_commit_date

            return 0, None
        except:
            return 0, None

    @staticmethod
    def git_get_branch_names(logger, project):
        try:
            branches = project.branches.list()
            branch_names = [branch.name for branch in branches]
            return branch_names
        except gitlab.exceptions.GitlabListError as e:
            logger.warning(f"Error fetching branches: {e}")
            return []

