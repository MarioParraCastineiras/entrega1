import mysql

class DataBaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.mydb = None

    def get_connection(self): #para que no sea bloqueante
        if self.mydb is None:
            self.mydb=mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        return self.mydb