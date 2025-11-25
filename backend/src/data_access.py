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
		try:
			cur.close()
		except Exception:
			pass
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
		try:
			cur.close()
		except Exception:
			pass
		conn.close()
