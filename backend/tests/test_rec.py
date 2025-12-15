import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import clio.functions as clio

def test_generate_recommendations_happy_path(monkeypatch):
    monkeypatch.setattr(clio, "db_get_user_interest_names", lambda username: ["art", "history"])
    monkeypatch.setattr(clio, "db_get_attractions_with_tags", lambda city=None: [
        {"name": "Art Museum", "tags": ["art"], "rating": 4.0, "price": 1.0, "city": "X", "type": "museum"},
        {"name": "History Museum", "tags": ["history"], "rating": 5.0, "price": 0.0, "city": "X", "type": "museum"},
    ])

    res = clio.generate_recommendations({"username": "ashleyfong", "city": "Detroit", "top_k": 5})
    assert res["success"] is True
    assert len(res["recommendations"]) > 0

def test_generate_recommendations_missing_username():
    res = clio.generate_recommendations({"city": "Liberty"})
    assert res["success"] is False