import os
from .db import get_conn


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

def list_interests() -> list[dict]:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT interest_id, name FROM Interests ORDER BY name")
        return [{"interest_id": r[0], "name": r[1]} for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()

def update_user_interests(payload) -> dict:
    '''

    '''
    username = payload.get("username")
    interests = payload.get("interests")

    if not username:
        raise ValueError("Missing username")
    if not isinstance(interests, list):
        raise ValueError("Interests must be a list of interest_ids")

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM User_Interests_Map WHERE username = %s", (username,))

        for interest_id in interests:
            cur.execute(
                "INSERT INTO User_Interests_Map (username, interest_id) VALUES (%s, %s)",
                (username, int(interest_id)),
            )

        conn.commit()
        return {"updated": len(interests)}
    finally:
        cur.close()
        conn.close()


def get_user_interest_names(username: str) -> list[str]:
    '''

    '''
    if not username:
        return []

    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = '''
            SELECT i.name
            FROM User_Interests_Map uim
            JOIN Interests i ON i.interest_id = uim.interest_id
            WHERE uim.username = %s
            ORDER BY i.name
        '''
        cur.execute(sql, (username,))
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()
          
		
def get_attraction_details(payload) -> dict:
    attraction_name = payload.get("name")
    if not attraction_name:
        raise ValueError("Please provide an attraction name.")

    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = '''
            SELECT
                a.name, a.`type`, a.city, a.price, a.rating,
                GROUP_CONCAT(DISTINCT t.tag_name ORDER BY t.tag_name SEPARATOR ',') AS tags
            FROM Attractions a
            LEFT JOIN Attraction_Tags_Map atm ON atm.attraction_name = a.name
            LEFT JOIN Attraction_Tags t ON t.tag_id = atm.tag_id
            WHERE a.name = %s
            GROUP BY a.name, a.`type`, a.city, a.price, a.rating
        '''
        cur.execute(sql, (attraction_name,))
        row = cur.fetchone()
        if not row:
            return {}

        name, typ, city, price, rating, tags = row
        return {
            "name": name,
            "type": typ,
            "city": city,
            "price": price,
            "rating": rating,
            "tags": tags.split(",") if tags else []
        }
    finally:
        cur.close()
        conn.close()

def list_cities() -> list[str]:
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT city FROM Attractions ORDER BY city")
        return [r[0] for r in cur.fetchall()]
    finally:
        cur.close()
        conn.close()


def list_attractions(payload) -> list:
    city = (payload.get("city") or "").strip()

    sql = '''
        SELECT
            a.id, a.name, a.`type`, a.city, a.price, a.rating,
            GROUP_CONCAT(DISTINCT t.tag_name ORDER BY t.tag_name SEPARATOR ',') AS tags
        FROM Attractions a
        LEFT JOIN Attraction_Tags_Map atm ON atm.attraction_name = a.name
        LEFT JOIN Attraction_Tags t ON t.tag_id = atm.tag_id
    '''
    params = ()

    if city:
        city = city.replace(",", " ").replace(".", " ")
        city = " ".join(city.split())
        sql += " WHERE LOWER(a.city) LIKE LOWER(%s) "
        params = (f"%{city}%",)

    sql += '''
        GROUP BY a.id, a.name, a.`type`, a.city, a.price, a.rating
        ORDER BY a.rating DESC
    '''

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        out = []
        for (id_, name, typ, city_val, price, rating, tags) in cur.fetchall():
            out.append({
                "id": id_,
                "name": name,
                "type": typ,
                "city": city_val,
                "price": price,
                "rating": rating,
                "tags": (tags.split(",") if tags else []),
            })
        return out
    finally:
        cur.close()
        conn.close()


def get_attractions_with_tags(city: str | None = None) -> list[dict]:
    conn = get_conn()
    try:
        cur = conn.cursor()

        sql = '''
            SELECT 
                a.id, a.name, a.`type`, a.city, a.price, a.rating,
                GROUP_CONCAT(DISTINCT t.tag_name ORDER BY t.tag_name SEPARATOR ',') AS tags
            FROM Attractions a
            LEFT JOIN Attraction_Tags_Map atm ON atm.attraction_name = a.name
            LEFT JOIN Attraction_Tags t ON t.tag_id = atm.tag_id
        '''
        params = []

        if city:
            city = city.replace(",", " ").replace(".", " ")
            city = " ".join(city.split())

            sql += " WHERE LOWER(a.city) LIKE LOWER(%s) "
            params.append(f"%{city}%")

        sql += " GROUP BY a.id, a.name, a.`type`, a.city, a.price, a.rating "

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()

        out = []
        for (id_, name, typ, city_val, price, rating, tags) in rows:
            tag_list = [x.strip().lower() for x in tags.split(",")] if tags else []
            out.append({
                "id": id_,
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
        
def save_recommendations(username: str, recommendations: list[dict]) -> dict:
    '''
    '''
    if not username:
        raise ValueError("No username")

    conn = get_conn()
    try:
        cur = conn.cursor()

        sql = '''
            INSERT INTO Recommendations (username, attraction_name, reason)
            VALUES (%s, %s, %s)
        '''

        saved = 0
        for r in recommendations:
            attraction_name = r.get("name")
            if not attraction_name:
                continue
            reason = r.get("match_reason") or r.get("reason") or "Recommended based on your interests"
            cur.execute(sql, (username, attraction_name, reason))
            saved += 1

        conn.commit()
        return {"saved": saved}
    finally:
        cur.close()
        conn.close()
        
def list_saved_recommendations(username: str) -> list[dict]:
    if not username:
        return []

    conn = get_conn()
    try:
        cur = conn.cursor()
        sql = '''
            SELECT recommendation_id, attraction_name, reason
            FROM Recommendations
            WHERE username = %s
            ORDER BY recommendation_id DESC
            LIMIT 100
        '''
        cur.execute(sql, (username,))
        rows = cur.fetchall()

        return [
            {"recommendation_id": r[0], "name": r[1], "reason": r[2]}
            for r in rows
        ]
    finally:
        cur.close()
        conn.close()
