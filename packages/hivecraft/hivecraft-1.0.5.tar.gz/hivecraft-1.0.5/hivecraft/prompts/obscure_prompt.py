from .prompt_file import PromptFile

class ObscurePrompt(PromptFile):
    """Handles the obscure.html prompt file."""

    def __init__(self, folder_name: str):
        super().__init__(folder_name, "obscure.html")

    def generate_template(self) -> str:
        """Generates the template for obscure.html."""
        return (
            "<article>\n"
            "  <h2>Part 2: Obscure</h2>\n"
            "  <p>Describe the second part of the puzzle here.</p>\n"
            "  <p>Provide examples:</p>\n"
            "  <code><pre>\n"
            "Input:\n"
            "...\n\n"
            "Output:\n"
            "...\n"
            "  </pre></code>\n"
            "</article>\n"
        )
