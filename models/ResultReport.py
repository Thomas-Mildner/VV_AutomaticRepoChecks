class ResultReport:

    def __init__(self, repo_name: str, is_successful_crawled, missing_files: [str] = None, analyse_markdown_character_count: int =None, data=None,
                 error_message=None):
        """
        Initializes a Result object.

        Args:
            is_successful_crawled (bool): Whether the operation was successful.
            data (any): The data returned by the operation.
            error_message (str, optional): An error message if the operation failed. Defaults to None.
        """

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
        markdown += f"* **Successful Crawled:** {self.is_successfulCrawled}\n"

        if self.is_successfulCrawled:
            markdown += f"* **MissingFiles in Repo:**\n  {self.missing_files}\n"
            markdown += f"* **Character Count of Analyse.md:**\n  {self.analyse_markdown_character_count}\n"
            markdown += f"* **Data:**\n  {self.data}\n"  # Consider formatting based on data type
        else:
            markdown += f"* **Error Message:**\n  {self.error_message}\n"

        return markdown
