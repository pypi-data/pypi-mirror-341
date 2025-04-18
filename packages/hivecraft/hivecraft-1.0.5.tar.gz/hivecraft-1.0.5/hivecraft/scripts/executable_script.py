import os
import importlib.util
import sys
from abc import ABC, abstractmethod
from typing import Any, List

class ExecutableScript(ABC):
    """Base class for handling executable Python scripts within an Alghive folder."""

    def __init__(self, folder_name: str, script_filename: str, expected_class_name: str):
        self.folder_name = folder_name
        self.script_filename = script_filename
        self.script_path = os.path.join(folder_name, script_filename)
        self.expected_class_name = expected_class_name
        self._module = None
        self._script_class = None

    def _load_module(self) -> Any:
        """Loads the Python script as a module."""
        if self._module is None:
            if not os.path.isfile(self.script_path):
                raise FileNotFoundError(f"Script file '{self.script_filename}' not found in '{self.folder_name}'.")
            try:
                module_name = os.path.splitext(self.script_filename)[0]
                spec = importlib.util.spec_from_file_location(module_name, self.script_path)
                if spec is None or spec.loader is None:
                     raise ImportError(f"Could not create spec for module '{module_name}' from '{self.script_path}'.")
                self._module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = self._module # Add to sys.modules to handle potential relative imports within the script
                spec.loader.exec_module(self._module)
            except Exception as e:
                raise ImportError(f"Failed to import script '{self.script_filename}': {e}")
        return self._module

    def _get_script_class(self) -> Any:
        """Gets the expected class from the loaded module."""
        if self._script_class is None:
            module = self._load_module()
            if not hasattr(module, self.expected_class_name):
                raise AttributeError(f"Script '{self.script_filename}' does not contain the expected class '{self.expected_class_name}'.")
            self._script_class = getattr(module, self.expected_class_name)
        return self._script_class

    def check_file_exists(self) -> bool:
        """Checks if the script file exists."""
        if not os.path.isfile(self.script_path):
            print(f"> Error: Script file '{self.script_filename}' is missing in '{self.folder_name}'.")
            return False
        return True

    @abstractmethod
    def validate(self) -> bool:
        """Validates the structure and content of the script."""
        pass

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Executes the main functionality of the script."""
        pass
    
    @abstractmethod
    def generate_template(self) -> str:
        """Generates a template for the script."""
        pass

    def _check_methods_exist(self, instance: Any, methods: List[str]) -> bool:
        """Checks if required methods exist on a class instance."""
        for method in methods:
            if not hasattr(instance, method) or not callable(getattr(instance, method)):
                print(f"> Error: Class '{self.expected_class_name}' in '{self.script_filename}' is missing required method '{method}'.")
                return False
        return True
