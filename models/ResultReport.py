class ResultReport:

    def __init__(self, repo_name: str, is_successful_crawled, repo_has_multiple_branches: bool = None, branch_names: [] = None, missing_files: [str] = None,
                 analyse_markdown_character_count: int = None, counted_commits: int = None, git_repo_last_updated_at= None,
                 pipeline_running_successful: bool = None, pipeline_job_details: [] = None,
                 missing_keywords_in_pipeline: [] = None, container_image_tag_names: [] = None,
                 container_registry_contains_all_necessary_tags: bool = None,
                 container_logs: [] = None,
                 data=None,
                 error_message=None):
        """
        Initializes a Result object.

        Args:
            is_successful_crawled (bool): Whether the operation was successful.
            data (any): The data returned by the operation.
            error_message (str, optional): An error message if the operation failed. Defaults to None.
        """

        self.container_logs = container_logs
        self.container_registry_contains_all_necessary_tags = container_registry_contains_all_necessary_tags
        self.container_image_tag_names = container_image_tag_names
        self.branch_names = branch_names
        self.repo_has_multiple_branches = repo_has_multiple_branches
        self.git_repo_last_updated_at = git_repo_last_updated_at
        self.missing_keywords_in_pipeline = missing_keywords_in_pipeline
        self.pipeline_job_details = pipeline_job_details
        self.counted_commits = counted_commits
        self.pipeline_running_successful = pipeline_running_successful
        self.analyse_markdown_character_count = analyse_markdown_character_count
        self.repo_name = repo_name
        self.is_successfulCrawled = is_successful_crawled
        self.missing_files = missing_files
        self.data = data
        self.error_message = error_message

    def generate_markdown(self):
        """
        Generates the markdown representation of the Result object.

        Returns:
            str: The markdown string representing the Result report.
        """

        markdown = f"## {self.repo_name} Results\n"

        if self.is_successfulCrawled:
            markdown += '## GIT Statistics \n'
            markdown += f"* **Successful Crawled:** {self.is_successfulCrawled}\n"
            markdown += f"* **Has Multiple Branches:** {self.repo_has_multiple_branches}\n"
            if self.branch_names:
                markdown += "* **Branch Names:** \n"
                for branch_name in self.branch_names:
                    markdown += f"{branch_name},"

            markdown += f"\n * **Last Updated at:** {self.git_repo_last_updated_at}\n"
            markdown += f"* **Counted Commits in Repo:**\n  {self.counted_commits}\n"
            markdown += f"* **Last Build Pipeline Status in Repo:**\n  {self.pipeline_running_successful}\n"
            if self.pipeline_job_details:
                for job in self.pipeline_job_details:
                    job_line = f"  - **Name**: {job['name']}, **Status**: {job['status']}, **Stage**: {job['stage']}, **Started At**: {job['started_at']}\n"
                    markdown += job_line
            else:
                markdown += 'No Pipeline Job Details found \n'
            if self.missing_keywords_in_pipeline:
                markdown += "* **Missing Keywords in Build Pipeline**: \n"
                for keyword in self.missing_keywords_in_pipeline:
                    markdown += f"{keyword},"

            markdown += "\n ## Required Files \n"
            markdown += f"* **MissingFiles in Repo:**\n  {self.missing_files}\n"
            markdown += f"* **Character Count of Analyse.md:**\n  {self.analyse_markdown_character_count}\n"

            markdown += '## Docker \n'
            markdown += f"\n * **Contains all necessary image tags:** {self.container_registry_contains_all_necessary_tags}\n"
            if self.container_image_tag_names:
                markdown += "* **Container Tags:** \n"
                for image_tag in self.container_image_tag_names:
                    markdown += f"{image_tag},"
            if self.container_logs:
                markdown += "\n * **Container Logs:** \n"
                for log_entry in self.container_logs:
                    log_entry_line = f"\t\t- {log_entry}\n"
                    markdown += log_entry_line

        else:
            markdown += f"* **Error Message:**\n  {self.error_message}\n"

        return markdown
