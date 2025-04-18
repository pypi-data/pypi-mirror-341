from typing import List
from .executable_script import ExecutableScript

class ForgeScript(ExecutableScript):
    """Handles the forge.py script."""

    def __init__(self, folder_name: str):
        super().__init__(folder_name, "forge.py", "Forge")

    def validate(self) -> bool:
        """Validates the forge.py script structure."""
        if not self.check_file_exists():
            return False
        try:
            script_class = self._get_script_class()
            # Instantiate with dummy values for validation
            instance = script_class(lines_count=1, unique_id="validation_id")
            if not self._check_methods_exist(instance, ["__init__", "run"]):
                 return False
        except (FileNotFoundError, ImportError, AttributeError, TypeError, Exception) as e:
            print(f"> Error validating '{self.script_filename}': {e}")
            return False
        return True

    def run(self, lines_count: int, unique_id: str) -> List[str]:
        """Runs the forge script to generate input lines."""
        try:
            script_class = self._get_script_class()
            instance = script_class(lines_count=lines_count, unique_id=unique_id)
            return instance.run()
        except (FileNotFoundError, ImportError, AttributeError, TypeError, Exception) as e:
            raise RuntimeError(f"Failed to run '{self.script_filename}': {e}") from e
        
    def generate_template(self) -> str:
        """
        Generates a template for the forge script.
        v1.0.0
        """
        return (
            "#!/usr/bin/env python3\n"
            "# -*- coding: utf-8 -*-\n"
            "import random\n"
            "import sys\n"
            "from typing import List\n"
            "\n"
            "class Forge:\n"
            "    def __init__(self, lines_count: int, unique_id: str):\n"
            "        self.lines_count = lines_count\n"
            "        self.unique_id = unique_id\n"
            "        random.seed(unique_id)\n"
            "\n"
            "    def run(self) -> List[str]:\n"
            "        # Implement the logic to generate input lines here\n"
            "        # lines = []\n"
            "        return lines\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    lines_count = int(sys.argv[1])\n"
            "    unique_id = sys.argv[2]\n"
            "    forge = Forge(lines_count, unique_id)\n"
            "    lines = forge.run()\n"
            "    with open('input.txt', 'w') as f:\n"
            "        f.write('\\n'.join(lines) + '\\n')\n"
        )
