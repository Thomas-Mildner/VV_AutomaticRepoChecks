import gitlab


class BuildPipelineHelper:

    @staticmethod
    def search_keywords_in_pipeline_file(logger, project, pipeline_path, keywords):
        """
        Searches for specific keywords in a GitLab pipeline file.

        Args:
            logger (logger): Logger instance
            project (project): The Gitlab Project
            pipeline_path (str): The path to the pipeline file (e.g., .gitlab-ci.yml).
            keywords (list): A list of keywords to search for.

        Returns:
            dict: A dictionary with keywords as keys and boolean values indicating if the keyword was found.
        """

        try:
            file = project.files.get(file_path=pipeline_path, ref='main')
            file_content = file.decode().decode('utf-8')
        except gitlab.exceptions.GitlabGetError as e:
            logger.warning(f"Error retrieving file: {e}")
            return None

        missing_keywords = []
        # Search for keywords
        for keyword in keywords:
            if keyword not in file_content:
                missing_keywords.append(keyword)

        return missing_keywords

    @staticmethod
    def check_pipeline_status(project):
        """
        Checks if a GitLab pipeline is running successfully.

        Args:
            project (project): The Gitlab Project

        Returns:
            str: The status of the pipeline.
        """

        # Get the latest pipeline
        pipelines = project.pipelines.list(per_page=1)
        if pipelines:
            pipeline = pipelines[0]
            # List all jobs associated with the pipeline
            jobs = pipeline.jobs.list()

            # Collect detailed job information
            job_details = []
            for job in jobs:
                job_info = {
                    'name': job.name,
                    'status': job.status,
                    'stage': job.stage,
                    'created_at': job.created_at,
                    'started_at': job.started_at,
                    'finished_at': job.finished_at,
                }
                job_details.append(job_info)
            return pipeline.status, job_details

        return 'no pipeline found', None
