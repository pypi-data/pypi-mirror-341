from dataclasses import dataclass

@dataclass
class Municipality:
    name: str
    province: str
    land_registry: str
    national_code: str
    cadastral_code: str
