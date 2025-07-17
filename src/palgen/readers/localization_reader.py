import json
from palgen.constants import PAL_NAME

class LocalizationReader:

    def __init__(self, file_path: str):
        self.file_path = f'{file_path}/{PAL_NAME}'
        self.names = {}

    def read(self) -> dict:
        """Reads and parses the localization data for the Pal names from specified JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)[0]['Rows'] # Isolates data to only the pal names.
                for k, v in data.items():
                    if k.startswith('PAL_NAME_'):
                        name = v.get('TextData').get('LocalizedString')
                        # Ensure the name is not empty or a placeholder.
                        if name != 'en_text':
                            # Store the name with the key in lowercase for consistency.
                            # This allows for case-insensitive lookups.
                            self.names[k.lower()] = name
            return self.names
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {e}")