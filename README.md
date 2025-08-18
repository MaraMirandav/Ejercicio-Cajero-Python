# Cajero en Python

Proyecto desarrollado durante el tercer trimestre del **primer curso del Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM)**, como parte del módulo optativo de **Programación en Python**.

## Objetivo

El propósito de este ejercicio es implementar en Python la lógica fundamental de un cajero automático, para realizar las siguientes operaciones: 
- Creación del banco
- Consulta de saldo
- Ingresos de dinero
- Retiro en efectivo
- Tranferencias de fondos
- Realización de compras
- Cambio de banco
    
Este proyecto refuerza conceptos como:
- Estructuras básicas de programación (bucles, condicionales)
- Programación Orientada a Objetos (POO)
- Manejo de funciones y excepciones
- Uso de bases de datos para manipulación y almacenamiento de la información.
- Implementación del patrón DAO (Data Access Object)
- Buenas prácticas en la escritura de código.

## Estructura del repositorio

- - `db_util.py`: Define la conexión a la base de datos mediante un método estático utilizando **mysql.connector**.  
- `creacion_database.py`: Contiene los métodos para la creación de las bases de datos (correspondientes a cada banco) y de la tabla **Cajero**, con sus respectivos atributos.  
- `CuentaBancaria.py`: Clase principal que representa una **Cuenta Bancaria** (POO).  
- `CuentaBancariaDAO.py`: Clase abstracta con la definición de los métodos necesarios para la gestión del sistema (crear banco, ingresar dinero, realizar compras, etc.).  
- `CuentaBancariaDAOImplementacion.py`: Implementación de los métodos definidos en `CuentaBancariaDAO.py`, integrando lógica de programación y la interacción con la base de datos. 
- `main.py`: Archivo principal que gestiona la interacción con el usuario y coordina todas las operaciones del cajero.

## Requisitos

- **Python 3.12.6**.  
- Editor de código como **VSCode**, **PyCharm** o similar.  

## Nota

- Las directrices iniciales del ejercicio fueron establecidas por el profesor de la asignatura.  
- La decisión de implementar el patrón **DAO** fue personal, para mantener un proyecto más ordenado, modular y cercano a prácticas reales.  
- Este repositorio tiene fines **educativos** y refleja mi progreso en el aprendizaje de Python durante el primer curso de DAM.  

## Reflexión sobre el aprendizaje adquirido

Este proyecto no fue únicamente un trabajo académico: también representó una forma de documentar mi aprendizaje y evolución como futura programadora.  
Me permitió aplicar de manera práctica los conocimientos adquiridos en el módulo de Python y, al mismo tiempo, conectar con lo aprendido en otras asignaturas como Bases de Datos.  

Al inicio, el desarrollo del cajero parecía complejo, ya que las directrices eran generales y había libertad para abordarlo según mi propio criterio. Para avanzar, dividí el trabajo en pequeños pasos: primero la conexión y creación de bases de datos y tablas, luego las clases y finalmente la implementación del patrón DAO.  
Elegí este enfoque porque lo considero más cercano a la realidad laboral y una forma ordenada de gestionar el proyecto.  

Gracias a este ejercicio:  
- Aprendí a manejar excepciones de forma consciente.  
- Reforcé la lógica de programación, implementándola en un proyecto más grande.  
- Descubrí la importancia de estructurar el código con buenas prácticas desde el inicio, organizándolo de manera modular y clara.
- Desarrollé habilidades en la gestión de bases de datos, aplicándolas directamente a través de la programación y comprendiendo mejor como se integran ambas para el funcionamiento del programa.
- Este proyecto me motivó a seguir mejorando mis habilidades, a tomar decisiones y me acercó un poco más a lo que será el trabajo en un contexto real.
