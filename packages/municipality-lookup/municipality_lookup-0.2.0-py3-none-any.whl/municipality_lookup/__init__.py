import logging
from .database import MunicipalityDatabase
from .search import MunicipalitySearcher
from .utils import normalize_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MunicipalityDB:
    def __init__(self, csv_path: str = "data/comuni.csv", min_similarity: float = 0.8):
        
        logger.info("Loading municipality database from: %s", csv_path)
        self.db = MunicipalityDatabase(csv_path)
        self.searcher = MunicipalitySearcher(self.db.get_all())
        self.min_similarity = min_similarity

    def get_by_name(self, name: str, min_score: float = None, fast: bool = True):
        norm_name = normalize_name(name)
        logger.debug("Searching for name: %s (normalized)", norm_name)

        result = self.searcher.find_exact(norm_name)
        if result:
            logger.info("Exact match found for %s", name)
            return result

        score = min_score if min_score is not None else self.min_similarity
        logger.info("No exact match, performing fuzzy search (min_score=%s, fast=%s)", score, fast)

        if fast:
            return self.searcher.find_similar_fast(norm_name, score)
        else:
            return self.searcher.find_similar(norm_name, score)


    def get_all_provinces(self) -> list[str]:
        return list(set(m.province for m in self.db.get_all()))

    def get_all_land_registries(self) -> list[str]:
        return list(set(m.land_registry for m in self.db.get_all()))

    def update_database(self, new_csv_path: str):
        logger.info("Updating database from: %s", new_csv_path)
        self.db.update_database(new_csv_path)
        self.searcher = MunicipalitySearcher(self.db.get_all())
