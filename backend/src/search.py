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
