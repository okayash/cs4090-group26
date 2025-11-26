import os
import mysql.connector


def _get_conn():
	'''
	get conn change details
	'''
	return mysql.connector.connect(
		host=os.getenv("DB_HOST", "127.0.0.1"),
		user=os.getenv("DB_USER", "root"),
		password=os.getenv("DB_PASSWORD", ""),
		database=os.getenv("DB_NAME", "test"),
	)


def create_user(data) -> str:
	'''
	create user - use case 4
	'''
	username = data.get("username")
	if not username:
		raise ValueError("Please input a username.")

	sql = (
		"INSERT INTO User (username, first_name, last_name, email, age, home_city) "
		"VALUES (%s, %s, %s, %s, %s, %s)"
	)
	params = (
		username,
		data.get("first_name"),
		data.get("last_name"),
		data.get("email"),
		data.get("age"),
		data.get("home_city"),
	)

	conn = _get_conn()
	try:
		cur = conn.cursor()
		cur.execute(sql, params)
		conn.commit()
		return username
	finally:
		cur.close()
		conn.close()


def delete_user(payload) -> dict:
	'''
	delete user - use case 11
	'''
	username = payload.get("username")

	if not username:
		raise ValueError("Please enter username to delete.")

	sql = "DELETE FROM User WHERE username = %s"
	params = (username,)

	conn = _get_conn()
	try:
		cur = conn.cursor()
		cur.execute(sql, params)
		conn.commit()
		return {"deleted": cur.rowcount}
	finally:
		cur.close()
		conn.close()

		
def get_attraction_details(payload) -> dict:
	'''
	get attraction details - use case 1
	'''
	attraction_id = payload.get("attraction_id")
	if not attraction_id:
		raise ValueError("Please provide an attraction ID.")

	sql = "SELECT id, name, type, city, tags, price, rating FROM Attractions WHERE id = %s"
	params = (attraction_id,)

	conn = _get_conn()
	try:
		cur = conn.cursor()
		cur.execute(sql, params)
		result = cur.fetchone()
		if result:
			(id, name, type, city, tags, price, rating) = result
			attraction = {
				"id": id,
				"name": name,
				"type": type,
				"city": city,
				"tags": tags,
				"price": price,
				"rating": rating
			}
			return attraction
		else:
			return {}
	finally:
		cur.close()
		conn.close()


def list_attractions(payload) -> list:
	'''
	list attractions - use case 3
	'''
	city = payload.get("city")

	sql = "SELECT id, name, type, city, tags, price, rating FROM Attractions"
	params = ()

	if city:
		sql += " WHERE city = %s"
		params = (city,)

	conn = _get_conn()
	try:
		cur = conn.cursor()
		cur.execute(sql, params)
		results = []
		for (id, name, type, city, tags, price, rating) in cur:
			attraction = {
				"id": id,
				"name": name,
				"type": type,
				"city": city,
				"tags": tags,
				"price": price,
				"rating": rating
			}
			results.append(attraction)
		return results
	finally:
		cur.close()
		conn.close()

		
def update_user_interests(payload) -> dict:
	'''
	update user interests - use case 4
	'''
	username = payload.get("username")
	interests = payload.get("interests")
	if not username:
		raise ValueError("Please provide a username.")
	if not interests or not isinstance(interests, list):
		raise ValueError("Please provide a list of interests.")

	sql_delete = "DELETE FROM User_Interests_Map WHERE username = %s"
	sql_insert = "INSERT INTO User_Interests_Map (username, interest_id) VALUES (%s, %s)"
	
	conn = _get_conn()
	try:
		cur = conn.cursor()
		cur.execute(sql_delete, (username,))
		for interest in interests:
			cur.execute(sql_insert, (username, interest))
		conn.commit()
		return {"updated": len(interests)}
	finally:
		cur.close()
		conn.close()