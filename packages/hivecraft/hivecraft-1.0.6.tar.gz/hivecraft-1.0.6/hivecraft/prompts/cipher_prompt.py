from .prompt_file import PromptFile

class CipherPrompt(PromptFile):
    """Handles the cipher.html prompt file."""

    def __init__(self, folder_name: str):
        super().__init__(folder_name, "cipher.html")

    def generate_template(self) -> str:
        """Generates the template for cipher.html."""
        return (
            "<article>\n"
            "  <h2>Part 1: Cipher</h2>\n"
            "  <p>Describe the first part of the puzzle here.</p>\n"
            "  <p>Provide examples:</p>\n"
            "  <code><pre>\n"
            "Input:\n"
            "...\n\n"
            "Output:\n"
            "...\n"
            "  </pre></code>\n"
            "</article>\n"
        )
