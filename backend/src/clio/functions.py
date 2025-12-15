from .search import recommend

from .data_access import (
    validate_user_credentials as db_validate_user_credentials,
    create_user as db_create_user,
    delete_user as db_delete_user,
    get_attraction_details as db_get_attraction_details,
    list_attractions as db_list_attractions,
    update_user_interests as db_update_user_interests,
    get_user_interest_names as db_get_user_interest_names,
    get_attractions_with_tags as db_get_attractions_with_tags, 
    list_interests as db_list_interests,
    save_recommendations as db_save_recommendations,
    list_saved_recommendations as db_list_saved_recommendations
)


def validate_user_credentials(username: str, password: str) -> bool:
    if not username or not password:
        return False

    try:
        return db_validate_user_credentials(username, password)
    except Exception:
        return False

def create_user(payload) -> dict:
    required = ["username", "first_name", "last_name", "password"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return {"success": False, "user_id": None, "error": f"missing fields: {', '.join(missing)}"}

    age = payload.get("age")
    if age is not None and age != "":
        try:
            age = int(age)
        except Exception:
            return {"success": False, "user_id": None, "error": "age must be an integer"}

    user_data = {
        "username": payload.get("username"),
        "first_name": payload.get("first_name"),
        "last_name": payload.get("last_name"),
        "email": payload.get("email"),
        "age": age,
        "home_city": payload.get("home_city"),
        "password": payload.get("password"), 
    }

    try:
        created_id = db_create_user(user_data)
        return {"success": True, "user_id": created_id, "error": None}
    except Exception as e:
        return {"success": False, "user_id": None, "error": str(e)}


def delete_user(payload) -> dict:
	'''
	delete user - use case 11
	'''
	if not payload:
		return {"success": False, "error": "error"}

	username = payload.get("username")
	if not username:
		return {"success": False, "error": "Please provide username to delete."}

	try:
		result = db_delete_user({"username": username})
		return {"success": True, "result": result, "error": None}
	except Exception as e:
		return {"success": False, "error": str(e)}
	
def get_attraction_details(payload) -> dict:
    '''
    get attraction details - use case 1
    '''
    if not payload:
        return {"success": False, "attraction": None, "error": "error"}
    
    attraction_id = payload.get("attraction_id")
    if not attraction_id:
        return {"success": False, "attraction": None, "error": "Please provide an attraction ID."}
    
    try:
        attraction = db_get_attraction_details({"attraction_id": attraction_id})
        if not attraction:
            return {"success": False, "attraction": None, "error": "Attraction not found"}
        return {"success": True, "attraction": attraction, "error": None}
    except Exception as e:
        return {"success": False, "attraction": None, "error": str(e)}


def list_attractions(payload) -> dict:
    '''
    list attractions - use case 3
    '''
    city = payload.get("city") if payload else None
    
    try:
        attractions = db_list_attractions({"city": city})
        return {"success": True, "attractions": attractions, "error": None}
    except Exception as e:
        return {"success": False, "attractions": [], "error": str(e)}


def update_user_interests(payload) -> dict:
    '''
    update user interests - use case 4
    '''
    if not payload:
        return {"success": False, "result": None, "error": "error"}
    
    username = payload.get("username")
    interests = payload.get("interests")
    
    if not username:
        return {"success": False, "result": None, "error": "Please provide a username."}
    
    if not interests or not isinstance(interests, list):
        return {"success": False, "result": None, "error": "Please provide a list of interests."}
    
    try:
        result = db_update_user_interests({"username": username, "interests": interests})
        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "result": None, "error": str(e)}


def generate_recommendations(payload) -> dict:
    if not payload:
        return {"success": False, "recommendations": [], "error": "Missing payload"}

    username = payload.get("username")
    city = payload.get("city")
    top_k = payload.get("top_k", 10)

    if not username:
        return {"success": False, "recommendations": [], "error": "Missing username"}

    try:
        top_k = int(top_k)
    except Exception:
        top_k = 10

    try:
        interests = db_get_user_interest_names(username)
        attractions = db_get_attractions_with_tags(city=city)

        recs = recommend(attractions, interests, top_k=top_k)

        if not recs:
            return {
                "success": True,
                "recommendations": [],
                "error": None,
                "message": "No matches found. Add more interests or remove filters."
            }

        return {"success": True, "recommendations": recs, "error": None}
    except Exception as e:
        return {"success": False, "recommendations": [], "error": str(e)}

def generate_recommendations(payload) -> dict:
    if not payload:
        return {"success": False, "recommendations": [], "error": "Missing payload"}

    username = payload.get("username")
    city = payload.get("city")
    top_k = payload.get("top_k", 10)

    if not username:
        return {"success": False, "recommendations": [], "error": "Missing username"}

    try:
        top_k = int(top_k)
    except Exception:
        top_k = 10

    try:
        interests = db_get_user_interest_names(username)              # list[str]
        attractions = db_get_attractions_with_tags(city=city)         # location filtered

        recs = recommend(attractions, interests, top_k=top_k)      # interest scoring

        return {"success": True, "recommendations": recs, "error": None}
    except Exception as e:
        return {"success": False, "recommendations": [], "error": str(e)}

def list_interests() -> dict:
    '''
    Service: returns [{'interest_id': 1, 'name': 'Art'}, ...]
    '''
    try:
        interests = db_list_interests()
        return {"success": True, "interests": interests, "error": None}
    except Exception as e:
        return {"success": False, "interests": [], "error": str(e)}


def get_user_interest_names(username: str) -> dict:
    '''
    Service: returns ['Art', 'History', ...]
    '''
    if not username:
        return {"success": False, "interest_names": [], "error": "Missing username"}

    try:
        names = db_get_user_interest_names(username)
        return {"success": True, "interest_names": names, "error": None}
    except Exception as e:
        return {"success": False, "interest_names": [], "error": str(e)}

def save_recommendations(payload) -> dict:
    username = payload.get("username")
    recs = payload.get("recommendations")

    if not username:
        return {"success": False, "error": "Missing username"}
    if not isinstance(recs, list):
        return {"success": False, "error": "Missing recommendations list"}

    try:
        result = db_save_recommendations(username, recs)
        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "error": str(e)}

    
def list_saved_recommendations(payload) -> dict:
    username = payload.get("username")
    if not username:
        return {"success": False, "recommendations": [], "error": "Missing username"}

    try:
        recs = db_list_saved_recommendations(username)
        return {"success": True, "recommendations": recs, "error": None}
    except Exception as e:
        return {"success": False, "recommendations": [], "error": str(e)}  
