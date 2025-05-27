import mysql.connector

class DatabaseConnection:
    def __init__(self, host='localhost', user='root', password='', database='sipadtei_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()