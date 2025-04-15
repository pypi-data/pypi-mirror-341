import pandas as pd
import os
import pickle
import hashlib
from typing import List
from municipality_lookup.models import Municipality

def _csv_hash(path: str) -> str:
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

class MunicipalityDatabase:
    def __init__(self, csv_path: str, cache_dir: str = ".cache"):
        self.csv_path = csv_path
        self.cache_dir = cache_dir
        self.hash = _csv_hash(csv_path)
        self.cache_file = os.path.join(cache_dir, f"{self.hash}.pkl")

        os.makedirs(cache_dir, exist_ok=True)

        if os.path.exists(self.cache_file):
            self._municipalities = self._load_from_pickle()
        else:
            self._df = pd.read_csv(csv_path, dtype=str).fillna('')
            self._df.columns = [col.strip() for col in self._df.columns]
            self._municipalities = self._load_municipalities()
            self._save_to_pickle()

    def _load_municipalities(self) -> List[Municipality]:
        return [
            Municipality(
                name=row['Comune'].strip(),
                province=row['Provincia'].strip(),
                land_registry=row['Conservatoria di Competenza'].strip(),
                national_code=row['Codice Nazionale'].strip(),
                cadastral_code=row['Codice Catastale'].strip()
            )
            for _, row in self._df.iterrows()
        ]

    def _save_to_pickle(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self._municipalities, f)

    def _load_from_pickle(self) -> List[Municipality]:
        with open(self.cache_file, 'rb') as f:
            return pickle.load(f)

    def get_all(self) -> List[Municipality]:
        return self._municipalities

    def update_database(self, new_csv_path: str):
        self.__init__(new_csv_path, cache_dir=self.cache_dir)

    def clear_cache(self):
        for file in os.listdir(self.cache_dir):
            if file.endswith(".pkl"):
                os.remove(os.path.join(self.cache_dir, file))
