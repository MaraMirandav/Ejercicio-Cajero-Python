class CuentaBancaria:
    #Constructor
    def __init__(self,nombre_banco:str,moneda:float, cantidad:int):
        self.__nombre_banco = nombre_banco
        self.__moneda = moneda
        self.__cantidad = cantidad

#Setter y Getter
    @property
    def nombre_banco(self) -> str:
        return self.__nombre_banco

    @nombre_banco.setter
    def nombre_banco(self,nombre_banco) -> None:
        self.__nombre_banco = nombre_banco

    @property
    def moneda(self) -> float:
        return self.__moneda

    @moneda.setter
    def moneda(self,moneda) -> None:
        self.__moneda = moneda

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self,cantidad) -> None:
        self.__cantidad = cantidad


