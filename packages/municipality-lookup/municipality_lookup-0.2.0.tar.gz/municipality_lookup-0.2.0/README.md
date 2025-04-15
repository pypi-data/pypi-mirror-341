# 🏛️ Municipality Lookup

**Municipality Lookup** is a lightweight Python library for retrieving information about Italian municipalities (comuni), including province, land registry office, national code, and cadastral code.

It supports both exact and fuzzy search — ideal for OCR scenarios or user input with typos. The official dataset is embedded and loaded automatically.

---

## 📦 Installation

Install via pip:

```bash
pip install municipality-lookup
```

---

## 🚀 Getting Started

Import and initialize the database using the default embedded CSV:

```python
from municipality_lookup.instance import get_db

# Load the built-in database
db = get_db()
```

---

## 🔍 Search for a Municipality

```python
# Exact match (case-insensitive)
result = db.get_by_name("ABANO TERME")
print(result)
# ➜ Municipality(name='ABANO TERME', province='PD', ...)
```

### ✨ Fuzzy search (handles typos or OCR noise)

```python
# Typo-tolerant search
result = db.get_by_name("abno terme")
print(result)
```

You can customize the **minimum similarity score** (default is `0.8`) and choose between:
- `fast=True` (default): faster search using RapidFuzz internals
- `fast=False`: slower but more controllable logic with combined ratio + partial_ratio

```python
# Custom fuzzy search
result = db.get_by_name("abano trm", min_score=0.7, fast=False)
```

---

## 📋 Explore the Dataset

```python
# List all province codes
print(sorted(db.get_all_provinces()))

# List all land registry offices
print(sorted(db.get_all_land_registries()))
```

---

## 🔄 Update the Database with a Custom CSV

You can replace the internal dataset with a custom file (same structure as the built-in one):

```python
db.update_database("path/to/your_custom_comuni.csv")
```

---

## 📄 CSV Structure

Custom CSVs must have the following columns (case-sensitive headers):

| Column                          | Description                               |
|---------------------------------|-------------------------------------------|
| `Comune`                        | Municipality name (string)                |
| `Provincia`                     | Province code (e.g. "PD")                 |
| `Conservatoria di Competenza`  | Land registry office                      |
| `Codice Nazionale`             | National municipality code (4 chars)      |
| `Codice Catastale`             | Cadastral code (4 chars)                  |

✅ Example:

```csv
Comune,Provincia,Conservatoria di Competenza,Codice Nazionale,Codice Catastale
ABANO TERME,PD,Padova,A001,D3AB
ABBADIA CERRETO,LO,Lodi,A004,C1AB
```

➡️ Rows with missing or invalid fields may be ignored or raise errors.

---

## 📚 Data Source

The default dataset is based on publicly available information from:

🔗 [visurasi.it – Elenco conservatorie e comuni](https://www.visurasi.it/elenco-conservatorie-e-comuni)

---

## 🧠 Advanced

You can use `find_exact()`, `find_similar()`, or `find_similar_fast()` directly if needed, via:

```python
from municipality_lookup.search import MunicipalitySearcher
```

---

## 📜 License

MIT © Andrea Iannazzo
