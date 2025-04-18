import os
import datetime
import xml.etree.ElementTree as ET
from hivecraft.props.meta.fields import META_FIELDS, XML_NAMESPACE

"""
meta.xml is a file that contains the properties of the metadata of the Alghive file
<Properties xmlns="http://www.w3.org/2001/WMLSchema">
    <author>...</author>
    <created>...</created>
    <modified>...</modified>
    <hivecraft_version>...</hivecraft_version>
    <title>...</title>
    <id>...</id>
</Properties>
"""
class MetaProps:
    def __init__(self, folder_name: str):
        self.folder_name = folder_name
        self.props_dir = os.path.join(folder_name, "props")
        self.file_name = os.path.join(self.props_dir, "meta.xml")
        self._fields = {field.name: field for field in META_FIELDS}
        # Initialize values using the default_value property which handles factories
        self._values = {field.name: field.default_value for field in META_FIELDS}

        # Dynamically create attributes for easy access
        for name, value in self._values.items():
            setattr(self, name, value)

    def _update_internal_values(self):
        """Updates internal dictionary from instance attributes."""
        for name in self._fields.keys():
            # Special handling for 'modified' - always update to current time on save
            if name == 'modified':
                modified_field = self._fields['modified']
                # Use the default_value property which correctly handles factories
                new_modified_val = modified_field.default_value
                self._values[name] = new_modified_val
                setattr(self, name, new_modified_val) # Also update the attribute
            else:
                self._values[name] = getattr(self, name)


    def _update_attributes(self):
        """Updates instance attributes from internal dictionary."""
        for name, value in self._values.items():
            setattr(self, name, value)

    def check_file_integrity(self): # Removed 'update' parameter
        """Checks if the file exists and is valid, creates/updates it otherwise."""


        os.makedirs(self.props_dir, exist_ok=True) # Ensure props directory exists

        if os.path.isfile(self.file_name):
            try:
                tree = ET.parse(self.file_name)
                root = tree.getroot()
                # Check root tag and namespace
                if not root.tag.endswith("Properties"): # Handle potential namespace prefix
                     raise ValueError(f"Invalid root tag in '{self.file_name}'. Expected 'Properties'.")

                parsed_values = {}
                for field_def in self._fields.values():
                    # Find element using namespace
                    element = root.find(f"ns:{field_def.name}", XML_NAMESPACE)
                    parsed_values[field_def.name] = field_def.parse_and_validate(element)

                # Special case: Update 'modified' time after successful load
                modified_field = self._fields['modified']
                parsed_values['modified'] = modified_field.default_value # Regenerate current time

                self._values = parsed_values # Update internal values
                self._update_attributes() # Update instance attributes

            except ET.ParseError as e:
                print(f"> Warning: Error parsing XML file '{self.file_name}': {e}. Overwriting with defaults.")
                self._values = {field.name: field.default_value for field in META_FIELDS} # Reset to defaults
                self._update_attributes()
                self.write_file() # Overwrite with default values
            except ValueError as e: # Catch validation errors
                print(f"> Warning: Validation error in '{self.file_name}': {e}. Overwriting with defaults.")
                self._values = {field.name: field.default_value for field in META_FIELDS} # Reset to defaults
                self._update_attributes()
                self.write_file() # Overwrite with default values
        else:
            # File does not exist, create it with defaults
            print()
            print(f"> File '{self.file_name}' does not exist. Creating a default one.")
            # Print defaults dynamically
            defaults_str = ", ".join(f"{name}='{value}'" for name, value in self._values.items())
            print(f"  Defaults: {defaults_str}")
            print()
            self.write_file() # Creates the file with default values

    def write_file(self):
        """Writes the current properties to the meta.xml file."""
        # Ensure 'modified' time is updated before writing
        self._update_internal_values()
        os.makedirs(self.props_dir, exist_ok=True)

        # Use the namespace in the root element only
        root = ET.Element("Properties", xmlns=XML_NAMESPACE["ns"])

        for field_def in self._fields.values():
             # Create element without explicit namespace (will inherit from root)
             elem = ET.SubElement(root, field_def.name)
             value = self._values.get(field_def.name)
             # Convert value to string for XML text content
             elem.text = str(value) if value is not None else ""

        # Pretty print XML
        ET.indent(root, space="    ")
        tree = ET.ElementTree(root)
        # Add XML declaration and write
        tree.write(self.file_name, encoding='utf-8', xml_declaration=True)