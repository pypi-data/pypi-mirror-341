from typing import List, Any
from .executable_script import ExecutableScript

class DecryptScript(ExecutableScript):
    """Handles the decrypt.py script."""

    def __init__(self, folder_name: str):
        super().__init__(folder_name, "decrypt.py", "Decrypt")

    def validate(self) -> bool:
        """Validates the decrypt.py script structure."""
        if not self.check_file_exists():
            return False
        try:
            script_class = self._get_script_class()
            # Instantiate with dummy values for validation
            instance = script_class(lines=["validation_line"])
            if not self._check_methods_exist(instance, ["__init__", "run"]):
                 return False
        except (FileNotFoundError, ImportError, AttributeError, TypeError, Exception) as e:
            print(f"> Error validating '{self.script_filename}': {e}")
            return False
        return True

    def run(self, lines: List[str]) -> Any:
        """Runs the decrypt script to get the solution for part 1."""
        try:
            script_class = self._get_script_class()
            instance = script_class(lines=lines)
            return instance.run()
        except (FileNotFoundError, ImportError, AttributeError, TypeError, Exception) as e:
            raise RuntimeError(f"Failed to run '{self.script_filename}': {e}") from e
        
    def generate_template(self) -> str:
        """
        Generates a template for the decrypt script.
        v1.0.0
        """
        return (
            "#!/usr/bin/env python3\n"
            "# -*- coding: utf-8 -*-\n"
            "from typing import List\n"
            "\n"
            "class Decrypt:\n"
            "    def __init__(self, lines: List[str]):\n"
            "        self.lines = lines\n"
            "\n"
            "    def run(self) -> str:\n"
            "        # Implement the logic to decrypt the lines here\n"
            "        # result = 0\n"
            "        return result\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    with open('input.txt') as f:\n"
            "        lines = f.readlines()\n"
            "    decrypt = Decrypt(lines)\n"
            "    solution = decrypt.run()\n"
            "    print(solution)\n"
        )
