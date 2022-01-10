import psycopg2

class User:
	
	def get_user(self, conn) -> list:
		data = []
		try:
			psql_command = "SELECT * FROM users"
			cur = conn.cursor()
			cur.execute(psql_command)
			row = cur.fetchone()
			for i in range(cur.rowcount):
				data.append(row[0])
				row = cur.fetchone()
				cur.close()

		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

		return data

	def create_user(self, conn, user_name):
		psql_insert_command = """INSERT INTO users (user_name)
									VALUES (%s);"""
		try:
			cur = conn.cursor()
			cur.execute(psql_insert_command, (user_name,))
			conn.commit()
			cur.close()

		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
