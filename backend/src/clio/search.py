'''
searching logic for retrieving attractions
'''

class SearchService:
    def search_by_name(name: str) -> list:
        '''
    search attractions by name
        '''
        temp = []
        # need to implement this
        return temp
    def search_by_type(type: str) -> list:
        '''
    search attractions by name
        '''
        temp = []
        # need to implement this
        return temp

def _score_attraction(user_interests: list[str], attraction_tags: list[str]) -> int:
    ui = set(x.strip().lower() for x in user_interests if x)
    at = set(x.strip().lower() for x in attraction_tags if x)
    return len(ui & at)


def recommend(attractions: list[dict], user_interests: list[str], top_k: int = 10) -> list[dict]:
    scored = []
    for a in attractions:
        score = _score_attraction(user_interests, a.get("tags", []))
        if score > 0:
            scored.append({**a, "score": score})

    # sort: score desc, rating desc (None-safe)
    scored.sort(key=lambda x: (x["score"], x["rating"] or 0), reverse=True)
    return scored[:top_k]

def recommend(attractions: list[dict], interests: list[str], top_k: int = 10) -> list[dict]:
    interests_set = {i.strip().lower() for i in (interests or []) if str(i).strip()}

    scored = []
    for a in attractions:
        tags = {t.strip().lower() for t in (a.get("tags") or []) if str(t).strip()}
        overlap = len(interests_set & tags)
        rating = a.get("rating")
        rating = float(rating) if rating not in (None, "") else 0.0

        score = overlap * 10 + rating 
        scored.append((score, overlap, rating, a))
    scored.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)

    results = []
    for (score, overlap, rating, a) in scored[:top_k]:
        out = dict(a)
        out["match_score"] = overlap
        out["match_reason"] = (
            f"Matched {overlap} interest tag(s)" if interests_set else "Popular in this area"
        )
        results.append(out)
    return results
