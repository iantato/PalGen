import json
from palgen.models.combiunique_model import CombiUniqueModel
from palgen.constants import UNIQUE_BREEDING

class CombiUniqueReader:

    def __init__(self, file_path: str) -> None:
        self.file_path = f'{file_path}/{UNIQUE_BREEDING}'
        self.combi_uniques = []

    def read(self) -> list[CombiUniqueModel]:
        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)[0]['Rows']
                for k, v in data.items():
                    combination = CombiUniqueModel(**v)
                    self.combi_uniques.append(combination)

                return self.combi_uniques
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {self.file_path}")
            except Exception as e:
                raise Exception(f"An error occurred while reading the file: {e}")