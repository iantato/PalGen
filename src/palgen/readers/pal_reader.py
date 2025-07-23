import json
from loguru import logger
from palgen.constants import PAL_INFO
from palgen.models.pal_model import Pal
from palgen.readers.localization_reader import LocalizationReader

class PalReader:

    def __init__(self, file_path: str):
        self.file_path = f'{file_path}/{PAL_INFO}'
        self.names = LocalizationReader(file_path).read()
        self.pals = []

    def read(self):
        """Reads and parses the Pal data from the JSON file."""
        try:
            internal_idx = 1

            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)[0]['Rows'] # Isolates data to only the Pal information.
                for k, v in data.items():
                    if (v.get('IsPal') and (not v.get('IsBoss') and not v.get('IsTowerBoss') and not v.get('isRaidBoss'))):
                        if self.get_pal_name(v.get('BPClass')) != "Unknown Pal":
                            pal = Pal(**v, internal_index=internal_idx, text_name=self.get_pal_name(v.get('BPClass')))
                            self.pals.append(pal)
                            logger.debug(f"Added Pal: {pal.text_name} (Internal Index: {internal_idx})")
                            internal_idx += 1
            return self.pals
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            raise FileNotFoundError(f"File not found: {self.file_path}")
        except Exception as e:
            logger.error(f"An error occurred while reading the file: {e}")
            raise Exception(f"An error occurred while reading the file: {e}")

    def get_pal_name(self, bp_class: str) -> str:
        """Returns the localized name of the Pal based on its blueprint class."""
        return self.names.get(f'pal_name_{bp_class.lower()}', "Unknown Pal")