# Cajero en Python

Proyecto desarrollado durante el tercer trimestre del **primer curso del Grado Superior en Desarrollo de Aplicaciones Multiplataforma (DAM)**, como parte del módulo optativo de **Programación en Python**.

## Objetivo

Implementar en Python un sistema de gestión de cajeros automáticos que utiliza una base de datos **MySQL**. Cada "banco" es representado por una base de datos independiente, permitiendo operaciones como:

- Consulta de saldo y desglose de billetes/monedas.
- Ingreso de dinero.
- Realización de compras y cálculo del cambio.
- Transferencia de fondos entre diferentes bancos (bases de datos).
- Creación y selección de bancos dinámicamente.

Este proyecto refuerza conceptos de programación orientada a objetos, patrón de diseño DAO (Data Access Object), manejo de transacciones SQL, y la interacción entre Python y bases de datos.

## Estructura del proyecto

- `Main.py`: Punto de entrada de la aplicación. Contiene el menú interactivo para el usuario.
- `creacion_database.py`: Gestiona la creación de la base de datos (banco) y la tabla `Cajero`.
- `CuentaBancariaDAOImplementacion.py`: Implementación del patrón DAO. Contiene toda la lógica de negocio y las operaciones contra la base de datos.
- `db_util.py`: (No incluido en el contexto) Utilidad para gestionar la conexión a la base de datos.
- `CuentaBancaria.py` y `CuentaBancariaDAO.py`: (No incluidos en el contexto) Definen la clase del modelo y la interfaz del DAO, respectivamente.

## Requisitos

- **MySQL Server**.
- Biblioteca de Python: `mysql-connector-python`. Puedes instalarla con:

  ```bash
  pip install mysql-connector-python
  ```

## Cómo usar

  1. **Clona** este repositorio.
  2. **Configura la conexión** a tu base de datos MySQL en el archivo `db_util.py` (asegúrate de que el usuario tiene permisos para crear bases de datos).
  3. **Ejecuta** el script principal desde tu terminal para iniciar el programa:

  ```bash
    python Main.py
  ```

## Nota

La estructura del ejercicio han sido establecidas por el profesor de la asignatura como parte de la formación académica.
Este repositorio tiene fines **educativos** y refleja el progreso en el aprendizaje de Python durante el primer curso de DAM.

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
