import json
from mysql.connector import pooling
import mysql.connector
class class_bd:
    def __init__(self):
        with open("./config/Settings.json") as f:
            keys = json.load(f)
        self.connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool", pool_size=10, pool_reset_session=True,
                                                      user=keys["mysql_user"], password=keys["mysql_pass"],
                                                      host=keys["mysql_host"], database='new_sports1')

    def bd(self, sql, fetch=False):
        try:
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                # get all records
                if fetch:
                    records = cursor.fetchall()
                else:
                    records = cursor.lastrowid
                connection.commit()
                print(cursor.rowcount, "Rows afetadas in query")
                cursor.close()
            else:
                print("Failed to insert record into table: not connected ")
                return None
        except mysql.connector.Error as error:
            print("Failed to insert record into table {}".format(error))
            records = None
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")
            return records