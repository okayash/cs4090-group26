from clio.search import recommend

def test_recommend_respects_top_k():
    attractions = [
        {"name": "A", "tags": ["art"], "rating": 4.0},
        {"name": "B", "tags": ["history"], "rating": 5.0},
        {"name": "C", "tags": ["science"], "rating": 3.0},
    ]
    recs = recommend(attractions, ["art", "history"], top_k=2)
    assert len(recs) == 2

def test_recommend_prefers_more_overlap():
    attractions = [
        {"name": "Low", "tags": ["art"], "rating": 5.0},
        {"name": "High", "tags": ["art", "history"], "rating": 1.0},
    ]
    recs = recommend(attractions, ["art", "history"], top_k=2)
    assert recs[0]["name"] == "High"
    assert recs[0]["match_score"] >= recs[1]["match_score"]

def test_recommend_handles_empty_interests():
    attractions = [{"name": "A", "tags": ["art"], "rating": 4.0}]
    recs = recommend(attractions, [], top_k=10)
    assert len(recs) == 1
    assert "match_reason" in recs[0]