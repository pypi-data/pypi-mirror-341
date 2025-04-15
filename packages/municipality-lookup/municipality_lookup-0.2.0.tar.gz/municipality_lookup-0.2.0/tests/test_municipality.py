from municipality_lookup.instance import get_db
from municipality_lookup.models import Municipality


def test_exact_match():
    db = get_db()
    result = db.get_by_name("ABANO TERME")
    assert isinstance(result, Municipality)
    assert result.name != ""
    assert result.province == "PD"


def test_fuzzy_match():
    db = get_db()
    result = db.get_by_name("abno terne", min_score=0.7, fast=False)
    assert isinstance(result, Municipality)
    assert "ABANO TERME" in result.name.upper()


def test_fuzzy_match_space():
    db = get_db()
    result = db.get_by_name("A L E S S A N D R I A", min_score=0.8)
    assert isinstance(result, Municipality)
    assert "ALESSANDRIA" in result.name.upper()


def test_fuzzy_below_threshold():
    db = get_db()
    result = db.get_by_name("abno trne", min_score=0.95)  # simile ma sotto soglia
    assert isinstance(result, Municipality)
    assert result.name == ""


def test_case_and_accent_insensitivity():
    db = get_db()
    result = db.get_by_name("àbànò térmé", min_score=0.8)
    assert isinstance(result, Municipality)
    assert "ABANO TERME" in result.name.upper()


def test_no_match():
    db = get_db()
    result = db.get_by_name("ZZZZZZZZZ", min_score=0.8)
    assert isinstance(result, Municipality)
    assert result.name == ""


# Nuovi test aggiunti

def test_fuzzy_with_special_characters():
    db = get_db()
    result = db.get_by_name("abano@terme", min_score=0.8)
    assert isinstance(result, Municipality)
    assert "ABANO TERME" in result.name.upper()


def test_fuzzy_with_truncated_name():
    db = get_db()
    result = db.get_by_name("ab4no t3rne", min_score=0.7, fast=False)
    assert isinstance(result, Municipality)
    assert "ABANO TERME" in result.name.upper()


def test_fuzzy_with_multiple_typo():
    db = get_db()
    result = db.get_by_name("Er- . bezzo", min_score=0.8)
    assert isinstance(result, Municipality)
    assert "ERBEZZO" in result.name.upper()

def test_fuzzy_with_multiple_typo_fast():
    db = get_db()
    result = db.get_by_name("Er- . bezzo", min_score=0.8, fast=True)
    assert isinstance(result, Municipality)
    assert "ERBEZZO" in result.name.upper()


def test_no_match_gibberish():
    db = get_db()
    result = db.get_by_name("xyzqwe", min_score=0.8)
    assert isinstance(result, Municipality)
    assert result.name == ""


def test_fuzzy_with_plural_typo():
    db = get_db()
    result = db.get_by_name("abano termi", min_score=0.8)
    assert isinstance(result, Municipality)
    assert "ABANO TERME" in result.name.upper()


def test_return_type():
    db = get_db()
    result = db.get_by_name("ABANO TERME")
    assert isinstance(result, Municipality)
