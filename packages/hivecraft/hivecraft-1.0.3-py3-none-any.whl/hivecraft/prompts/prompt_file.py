import os
from abc import ABC, abstractmethod

class PromptFile(ABC):
    """Base class for handling HTML prompt files."""

    def __init__(self, folder_name: str, filename: str):
        self.folder_name = folder_name
        self.filename = filename
        self.filepath = os.path.join(folder_name, filename)

    def check_file_exists(self) -> bool:
        """Checks if the prompt file exists."""
        if not os.path.isfile(self.filepath):
            print(f"> Error: Prompt file '{self.filename}' is missing in '{self.folder_name}'.")
            return False
        return True

    def validate(self) -> bool:
        """Validates the basic structure of the HTML prompt file."""
        if not self.check_file_exists():
            return False
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content.startswith("<article>") or not content.endswith("</article>"):
                    print(f"> Error: File '{self.filename}' does not start and end with <article> tag after stripping whitespace.")
                    return False
        except Exception as e:
            print(f"> Error reading or validating prompt file '{self.filename}': {e}")
            return False
        return True

    @abstractmethod
    def generate_template(self) -> str:
        """Generates a template content for the prompt file."""
        pass

    def write_template(self):
        """Writes the generated template to the file if it doesn't exist."""
        if not os.path.isfile(self.filepath):
            try:
                os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    f.write(self.generate_template())
                print(f"> Created default prompt file: '{self.filename}'")
            except Exception as e:
                print(f"> Error writing template file '{self.filename}': {e}")
