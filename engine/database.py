import psycopg2


class Database:
    def __init__(self, dbname, username, password, host):
        self.connect = psycopg2.connect(
            host=host,
            database=dbname,
            user=username,
            password=password
        )
        self.cursor = self.connect.cursor()

    def execute(self, entity):
        SQL = "SELECT object FROM yagofacts WHERE subject = (%s);"
        data = (entity,)
        self.cursor.execute(SQL, data)
        return self.cursor.fetchall()
