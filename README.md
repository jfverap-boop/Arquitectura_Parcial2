# Simulador de memoria RAM y CPU en Python

## 1. Descripción del proyecto

Este proyecto consiste en la ampliación de un simulador de memoria RAM y CPU desarrollado en Python. Su propósito es representar de forma didáctica cómo se almacenan los datos en memoria, cómo se ejecutan instrucciones y cómo interactúan algunos registros básicos del procesador.

El programa permite leer y escribir datos en la RAM, ejecutar operaciones aritméticas mediante un conjunto de instrucciones, consultar el estado del acumulador y revisar un historial de ejecución paso a paso.

También incorpora un sistema de validación de entradas y la posibilidad de configurar la capacidad de la memoria y el ancho de los datos en bits.

## 2. Objetivos

- Comprender la relación entre la memoria RAM, los registros del procesador y las instrucciones.
- Implementar nuevas operaciones aritméticas, como resta, multiplicación e incremento.
- Representar el ciclo de ejecución de un programa mediante el contador de programa.
- Validar instrucciones y prevenir errores relacionados con direcciones inválidas o posiciones vacías.
- Analizar cómo la capacidad de memoria y el ancho de los datos afectan los valores que pueden almacenarse.

## 3. Tecnologías utilizadas

- **Lenguaje de programación:** Python 3.
- **Entorno de desarrollo:** Visual Studio Code.
- **Librerías externas:** no se requieren; el simulador utiliza funcionalidades propias de Python.

## 4. Requisitos para ejecutar el programa

Antes de ejecutar el simulador, se debe tener instalado Python 3 y un editor de código, como Visual Studio Code.

Para comprobar que Python está instalado, se puede ejecutar el siguiente comando en la terminal:

```bash
python --version
```

En algunos equipos con Windows también puede utilizarse:

```bash
py --version
```

## 5. Estructura de archivos

El proyecto está compuesto por el simulador principal y cuatro archivos de prueba utilizados para generar las evidencias de ejecución.

```text
codigos_evidencias_vscode/
│
├── simulador_ram_mejorado.py
├── evidencia_1_aritmetica.py
├── evidencia_2_desbordamiento.py
├── evidencia_3_validaciones.py
├── evidencia_4_configuracion.py
└── README.md
```

El archivo `simulador_ram_mejorado.py` contiene la implementación principal. Los archivos de evidencia permiten comprobar por separado el funcionamiento de las operaciones, el desbordamiento, las validaciones y la configuración de la memoria.

Todos los archivos deben permanecer en la misma carpeta para que las pruebas puedan importar correctamente el simulador.

## 6. Funcionalidades implementadas

### 6.1. Visualización de la memoria RAM

Permite consultar las posiciones de memoria disponibles, el valor decimal almacenado y su representación binaria.

Las posiciones que todavía no contienen datos se identifican como vacías. Al finalizar la consulta, el programa muestra la cantidad de posiciones ocupadas y la capacidad total configurada.

### 6.2. Escritura de datos

Permite almacenar un número entero en una dirección específica de la RAM.

Antes de realizar la operación, el programa verifica que la dirección esté dentro del rango permitido y que el dato pueda representarse con el ancho de palabra configurado.

Si la posición ya contiene información, el simulador muestra un mensaje indicando que el dato anterior fue reemplazado.

### 6.3. Lectura de datos

Permite consultar el contenido de una dirección de memoria. Cuando la posición contiene un valor, se muestra tanto su representación decimal como la binaria.

Si la dirección está vacía o se encuentra fuera del rango permitido, el programa informa la situación sin intentar realizar una lectura inválida.

### 6.4. Ejecución de instrucciones

El simulador permite ingresar una secuencia de instrucciones y ejecutarlas en orden. Durante el proceso, se actualizan los registros correspondientes y se muestra un historial de cada operación.

Las instrucciones implementadas son:

| Instrucción       | Función                                                                   |
| ----------------- | ------------------------------------------------------------------------- |
| `LOAD dirección`  | Carga en el acumulador el dato de una dirección de RAM.                   |
| `ADD dirección`   | Suma al acumulador el dato almacenado en la dirección indicada.           |
| `SUB dirección`   | Resta del acumulador el dato de la dirección indicada.                    |
| `MUL dirección`   | Multiplica el acumulador por el dato almacenado en la dirección indicada. |
| `INC`             | Incrementa el acumulador en una unidad.                                   |
| `STORE dirección` | Guarda en la RAM el valor actual del acumulador.                          |

