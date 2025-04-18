from typing import List, Any
from .executable_script import ExecutableScript

class UnveilScript(ExecutableScript):
    """Handles the unveil.py script."""

    def __init__(self, folder_name: str):
        super().__init__(folder_name, "unveil.py", "Unveil")

    def validate(self) -> bool:
        """Validates the unveil.py script structure."""
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
        """Runs the unveil script to get the solution for part 2."""
        try:
            script_class = self._get_script_class()
            instance = script_class(lines=lines)
            return instance.run()
        except (FileNotFoundError, ImportError, AttributeError, TypeError, Exception) as e:
            raise RuntimeError(f"Failed to run '{self.script_filename}': {e}") from e
        
    def generate_template(self) -> str:
        """
        Generates a template for the unveil script.
        v1.0.0
        """
        return (
            "#!/usr/bin/env python3\n"
            "# -*- coding: utf-8 -*-\n"
            "from typing import List\n"
            "\n"
            "class Unveil:\n"
            "    def __init__(self, lines: List[str]):\n"
            "        self.lines = lines\n"
            "\n"
            "    def run(self) -> str:\n"
            "        # Implement the logic to unveil the solution here\n"
            "        # solution = 0\n"
            "        return solution\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    with open('input.txt') as f:\n"
            "        lines = f.readlines()\n"
            "    unveil = Unveil(lines)\n"
            "    solution = unveil.run()\n"
            "    print(solution)\n"
        )
