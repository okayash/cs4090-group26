import os
from db import get_conn


def validate_user_credentials(username: str, password: str) -> bool:
	'''
	
	'''
	conn = get_conn()
	try:
		cur = conn.cursor()
		sql = "SELECT username FROM User WHERE username = %s AND password = %s"
		cur.execute(sql, (username, password))
		return cur.fetchone() is not None
	finally:
		cur.close()
		conn.close()


def create_user(data) -> str:
	'''
	create user - use case 4

	'''
	username = data.get("username")
	if not username:
		raise ValueError("Please input a username.")

	sql = (
		"INSERT INTO User (username, first_name, last_name, email, age, home_city, password) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )
	params = (
		username,
		data.get("first_name"),
		data.get("last_name"),
        data.get("email"),
        data.get("age"),
        data.get("home_city"),
        data.get("password"),   
    )

	conn = get_conn()
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

	conn = get_conn()
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

	conn = get_conn()
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

	conn = get_conn()
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
	
	conn = get_conn()
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


def get_user_interest_names(username: str) -> list[str]:
    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = """
            SELECT i.name
            FROM User_Interests_Map uim
            JOIN Interests i ON i.interest_id = uim.interest_id
            WHERE uim.username = %s
        """
        cur.execute(sql, (username,))
        return [row[0] for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()


def get_attractions_with_tags(city: str | None = None) -> list[dict]:
    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = """
            SELECT 
                a.name, a.`type`, a.city, a.price, a.rating,
                GROUP_CONCAT(t.tag_name) AS tags
            FROM Attractions a
            LEFT JOIN Attraction_Tags_Map atm ON atm.attraction_name = a.name
            LEFT JOIN Attraction_Tags t ON t.tag_id = atm.tag_id
        """
        params = []
        if city:
            sql += " WHERE a.city = %s "
            params.append(city)

        sql += " GROUP BY a.name, a.`type`, a.city, a.price, a.rating "

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()

        out = []
        for (name, typ, city_val, price, rating, tags) in rows:
            tag_list = []
            if tags:
                tag_list = [x.strip().lower() for x in tags.split(",") if x.strip()]
            out.append({
                "name": name,
                "type": typ,
                "city": city_val,
                "price": price,
                "rating": rating,
                "tags": tag_list
            })
        return out
    finally:
        cur.close()
        conn.close()
