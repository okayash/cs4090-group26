import clio.functions as clio

def test_create_user_missing_fields():
    res = clio.create_user({"username": "", "first_name": "Ashley", "last_name": "Fong"})
    assert res["success"] is False

def test_update_user_interests_rejects_bad_payload():
    res = clio.update_user_interests({"username": "", "interests": []})
    assert res["success"] is False