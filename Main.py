from creacion_database import CreacionDatabase
from CuentaBancaria import CuentaBancaria
from CuentaBancariaDAOImplementacion import CuentaBancariaDAOImplementacion
from os import system

OPCIONES :tuple = (
                    "1.- Listar",
                    "2.- Realizar Compra",
                    "3.- Introducir Dinero",
                    "4.- Transferir Fondos",
                    "5.- Cambiar Banco (BBDD)",
                    "6.- Salir"
                    )

#Método para generar el menú principal
def menu(schema_name:str) -> int:
    print(f"\nUsted está en la BBDD de Banco {schema_name}\n")
    for opcion in OPCIONES:
        print(opcion)
    eleccion = int(input("\nIndique la opción aquí ---> "))
    return eleccion

if __name__ == "__main__":
    #Conexion
    conexion_dao = CuentaBancariaDAOImplementacion()

    #Instancias de banco
    nombre_banco = "desconocido"
    moneda = 0
    cantidad = 0

    banco = CuentaBancaria(nombre_banco,moneda,cantidad)
    otro_banco = CuentaBancaria(nombre_banco,moneda,cantidad)

    #Ingreso del nombre del banco, creación del banco y tabla cajero
    system("clear")
    nombre_banco_actual = input("Indique el nombre de su banco: ")
    banco.nombre_banco = nombre_banco_actual
    conexion_dao.crear_database(banco.nombre_banco)

    seguir_operando: bool = True

    while(seguir_operando):
        opcion :int = menu(banco.nombre_banco)

        match opcion:
            case 1: #Listar
                system("clear")
                print("A continuación, el detalle de su cuenta bancaria:")
                conexion_dao.listar_dinero(banco)

            case 2: #Realizar Compra
                system("clear")
                monto_a_pagar:float = float(input("\nIngresa el monto total de la compra: "))
                monto_pagado:str = input("Ingresa moneda y cantidad a pagar en este formato (#500-2): ")
                conexion_dao.realizar_compra(banco,monto_a_pagar,monto_pagado)

            case 3: #Introducir dinero
                system("clear")
                dinero_a_ingresar:str = input("\nIngresa moneda y cantidad en este formato (#500-2): ")
                conexion_dao.introducir_dinero_cuenta(banco, dinero_a_ingresar)

            case 4: #Transferir Fondos
                system("clear")
                banco_a_transferir:str = input("Indique el nombre del banco a transferir: ")
                otro_banco.nombre_banco = banco_a_transferir
                monto_a_transferir:str = input("\nIngresa moneda y cantidad a transferir en este formato (#500-2): ")
                conexion_dao.transferir_fondos(banco, otro_banco,monto_a_transferir)

            case 5: #Cambiar de banco
                system("clear")
                respuesta_cambio:str = input("\n¿Está seguro/a que desea cambiar de banco? (Si / NO): ").lower()
                if respuesta_cambio == "si":
                    nombre_banco_actual:str = input("Indique el nombre de su banco: ")
                    banco.nombre_banco = nombre_banco_actual
                    conexion_dao.cambiar_banco(banco)
                else:
                    continue

            case 6: #Salir
                system("clear")
                print("\n¡Hasta pronto!")
                seguir_operando = False

            case _: #Default
                system("clear")
                print("\nDebes ingresar una opción válida, vuelve a intentarlo")
