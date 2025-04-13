from mysql.connector import connect, Error, MySQLConnection
from db_util import DBUtil

class CreacionDatabase:
    #Metodo para crear la base de datos
    def create_database(self,schema_name:str) -> None:
        try:
            conn = DBUtil.get_connection()
            cursor = conn.cursor() #creación del cursor afuera para reutilizarlo

            #En caso de que exista la base de datos -> Use
            if self.bases_datos_existe(schema_name, conn):
                print(f"\nBanco {schema_name} seleccionado con éxito")
                use_database_query :str = f"USE {schema_name}"
                cursor.execute(use_database_query)

                if self.tabla_cajero_existe(schema_name,conn):
                    print("Tabla Cajero seleccionada con éxito")
                else:
                    self.create_table_cajero(conn)
                    print("Tabla Cajero creada con éxito")
            else:
            #En caso de que no exista la base de datos -> Create Database + USE
                create_database_query :str = f"CREATE DATABASE IF NOT EXISTS {schema_name}"
                cursor.execute(create_database_query)
                print(f"\nBanco {schema_name} creado con éxito")

                use_database_query :str = f"USE {schema_name}"
                cursor.execute(use_database_query)
                self.create_table_cajero(conn)
                print("\Tabla Cajero creada con éxito")
        except Error as e:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    #Metodo boolean para poder ver si está la base de datos
    def bases_datos_existe(self,schema_name:str, conn:MySQLConnection) -> bool:
        existe :bool = False
        select_query :str = "SELECT COUNT(schema_name) " \
                        "FROM INFORMATION_SCHEMA.SCHEMATA " \
                        "WHERE schema_name = %s"

        try:
            cursor = conn.cursor()
            cursor.execute(select_query,(schema_name,))
            result = cursor.fetchone()

            if result and result[0] > 0:
                existe = True
        except Error as e:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()

        return existe


    #Metodo boolean para poder ver si está la base de datos
    def tabla_cajero_existe(self,schema_name:str, conn:MySQLConnection) -> bool:
        existe :bool = False
        select_query :str = "SELECT table_name " \
                        "FROM INFORMATION_SCHEMA.TABLES " \
                        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'Cajero'"
        try:
            cursor = conn.cursor()
            cursor.execute(select_query,(schema_name,))
            result = cursor.fetchone()

            if result: #Si fetchone() devuelve algo, existe
                existe = True
        except Error as e:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()


        return existe

    #Metodo para crear la tabla cajero
    def create_table_cajero(self,conn:MySQLConnection) -> None:
        create_table_query :str = "CREATE TABLE Cajero (" \
                                    "Moneda DECIMAL(10,2) PRIMARY KEY," \
                                    "Cantidad INT NOT NULL" \
                                    ")"
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            self.insertar_datos(conn)
        except Error as e:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()


    #Metodo para insertar datos en la tabla cajero
    def insertar_datos(self,conn:MySQLConnection) -> None:
        datos_cajero:dict[float,int] = self.obtener_datos()
        insert_query :str = "INSERT INTO Cajero (Moneda, Cantidad) VALUES (%s, %s)"
        try:
            cursor = conn.cursor()
            for moneda,cantidad in datos_cajero.items():
                try:
                    cursor.execute(insert_query,(moneda, cantidad))
                except Error as e:
                    print(f"Error al ingresar moneda {moneda:.2f} € y cantidad {cantidad}: {e}")
            conn.commit()
        except Error as error:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()


    #Método para obtener datos que se insertarán en la tabla
    def obtener_datos(self) -> dict[float,int]:
        unidades :int = [5, 2 ,1] #unidades de moneda
        cantidad : int = 0 #Cantidad inicial
        dict_datos_cajero :dict[float, int] = {} #Diccionario para almacenar los datos

        for i in range(-2, 3):
            for j in unidades:
                moneda = (j * (10**i))
                dict_datos_cajero[moneda] = cantidad

        return dict_datos_cajero
