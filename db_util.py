from mysql.connector import connect, Error, MySQLConnection

class DBUtil:
    HOST :str = 'localhost'
    USER :str = 'root'
    PASSWORD :str = ''

    @staticmethod
    def get_connection() -> MySQLConnection | None:
        connection = None
        try:
            connection = connect(
                host = DBUtil.HOST,
                user = DBUtil.USER,
                password = DBUtil.PASSWORD)
            #print("Conexión a MySQL establecida")
        except Error as e:
            print(f"Error '{e}'")
        return connection