La captura de instrucciones finaliza cuando el usuario escribe `FIN`.

### 6.5. Historial de ejecución

Después de cada instrucción ejecutada, el programa presenta una tabla con los siguientes campos:

- **PC:** posición de la instrucción que se está ejecutando.
- **Instrucción:** operación que se ejecutó.
- **ACC antes:** valor del acumulador antes de ejecutar la instrucción.
- **ACC después:** valor del acumulador al terminar la operación.
- **Dir. RAM:** dirección de memoria consultada o modificada, cuando corresponde.
- **Resultado:** descripción de la operación o del error detectado.

Este historial facilita la revisión del comportamiento del programa y permite identificar cómo cambia el acumulador en cada paso.

### 6.6. Validación y protección

El programa incorpora controles para detectar entradas incorrectas y evitar operaciones que no puedan ejecutarse correctamente.

Entre las validaciones implementadas se encuentran:

- Verificación de que la instrucción exista.
- Comprobación del formato de las instrucciones.
- Validación de que las direcciones estén dentro del rango configurado.
- Detección de posiciones de memoria vacías.
- Comprobación de que el acumulador esté inicializado antes de realizar operaciones aritméticas o incrementarlo.
- Validación de los valores ingresados para configurar la memoria.

Cuando se detecta un problema, se muestra un mensaje descriptivo. Las instrucciones inválidas se omiten durante la captura del programa y la ejecución puede continuar con las instrucciones válidas.

### 6.7. Configuración de la memoria

El usuario puede cambiar la cantidad de posiciones de RAM y el ancho de cada dato.

Los límites implementados son:

- Capacidad: entre 1 y 256 posiciones.
- Ancho de dato: entre 1 y 64 bits.

El simulador calcula el valor máximo representable mediante la siguiente fórmula:

**Valor máximo = 2ⁿ − 1**

Donde _n_ corresponde al número de bits utilizados para representar cada dato.

También calcula la capacidad teórica total en bits y bytes:

**Capacidad en bits = posiciones de RAM × bits por dato**

**Capacidad en bytes = capacidad en bits ÷ 8**

Cuando se modifica la configuración, se reinician la memoria RAM y los registros asociados. Si existen datos almacenados, el programa solicita una confirmación antes de borrarlos.

## 7. Conceptos de arquitectura de computadores

El simulador representa algunos elementos fundamentales de la arquitectura de un computador.

### Memoria RAM

Es el espacio de almacenamiento utilizado por el programa para guardar datos en posiciones identificadas mediante direcciones numéricas. En este modelo, las direcciones comienzan en cero.

### Acumulador (ACC)

Es el registro utilizado para almacenar los operandos y resultados de las operaciones aritméticas. Las instrucciones `LOAD`, `ADD`, `SUB`, `MUL` e `INC` interactúan con este registro.

### Contador de programa (PC)

Es la variable que indica la posición de la instrucción que se está ejecutando. En cada paso de la secuencia, el contador aumenta en una unidad.

### Ancho de palabra

Representa la cantidad de bits disponibles para almacenar cada dato. Por ejemplo, con 8 bits se pueden representar valores entre 0 y 255 sin signo.

Estos componentes permiten estudiar de forma simplificada la relación entre el almacenamiento de datos, los registros y la ejecución de instrucciones.

## 8. Tratamiento del desbordamiento

La implementación utiliza aritmética modular de acuerdo con el ancho de palabra configurado.

Para una memoria de 8 bits, los resultados se ajustan al rango de 0 a 255 mediante la operación módulo 256.

Por ejemplo:

```python
resultado = (200 + 100) % 256
print(resultado)
```

El resultado es:

```text
44
```

Esto sucede porque 300 módulo 256 es igual a 44.

La misma regla se aplica a las operaciones `ADD`, `SUB`, `MUL` e `INC`. De esta manera, se representa de forma simplificada el comportamiento de una operación aritmética limitada a un ancho fijo de bits.

## 9. Cómo ejecutar el simulador

