# ✅ File: tests/test_main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ✅ Test queries and expected keywords
TEST_CASES = [
    # Wikipedia/general knowledge queries
    ("What is Python?", ["Python", "interpreted", "language"]),
    ("What is Machine Learning?", ["Machine learning", "data", "AI"]),

    # Mock data queries
    ("Top schools in Indore", ["Emerald Heights", "Indore Public School"]),
    ("Top-rated dentists near me", ["Dental", "Clinic"]),
    ("Vegetarian restaurants within 2 km of MG Road, Bengaluru", ["Green Theory", "Little Green"]),
    ("Trending events in Jaipur this weekend - Is there any late-night food delivery around Indiranagar?", ["Jaipur Music", "Empire", "Meghana"]),
    ("Top-rated dentists in Bengaluru", ["32 Smiles", "Smile Zone"]),

    # DuckDuckGo fallback (not in mock or Wikipedia)
    ("Gyms in JP Nagar, Bengaluru", ["gym", "fitness", "JP Nagar"]),

    # Fallback message when nothing is found
    ("Some unknown topic to test fallback", ["Sorry", "couldn’t find"])
]

@pytest.mark.parametrize("query,expected_keywords", TEST_CASES)
def test_query_responses(query, expected_keywords):
    response = client.post("/search", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert any(keyword.lower() in data["response"].lower() for keyword in expected_keywords), \
        f"Response for '{query}' did not contain any expected keywords."

def test_empty_query():
    response = client.post("/search", json={"query": ""})
    assert response.status_code == 200
    assert "Sorry" in response.json()["response"] or "couldn’t find" in response.json()["response"]
