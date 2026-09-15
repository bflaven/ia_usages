"""Tests for the shared style_guide logic and the FastAPI legacy endpoint.

Covers the three acceptance-criteria scenarios from docs/02_user_story.md:
known term, unknown term, and (separately, via test_client_demo.py) a
second independent client reaching the same data.
"""

from fastapi.testclient import TestClient

from src import style_guide
from src.main import app


def test_lookup_known_term():
    result = style_guide.lookup_term("Sud-Liban", "fr-en")
    assert result["found"] is True
    assert result["approved"] == "southern Lebanon"
    assert "guide_last_updated" in result


def test_lookup_unknown_term_returns_suggestions_not_a_guess():
    result = style_guide.lookup_term("a term that does not exist")
    assert result["found"] is False
    assert result["suggestions"] == [] or isinstance(result["suggestions"], list)


def test_lookup_unknown_term_suggests_close_matches():
    result = style_guide.lookup_term("Sud Liban")  # missing the hyphen
    assert result["found"] is False
    assert "Sud-Liban" in result["suggestions"]


def test_check_style_rule_finds_known_terms_in_text():
    text = "Our coverage of Sud-Liban used generative AI for the first draft."
    result = style_guide.check_style_rule(text)
    hit_terms = [h["term"] for h in result["hits"]]
    assert "Sud-Liban" in hit_terms


def test_legacy_rest_endpoint_matches_shared_logic():
    client = TestClient(app)
    response = client.get(
        "/legacy/lookup-term", params={"term": "Sud-Liban", "language_pair": "fr-en"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["found"] is True
    assert body["approved"] == "southern Lebanon"


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