1. Abrir Visual Studio Code.
2. Seleccionar **Archivo → Abrir carpeta**.
3. Elegir la carpeta donde se encuentra `simulador_ram_mejorado.py`.
4. Abrir el archivo principal.
5. Seleccionar **Terminal → Nueva terminal**.
6. Ejecutar el siguiente comando:

```bash
python simulador_ram_mejorado.py
```

Si el comando anterior no funciona en Windows, se puede utilizar:

```bash
py simulador_ram_mejorado.py
```

Al iniciar, se presenta un menú con las siguientes opciones:

| Opción | Acción                                      |
| ------ | ------------------------------------------- |
| 1      | Mostrar memoria RAM.                        |
| 2      | Escribir un dato en la RAM.                 |
| 3      | Leer un dato de la RAM.                     |
| 4      | Ingresar y ejecutar un programa.            |
| 5      | Reiniciar la RAM y la CPU.                  |
| 6      | Configurar la capacidad y el ancho de dato. |
| 0      | Salir del simulador.                        |

Para seleccionar una opción, se debe ingresar el número correspondiente en la terminal.

## 10. Pruebas de funcionamiento

El proyecto incluye cuatro pruebas para verificar las mejoras implementadas.

### Evidencia 1. Operaciones aritméticas

Comprueba el funcionamiento de las instrucciones `SUB`, `MUL`, `INC` y `STORE`, verificando los resultados obtenidos en el acumulador y en la memoria.

### Evidencia 2. Desbordamiento

Evalúa el comportamiento de la aritmética modular de 8 bits cuando una suma supera el máximo representable.

### Evidencia 3. Validaciones

Comprueba la respuesta del programa frente a direcciones fuera de rango, operaciones desconocidas y accesos a posiciones vacías.

### Evidencia 4. Configuración

Verifica el cambio de capacidad y ancho de dato, además del cálculo del valor máximo y la capacidad total de la memoria.

Para ejecutar cada prueba, se utiliza el comando correspondiente desde la terminal de VS Code:

```bash
python evidencia_1_aritmetica.py
python evidencia_2_desbordamiento.py
python evidencia_3_validaciones.py
python evidencia_4_configuracion.py
```

Cada comando debe ejecutarse por separado. Los resultados permiten comprobar el comportamiento esperado y obtener las capturas utilizadas como evidencias de ejecución.

## 11. Limitaciones del simulador

Este programa tiene fines académicos y representa una versión simplificada de algunos componentes de un computador.

No simula una memoria física real ni reproduce todas las características de un procesador comercial. Tampoco modela tiempos de acceso, cachés, buses físicos, ejecución en paralelo, interrupciones o un sistema operativo.

El historial de ejecución permite observar los cambios de estado, pero la representación sigue siendo una abstracción diseñada para facilitar el aprendizaje de los conceptos básicos.

## 12. Conclusión

La ampliación del simulador permite relacionar conceptos de programación con fundamentos de arquitectura de computadores. Mediante las operaciones aritméticas, el manejo de la memoria, los registros y las validaciones es posible observar cómo una secuencia de instrucciones modifica el estado del sistema.

Además, la configuración del ancho de palabra permite comprender por qué el rango de los datos depende del número de bits disponibles y cómo se presenta el desbordamiento cuando se trabaja con una cantidad limitada de bits.

El desarrollo constituye una herramienta de apoyo para estudiar la relación entre memoria, registros e instrucciones, así como para practicar validaciones y organización del código en Python.

## 11. Ampliación del Examen 2: ciclo Fetch–Decode–Execute

La opción 4 ejecuta ahora cada instrucción en tres etapas visibles: FETCH, DECODE y EXECUTE. En el modo interactivo, presione ENTER para avanzar entre las etapas y entre instrucciones. Durante cada etapa se muestran PC, ACC, instrucción actual y RAM. El PC avanza únicamente después de terminar EXECUTE.

Para ejecutar las tres pruebas reproducibles del examen:

```bash
python pruebas_examen2.py
```

Las pruebas verifican el ciclo por etapas y las operaciones, el desbordamiento modular de 8 bits, y la configuración/validación de la memoria. Las salidas están en `EVIDENCIAS_PRUEBAS.txt`.
