"""
Basic smoke tests for the /ask and /healthz endpoints.
Run: pytest tests/test_ask.py
Requires a running local instance: python app.py
"""

import pytest
import requests

BASE_URL = "http://localhost:8000"


def test_healthz():
    r = requests.get(f"{BASE_URL}/healthz", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "faiss_loaded" in data


def test_ask_basic():
    payload = {"question": "What are early signs of autism?"}
    r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=30)
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert len(data["answer"]) > 20


def test_ask_french():
    payload = {"question": "Quels sont les premiers signes de l'autisme ?"}
    r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=30)
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data


def test_ask_arabic():
    payload = {"question": "ما هي العلامات المبكرة للتوحد؟"}
    r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=30)
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data


def test_ask_empty_question():
    r = requests.post(f"{BASE_URL}/ask", json={"question": ""}, timeout=10)
    assert r.status_code == 400


def test_citations_format():
    payload = {"question": "Down syndrome communication strategies"}
    r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=30)
    assert r.status_code == 200
    data = r.json()
    citations = data.get("citations", [])
    for c in citations:
        assert "source" in c
        assert c["source"] != "NC"
