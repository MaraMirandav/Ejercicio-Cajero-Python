from random import shuffle

# generar info rapido
lista = [1,2,3,4,5,6,7,8,9,10]
lista_lc = [i for i in range(1,101)]

# lc anidados
lista_money = [(j*10**i) for i in range(-2, 3) for j in (1, 2, 5)]

# Generador
lista_money_generator = ((j*10**i) for i in range(-2, 3) for j in (1, 2, 5))

hola = 1
# print(lista)
# print(lista_lc)
# print(lista_money)

# dictionary comprehensions
dict_cm = {k: 0 for k in lista_money_generator}

# for k, v in dict_cm.items():
#     print(k, '€ - ', v)


class XD:
    LISTA_MONEY_GENERATOR = ((j*10**i) for i in range(-2, 3) for j in (1, 2, 5))
    
    @staticmethod
    def crear_monedero() -> dict[float, int]:
        monedero_auxiliar: dict[float, int] = {k: 0 for k in XD.LISTA_MONEY_GENERATOR}
        return monedero_auxiliar

lista_nombres = ['Mimis', 'ikis', 'jimmys']
lista_apellidos = ['Miranda', 'Ovalle', 'Barrera', 'Villablanca']

lista_names = [(i, j, h) for i in lista_nombres for j in lista_apellidos for h in lista_apellidos]

for i, j, k in lista_names:
    print(i, j, k)
