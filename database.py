import psycopg2
import config
"""

    MSOBOT - Database Sınıfı

"""
class Database():
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='"+config.DATABASE+"' user='"+config.USER+
                "' host='"+config.HOST+"' password='"+config.PASSWORD+
                "' port='"+config.PORT+"'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            #print("Veritabanı bağlantısı gerçekleşti.")
        except:
            print("Veritabanı bağlantısı yapılamadı.")

    def server_insert(self, data):
        sorgu = "INSERT INTO servers(server_id, name) VALUES('"+data[0]+"', '"+data[1]+"')"
        self.cursor.execute(sorgu)

    def server_query_all(self):
        self.cursor.execute("SELECT * FROM servers")
        return self.cursor.fetchall()

    def uye_insert(self, data):
        sorgu = "INSERT INTO members(member_id, name, server_id) VALUES ('{}', '{}', '{}')".format(data[0],
                                                                                                   data[1].replace("'", ""), data[2])
        self.cursor.execute(sorgu)

    def uye_query_all(self):
        self.cursor.execute("SELECT * FROM members")
        return self.cursor.fetchall()