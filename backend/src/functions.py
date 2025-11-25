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