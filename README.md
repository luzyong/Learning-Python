# Curso Integral de Python: De PCEP a PCPP


---

## Propósito del curso

Este curso está diseñado para proporcionar una formación completa y estructurada en el lenguaje de programación Python, cubriendo desde los conceptos fundamentales hasta técnicas avanzadas de desarrollo. El objetivo principal es guiar al estudiante a través de un recorrido progresivo que abarca la sintaxis básica, estructuras de control, programación orientada a objetos, manejo de archivos y bases de datos, desarrollo de interfaces gráficas, y buenas prácticas de programación según los estándares PEP.

Dirigido a programadores de todos los niveles, desde principiantes que desean iniciar su carrera en Python hasta desarrolladores experimentados que buscan profundizar en aspectos avanzados del lenguaje y prepararse para las certificaciones oficiales PCEP, PCAP y PCPP de Python Institute.

---

## Material del curso

La presentación del curso, que contiene el desarrollo completo de todos los temas, está disponible en el siguiente enlace:

[**📊 Presentación del curso - Google Slides**](https://docs.google.com/presentation/d/1jls9ETOdV9rlJOdPDa_RdPYHehHRZGObNcibX7yRW9s/edit?usp=sharing)

> **Nota:** La presentación se encuentra en constante actualización y desarrollo.

---

## Temario general

### 1. Fundamentos y Lógica de Programación
- **Introducción al lenguaje**: Intérpretes vs. compiladores, léxico, sintaxis y semántica
- **Estructura del código**: Palabras reservadas, instrucciones, comentarios e indentación
- **Literales y variables**:
  - Tipos: booleanos, enteros, flotantes (notación científica) y cadenas
  - Sistemas numéricos: binario, octal, decimal y hexadecimal
  - Convenciones de nombres y estándar PEP-8
- **Operadores y casting**:
  - Aritméticos, lógicos (not, and, or), relacionales y a nivel de bits (bitwise)
  - Prioridades y enlace (binding)
  - Conversión de tipos (casting)
- **Entrada y salida (I/O)**: Uso avanzado de print() e input()

### 2. Control de Flujo y Colecciones de Datos
- **Decisiones y ramificación**: if, if-else, if-elif-else y anidamiento
- **Bucles e iteraciones**: while, for, range(), in, break, continue y cláusulas else en bucles
- **Listas y tuplas**:
  - Indexación, slicing, mutabilidad vs. inmutabilidad
  - Métodos de lista, listas anidadas (matrices) y list comprehensions
- **Diccionarios y cadenas**:
  - Operaciones con claves/valores
  - Métodos y funciones de strings

### 3. Modularización, Funciones y Excepciones
- **Funciones y generadores**: Definición, invocación, return, recursividad y None
- **Interacción con el entorno**: Parámetros vs. argumentos, argumentos por posición y keyword, scopes (local vs. global) y shadowing
- **Módulos y paquetes**
- **Gestión de errores**:
  - Jerarquía de excepciones (ArithmeticError, LookupError, etc.)
  - Bloques try-except, propagación y delegación de responsabilidades
  - Técnicas avanzadas: Chained exceptions (_context_, __cause__) y análisis de objetos traceback

### 4. Programación Orientada a Objetos Avanzada (OOP)
- **Conceptos core**: Clases, instancias, atributos, métodos e isinstance()/issubclass()
- **Métodos mágicos (Dunder)**: Comparación, conversión, introspección y acceso a contenedores
- **Arquitectura**:
  - Herencia simple y múltiple, Method Resolution Order (MRO) y polimorfismo
  - Herencia vs. composición ("is a" vs. "has a")
  - Clases abstractas y métodos abstractos
- **Encapsulamiento y métodos especiales**: Getters, setters, deleters, @classmethod y @staticmethod
- **Metaprogramación**: Uso de la metaclasse type y atributos especiales del sistema

### 5. Funciones Avanzadas y Serialización
- **Sintaxis extendida**: Uso de *args y kwords, closures y decoradores (de función y de clase)
- **Copia de objetos**: Labels vs. identidad, copy() y deepcopy()
- **Persistencia de datos**: Serialización con pickle y almacenamiento en diccionario con shelve

### 6. Estándares, Buenas Prácticas (PEP) y Calidad
- **Filosofía Python**: PEP 1, PEP 8 (Estilo), PEP 20 (The Zen of Python)
- **Documentación**: PEP 257 (Docstrings), linters, fixers y PEP 484 (Type hints)

### 7. Desarrollo de Interfaces (GUI) y Redes
- **Programación de GUIs con Tkinter**:
  - Widgets (Button, Label, Entry, Radiobutton, Canvas)
  - Layout Managers (grid, place), geometría y colores
  - Programación dirigida por eventos: callbacks y binding
- **Programación de red**:
  - Sockets (TCP/IP), dominios, puertos y servicios
  - Clientes REST: Métodos HTTP (GET, POST, PUT, DELETE) y códigos de estado
  - Transferencia de datos: JSON y XML (procesamiento y estructura)

### 8. Archivos, Bases de Datos y Entorno
- **SQLite en Python**: Conexiones, cursores, transacciones y sentencias SQL (CRUD)
- **Procesamiento de archivos**: Lectura/escritura de CSV y parsing/construcción de XML
- **Herramientas de sistema**: Registro de eventos (logging), niveles y manejadores; archivos de configuración (.ini) con ConfigParser

---

## Ejercicios propuestos

El curso incluye una colección de ejercicios prácticos diseñados para reforzar cada uno de los temas abordados en el temario. Los enunciados de los ejercicios se encuentran disponibles en la carpeta [`/ejercicios`](./ejercicios) del repositorio, organizados por módulos temáticos.

---

> **Nota:** El material de estudio y los ejercicios están en constante desarrollo. Las contribuciones y sugerencias son bienvenidas.