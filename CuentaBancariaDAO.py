from abc import ABC, abstractmethod
from CuentaBancaria import CuentaBancaria
from creacion_database import CreacionDatabase

class CuentaBancariaDAO(ABC):
    @abstractmethod
    def crear_database(self, nombre_banco: str) -> None:
        pass

    @abstractmethod
    def listar_dinero(self, banco:CuentaBancaria) -> None:
        pass

    @abstractmethod
    def mostrar_total_cuenta(self, banco:CuentaBancaria) -> None:
        pass

    @abstractmethod
    def realizar_compra(self, banco:CuentaBancaria, monto_pagar:float, monto_pagado:str) -> None:
        pass

    @abstractmethod
    def introducir_dinero_cuenta(self, banco:CuentaBancaria, monto_ingresar:str) -> None:
        pass

    @abstractmethod
    def transferir_fondos(self, banco:CuentaBancaria, otro_banco:CuentaBancaria, monto_transferir:str) -> None:
        pass

    @abstractmethod
    def cambiar_banco(self, otro_banco:CuentaBancaria) -> None:
        pass