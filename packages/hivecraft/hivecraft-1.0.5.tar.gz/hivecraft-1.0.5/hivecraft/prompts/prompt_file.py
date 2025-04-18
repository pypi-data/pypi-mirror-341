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
                
                # Check if the file starts and ends with <article> tag
                if not content.startswith("<article>") or not content.endswith("</article>"):
                    print(f"> Error: File '{self.filename}' does not start and end with <article> tag after stripping whitespace.")
                    return False
                
                # Check if the file contains a non-closed tag
                if content.count("<") != content.count(">"):
                    print(f"> Error: File '{self.filename}' contains non-closed tags.")
                    return False
                
                # Check for the presence of <a> tags and check if they are not empty and if the href attribute points to a valid URL
                if "<a " in content:
                    if not any(tag.startswith("<a href=") for tag in content.split("<a ")[1:]):
                        print(f"> Error: File '{self.filename}' does not contain valid <a> tags.")
                        return False
                    # Check if the href attribute points to a valid URL
                    for tag in content.split("<a ")[1:]:
                        if 'href="' in tag:
                            href = tag.split('href="')[1].split('"')[0]
                            if not href.startswith("http://") and not href.startswith("https://"):
                                print(f"> Error: Invalid URL in <a> tag in file '{self.filename}'.")
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
