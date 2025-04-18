from typing import Type, Callable, Any, Optional
import xml.etree.ElementTree as ET

class FieldDefinition:
    """Represents the definition of a field within an XML properties file."""
    def __init__(self,
                 name: str,
                 data_type: Type,
                 required: bool = True,
                 validator: Optional[Callable[[Any], bool]] = None,
                 default_value: Optional[Any] = None,
                 default_value_factory: Optional[Callable[[], Any]] = None): # Added factory
        self.name = name
        self.data_type = data_type
        self.required = required
        self.validator = validator
        # Ensure only one default mechanism is provided
        if default_value is not None and default_value_factory is not None:
            raise ValueError("Cannot provide both default_value and default_value_factory")
        self._default_value = default_value
        self._default_value_factory = default_value_factory

    @property
    def default_value(self) -> Any:
        """Gets the default value, generating it if a factory is provided."""
        if self._default_value_factory:
            return self._default_value_factory()
        return self._default_value

    def parse_and_validate(self, element: Optional[ET.Element]) -> Any:
        """Parses the value from an XML element, validates, and type-converts it."""
        current_default = self.default_value # Get potentially generated default

        if element is None:
            if self.required:
                # If required and no element, check if there's a default.
                # If no default either, it's an error.
                if current_default is None:
                     raise ValueError(f"Required field '{self.name}' is missing and has no default value.")
                # Otherwise, use the default.
                return current_default
            return current_default # Not required, return default (which could be None)

        value_str = element.text
        if value_str is None or value_str.strip() == "": # Treat empty tags like missing for required fields
            if self.required:
                if current_default is None:
                    raise ValueError(f"Required field '{self.name}' has no value and no default.")
                # Use default if element is present but empty
                value = current_default
            else:
                 # Not required and empty/missing value, use default
                 return current_default
        else:
            try:
                # Attempt type conversion only if value_str is not empty
                value = self.data_type(value_str)
            except (ValueError, TypeError) as e:
                # If conversion fails, check if the raw string matches a string default
                if self.data_type is str and value_str == current_default:
                     value = current_default
                else:
                    raise ValueError(f"Field '{self.name}' has invalid type or format. Expected {self.data_type.__name__}, got '{value_str}'. Error: {e}")

        if self.validator and not self.validator(value):
            # Re-validate even if using default, in case default is somehow invalid
            # (though validators should ideally ensure defaults are valid)
            raise ValueError(f"Field '{self.name}' failed validation with value '{value}'.")

        return value

    def to_xml_string(self, value: Any) -> str:
        """Formats the field value as an XML string."""
        # Handle potential None values, especially for non-required fields
        value_str = str(value) if value is not None else str(self.default_value) if self.default_value is not None else ""
        return f"    <{self.name}>{value_str}</{self.name}>\n"