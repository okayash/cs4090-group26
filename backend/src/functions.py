from search import recommend


try:
	from .data_access import create_user as db_create_user
except ImportError:
	from data_access import create_user as db_create_user

try:
	from .data_access import delete_user as db_delete_user
except Exception:
	try:
		from data_access import delete_user as db_delete_user
	except Exception:
		db_delete_user = None	
try:
    from .data_access import get_attraction_details as db_get_attraction_details
except ImportError:
    from data_access import get_attraction_details as db_get_attraction_details

try:
    from .data_access import list_attractions as db_list_attractions
except ImportError:
    from data_access import list_attractions as db_list_attractions

try:
    from .data_access import update_user_interests as db_update_user_interests
except ImportError:
    from data_access import update_user_interests as db_update_user_interests


def create_user(payload) -> dict:
	'''
	create new user - use case 4
	'''
	required = ["username", "first_name", "last_name"]
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
    
try:
    from .data_access import get_user_interest_names as db_get_user_interest_names
    from .data_access import get_attractions_with_tags as db_get_attractions_with_tags
except ImportError:
    from data_access import get_user_interest_names as db_get_user_interest_names
    from data_access import get_attractions_with_tags as db_get_attractions_with_tags


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
