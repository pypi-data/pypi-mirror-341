import importlib.resources
from importlib.resources import files
from municipality_lookup import MunicipalityDB

_db_instance = None

def get_db(csv_path: str = None) -> MunicipalityDB:
    global _db_instance
    if _db_instance is None:
        if csv_path is None:
            # Load built-in CSV
            csv_path = files("municipality_lookup.data").joinpath("comuni.csv")
        _db_instance = MunicipalityDB(str(csv_path))
    return _db_instance
