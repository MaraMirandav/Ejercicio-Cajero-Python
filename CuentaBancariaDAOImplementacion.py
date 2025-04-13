from mysql.connector import connect, Error, MySQLConnection
from creacion_database import CreacionDatabase
from db_util import DBUtil

from CuentaBancaria import CuentaBancaria
from CuentaBancariaDAO import CuentaBancariaDAO

class CuentaBancariaDAOImplementacion(CuentaBancariaDAO):

    #/*----------------------------------------------------------------------------------*/

    #Método para la creación de la Base de Datos y Tabla Cajero
    def crear_database(self, nombre_banco: str) -> None:
        conexion = CreacionDatabase()
        conexion.create_database(nombre_banco)

    #/*----------------------------------------------------------------------------------*/

    #Case 1) Método para listar el dinero que se encuentra en la cuenta bancaria
    def listar_dinero(self, banco:CuentaBancaria) -> None:
        select_query:str = "SELECT Moneda, Cantidad FROM Cajero ORDER BY Moneda DESC"
        use_query:str = f"USE {banco.nombre_banco}"
        try:
            conn = DBUtil.get_connection()
            cursor = conn.cursor()

            cursor.execute(use_query)
            cursor.execute(select_query)
            result = cursor.fetchall()

            self.mostrar_total_cuenta(banco,conn)
            print("\n" + "-" * 56)
            print(f"|{"Detalle Dinero":^54}|")
            if result:
                print("-" * 56)
                print(f"|     Moneda      |     Cantidad    |       Total      |")
                print("-" * 56)

                for moneda, cantidad in result:
                    print(f"|   {moneda:11.2f}   |   {cantidad:12d}  |   € {moneda*cantidad:11.2f}  |")
                print("-" * 56)
            else:
                print(f"\nNo se encontraron registros en la cuenta de '{banco.nombre_banco}'.")

        except Error as e:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    #/*----------------------------------------------------------------------------------*/

    #Método para mostrar el total de la cuenta
    def mostrar_total_cuenta(self, banco:CuentaBancaria,conn:MySQLConnection) -> None:
        select_query:str = "SELECT SUM(Moneda * Cantidad) AS Total FROM Cajero"
        total:float = 0

        try:
            cursor = conn.cursor()
            cursor.execute(select_query)
            result = cursor.fetchone()

            if result and result[0] is not None:
                total = result[0]
                print("\n" + "-" * 38)
                print(f"|   Banco: {banco.nombre_banco:<23}   |")
                print("-" * 38)
                print(f"|   Dinero en la cuenta: € {total:2.2f}    |")
                print("-" * 38)
        except Error as e:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()

    #/*----------------------------------------------------------------------------------*/

    # Case 2) Método para realizar compras
    def realizar_compra(self, banco:CuentaBancaria, monto_pagar:float, monto_pagado:str) -> None:
        monto_pagado_compra:dict[float,int] = self.obtener_datos(monto_pagado)
        total_pagado:float = self.monto_pagado_(banco,monto_pagado_compra)

        use_query:str = f"USE {banco.nombre_banco}"

        update_query_pagar:str = "UPDATE Cajero SET Cantidad = Cantidad - %s " \
                                    "WHERE Moneda  = %s AND Cantidad >= %s"

        update_query_vuelto:str = "UPDATE Cajero SET Cantidad = Cantidad + %s " \
                                    "WHERE Moneda = %s"

        if monto_pagar > total_pagado:
            print("\n"+ "-" * 44)
            print(f"\nEl monto pagado es insuficiente. Faltan: {monto_pagar - total_pagado:.2f} €")
            print("\n"+ "-" * 44)
            return

        try:
            conn = DBUtil.get_connection()
            conn.autocommit = False
            cursor = conn.cursor()
            cursor.execute(use_query)

            print("\n"+ "-" * 44)
            for moneda,cantidad in monto_pagado_compra.items():
                if self.moneda_existe(moneda, conn):
                    cursor.execute(update_query_pagar,(cantidad,moneda,cantidad))
                    print(f"Pago realizado: moneda {moneda:.2f} €, cantidad {cantidad}")

            if self.hay_vuelto(banco,monto_pagar,monto_pagado_compra):
                vuelto:float = self.vuelto_a_entregar(banco,monto_pagar,monto_pagado_compra)
                dinero_disponible = self.datos_dinero_en_cuenta(banco,conn)
                vuelto_a_pagar:dict[float,int] = self.monto_a_pagar(banco,vuelto,dinero_disponible)

                for moneda_vuelto, cantidad_vuelto in vuelto_a_pagar.items():
                    if self.moneda_existe(moneda_vuelto,conn):
                        cursor.execute(update_query_vuelto,(cantidad_vuelto,moneda_vuelto))
                        print(f"Vuelto recibido: moneda {moneda_vuelto:.2f} €, cantidad {cantidad_vuelto}")
                print(f"\nVuelto total de la compra: {vuelto:.2f} €")
            conn.commit()
            conn.autocommit = True
        except Error as e:
            print(f"Error '{e}'")
            conn.rollback()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        print("\nPago finalizado, ¡muchas gracias!")
        print("-" * 44)

    # Método para obtener un diccionario con el dinero que tienes en el cajero
    def datos_dinero_en_cuenta(self, banco:CuentaBancaria, conn:MySQLConnection) -> dict[float, int]:
        dinero_en_cuenta:dict[float,int] = {}
        select_query:str = "SELECT Moneda, Cantidad FROM Cajero ORDER BY Moneda DESC"
        try:
            cursor = conn.cursor()
            cursor.execute(select_query)
            result = cursor.fetchall()

            for moneda, cantidad in result:
                dinero_en_cuenta[float(moneda)] = cantidad
        except Error as e:
            print(f"Error '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()

        return dinero_en_cuenta

    # Método que devuelve un diccionario con el monto A Pagar(float)
    def monto_a_pagar(self, banco:CuentaBancaria, monto_pagar:float, monto_pagado:dict[float,int]) -> dict[float, int]:
        monto_a_pagar_dict:dict[float,int] = {}
        monto_restante = monto_pagar

        for moneda, cantidad_disponible in sorted(monto_pagado.items(),reverse=True):
            if monto_restante <= 0:
                break
            moneda_float = float(moneda)
            cantidad_necesaria:int = int(monto_restante // moneda_float)
            cantidad_a_usar:int = min(cantidad_disponible,cantidad_necesaria) #valor mas pequeño
            #cantidad_a_usar:int = cantidad_disponible if cantidad_disponible < cantidad_necesaria else cantidad_necesaria

            if cantidad_a_usar > 0:
                monto_a_pagar_dict[moneda_float] = cantidad_a_usar
                monto_restante -= cantidad_a_usar * moneda
        return monto_a_pagar_dict

    # Método que devuelve un float con el monto pagado
    def monto_pagado_(self, banco:CuentaBancaria, monto_pagado:dict[float,int]) -> float:
        total_pagado:float = 0
        for moneda, cantidad in monto_pagado.items():
            total_pagado += moneda * cantidad
        return total_pagado

    # Método que devuelve un float con el vuelto
    def vuelto_a_entregar(self, banco:CuentaBancaria, monto_pagar:float, monto_pagado:dict[float,int]) -> float:
        total_pagado:float = self.monto_pagado_(banco,monto_pagado)
        if total_pagado > monto_pagar:
            vuelto:float = total_pagado - monto_pagar
            return vuelto
        return 0

    # Método que devuelve un boolean para evaluar si hay vuelto
    def hay_vuelto(self, banco:CuentaBancaria, monto_pagar:float, monto_pagado:dict[float,int]) -> bool:
        total_pagado:float = self.monto_pagado_(banco, monto_pagado)
        if total_pagado > monto_pagar:
            return True
        return False

    #/*----------------------------------------------------------------------------------*/

    # Case 3) Método para introducir dinero a la cuenta bancaria
    def introducir_dinero_cuenta(self, banco:CuentaBancaria, monto_ingresar:str) -> None:
        datos_ingresar:dict[float,int] = self.obtener_datos(monto_ingresar)
        update_query:str = "UPDATE Cajero SET Cantidad = Cantidad + %s WHERE Moneda = %s"
        use_query:str = f"USE {banco.nombre_banco}"

        try:
            conn = DBUtil.get_connection()
            conn.autocommit = False
            cursor = conn.cursor()
            cursor.execute(use_query)

            print("\n" + "-" * 44)
            for moneda, cantidad in sorted(datos_ingresar.items(),reverse=True):
                if self.moneda_existe(moneda,conn):
                    cursor.execute(update_query,(cantidad,moneda))
                    print(f"Dinero ingresado en la cuenta: moneda {moneda:.2f} €, cantidad {cantidad}")
                else:
                    print(f"Error al ingresar, moneda {moneda:.2f} € no existe")
            conn.commit()
            conn.autocommit = True
            print("-" * 44)
            self.mostrar_total_cuenta(banco,conn)
        except Error as e:
            conn.rollback()
            print(f"Error '{e}': Error al ingresar moneda {moneda:.2f} € y cantidad {cantidad}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    # Método para verificar si la moneda existe
    def moneda_existe(self, moneda:float, conn:MySQLConnection) -> bool:
        existe:bool = False
        select_query:str = "SELECT count(*) from cajero where moneda = %s"
        try:
            cursor = conn.cursor()
            cursor.execute(select_query,(moneda,))
            result = cursor.fetchone()

            if result and result[0] > 0:
                existe = True
        except Error as e:
            print(f"Error : '{e}'")
        finally:
            if conn.is_connected():
                cursor.close()

        return existe

    # Método para obtener los datos a insertar en la tabla a partir del String (#500-2#10-2)
    def obtener_datos(self, moneda_ingresar:str) -> dict[float,int]:
        dinero_ingresar:dict[float,int] = {}
        montos_completos = moneda_ingresar.split("#")

        for monto in montos_completos:
            if monto:
                partes = monto.split("-")
                if len(partes) == 2:
                    moneda:float = float(partes[0])
                    cantidad:int = int(partes[1])
                    dinero_ingresar[moneda] = cantidad

        return dinero_ingresar

    #/*----------------------------------------------------------------------------------*/
    # Case 4) Método para transferir fondos
    def transferir_fondos(self, banco:CuentaBancaria, otro_banco:CuentaBancaria, monto_transferir:str) -> None:
        datos_transferir: dict[float,int] = self.obtener_datos(monto_transferir)

        update_query_transferir:str = f"UPDATE {banco.nombre_banco}.Cajero SET Cantidad = Cantidad - %s WHERE Moneda = %s AND Cantidad >= %s"
        update_query_recibido:str = f"UPDATE {otro_banco.nombre_banco}.Cajero SET Cantidad = Cantidad + %s WHERE Moneda = %s"
        use_query_banco:str = f"USE {banco.nombre_banco}"
        use_query_otro_banco:str = f"USE {otro_banco.nombre_banco}"

        try:
            conn = DBUtil.get_connection()
            conn.autocommit = False
            cursor = conn.cursor()

            print("\n"+ "-" * 84)
            cursor.execute(use_query_banco)
            for moneda_transferir, cantidad_transferir in datos_transferir.items():
                if self.moneda_existe(moneda_transferir,conn):
                    cursor.execute(update_query_transferir,(cantidad_transferir,moneda_transferir,cantidad_transferir))
                    print(f"Transferencia realizada con éxito: moneda {moneda_transferir:.2f} €, cantidad {cantidad_transferir}")

            cursor.execute(use_query_otro_banco)
            for moneda_recibida, cantidad_recibida in datos_transferir.items():
                if self.moneda_existe(moneda_recibida,conn):
                    cursor.execute(update_query_recibido,(cantidad_recibida,moneda_recibida))
                    print(f"\nTransferencia recibida en Banco {otro_banco.nombre_banco} con éxito: moneda {moneda_recibida:.2f} €, cantidad {cantidad_recibida}")
            conn.commit()
            conn.autocommit = True
            print("-" * 84)
        except Error as e:
            print(f"Error '{e}'")
            conn.rollback()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    #/*----------------------------------------------------------------------------------*/

    # Case 5) Método para cambiar de bases de datos segun el banco
    def cambiar_banco(self, otro_banco:CuentaBancaria) -> None:
        try:
            conn = CreacionDatabase()
            conn.create_database(otro_banco.nombre_banco)
        except Error as e:
            print(f"Error : '{e}' Al cambiar al banco {otro_banco.nombre_banco()}")

    #/*----------------------------------------------------------------------------------*/