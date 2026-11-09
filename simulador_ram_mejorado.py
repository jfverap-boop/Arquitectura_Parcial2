"""Simulador didáctico de memoria RAM y CPU

Permite configurar la memoria, leer y escribir datos, y ejecutar un conjunto
pequeño de instrucciones. La aritmética usa resultados modulares de acuerdo
con el ancho de palabra seleccionado: por ejemplo, con 8 bits, 260 se convierte
 en 4 porque 260 % 256 == 4
"""

DEFAULT_CAPACITY = 16
DEFAULT_BITS = 8
MAX_CAPACITY = 256
MAX_BITS = 64

CAPACIDAD = DEFAULT_CAPACITY
BITS = DEFAULT_BITS
MAXIMO = (2 ** BITS) - 1
ram = [None] * CAPACIDAD
ACC = None
PC = 0

OPERACIONES_CON_DIRECCION = {"LOAD", "ADD", "SUB", "MUL", "STORE"}
OPERACIONES_VALIDAS = OPERACIONES_CON_DIRECCION | {"INC"}


def configurar_memoria(capacidad, bits):
    """Configura RAM y reinicia los registros asociados"""
    global CAPACIDAD, BITS, MAXIMO, ram, ACC, PC
    CAPACIDAD = capacidad
    BITS = bits
    MAXIMO = (2 ** BITS) - 1
    ram = [None] * CAPACIDAD
    ACC = None
    PC = 0


def pedir_entero(mensaje):
    """Solicita un entero sin dejar que una entrada no numérica cierre el programa"""
    while True:
        texto = input(mensaje).strip()
        try:
            return int(texto)
        except ValueError:
            print("Entrada no válida. Ingresa un número entero.")


def formato_binario(dato):
    """Representa un dato con exactamente BITS posiciones binarias"""
    return format(dato, f"0{BITS}b")


def mostrar_datos_memoria():
    """Muestra las características generales de la memoria configurada"""
    bits_totales = CAPACIDAD * BITS
    bytes_totales = bits_totales / 8
    ocupadas = sum(dato is not None for dato in ram)
    print(f"Capacidad: {CAPACIDAD} posiciones | Ancho: {BITS} bits | Máximo: {MAXIMO}")
    print(f"Capacidad teórica: {bits_totales} bits = {bytes_totales:g} bytes")
    print(f"Posiciones ocupadas: {ocupadas}/{CAPACIDAD}")


def mostrar_memoria():
    print("\n========================= MEMORIA RAM =========================")
    ancho_decimal = max(7, len(str(MAXIMO)))
    print(f"{'Dirección':>9} | {'Decimal':>{ancho_decimal}} | Binario")
    print("-" * (25 + BITS))
    for direccion, dato in enumerate(ram):
        decimal = "Vacía" if dato is None else str(dato)
        binario = "-" * BITS if dato is None else formato_binario(dato)
        print(f"{direccion:9} | {decimal:>{max(7, len(str(MAXIMO)))}} | {binario}")
    print("-" * (25 + BITS))
    mostrar_datos_memoria()


def escribir():
    direccion = pedir_entero(f"Dirección de memoria (0-{CAPACIDAD - 1}): ")
    dato = pedir_entero(f"Dato a guardar (0-{MAXIMO}): ")
    if not 0 <= direccion < CAPACIDAD:
        print(f"Error: la dirección debe estar entre 0 y {CAPACIDAD - 1}.")
        return
    if not 0 <= dato <= MAXIMO:
        print(f"Error: el dato debe estar entre 0 y {MAXIMO} para {BITS} bits.")
        return
    anterior = ram[direccion]
    ram[direccion] = dato
    if anterior is None:
        print(f"WRITE: se guardó {dato} en la dirección {direccion}.")
    else:
        print(f"OVERWRITE: la dirección {direccion} cambió de {anterior} a {dato}.")


def leer():
    direccion = pedir_entero(f"Dirección que deseas consultar (0-{CAPACIDAD - 1}): ")
    if not 0 <= direccion < CAPACIDAD:
        print(f"Error: la dirección debe estar entre 0 y {CAPACIDAD - 1}.")
        return
    dato = ram[direccion]
    if dato is None:
        print(f"READ: la dirección {direccion} está vacía.")
    else:
        print(f"READ: dirección {direccion} = {dato} (binario: {formato_binario(dato)}).")


def analizar_instruccion(linea):
    """Valida sintaxis y dirección de una instrucción de programa

    Retorna (instrucción, error). Cuando hay error, instrucción es None
    Las instrucciones inválidas se omiten y la captura del programa continúa
    """
    partes = linea.upper().split()
    if not partes:
        return None, "La instrucción está vacía."
    operacion = partes[0]
    if operacion not in OPERACIONES_VALIDAS:
        return None, f"Operación desconocida: {operacion}. Usa LOAD, ADD, SUB, MUL, INC o STORE."
    argumentos_esperados = 1 if operacion == "INC" else 2
    if len(partes) != argumentos_esperados:
        if operacion == "INC":
            return None, "INC no recibe dirección; escribe solamente INC."
        return None, f"Formato incorrecto. Uso esperado: {operacion} dirección."
    if operacion == "INC":
        return (operacion, None), None
    try:
        direccion = int(partes[1])
    except ValueError:
        return None, "La dirección debe ser un número entero."
    if not 0 <= direccion < CAPACIDAD:
        return None, f"Dirección fuera de rango: usa 0 a {CAPACIDAD - 1}."
    return (operacion, direccion), None


def imprimir_historial(historial):
    """Imprime la tabla acumulada después de cada instrucción ejecutada"""
    print("\nHISTORIAL DE EJECUCIÓN (PC corresponde a la instrucción ejecutada)")
    encabezados = ("PC", "Instrucción", "ACC antes", "ACC después", "Dir. RAM", "Resultado")
    anchos = (4, 16, 12, 13, 10, 40)
    print(" | ".join(f"{titulo:<{ancho}}" for titulo, ancho in zip(encabezados, anchos)))
    print("-+-".join("-" * ancho for ancho in anchos))
    for fila in historial:
        valores = (str(fila["pc"]), fila["instruccion"], fila["antes"], fila["despues"],
                   fila["direccion"], fila["resultado"])
        print(" | ".join(f"{str(valor):<{ancho}.{ancho}}" for valor, ancho in zip(valores, anchos)))


def mostrar_estado_cpu(etapa, instruccion_actual="—"):
    """Muestra el estado visible de la CPU y la RAM durante cada etapa."""
    print(f"\n--- ETAPA {etapa} ---")
    print(f"PC: {PC}")
    print(f"ACC: {ACC}")
    print(f"Instrucción actual: {instruccion_actual}")
    print(f"RAM: {ram}")


def ejecutar_instruccion(operacion, direccion):
    """Ejecuta una instrucción ya decodificada y devuelve su descripción."""
    global ACC, ram
    dato = ram[direccion] if direccion is not None else None
    if operacion == "LOAD":
        if dato is None:
            return f"ERROR: RAM[{direccion}] está vacía; ACC no cambia"
        ACC = dato
        return f"ACC <- RAM[{direccion}] = {dato}"
    if operacion in {"ADD", "SUB", "MUL"}:
        if ACC is None:
            return "ERROR: ACC no está inicializado; operación omitida"
        if dato is None:
            return f"ERROR: RAM[{direccion}] está vacía; ACC no cambia"
        if operacion == "ADD":
            bruto, simbolo = ACC + dato, "+"
        elif operacion == "SUB":
            bruto, simbolo = ACC - dato, "-"
        else:
            bruto, simbolo = ACC * dato, "*"
        anterior = ACC
        ACC = bruto % (MAXIMO + 1)
        return f"{bruto} = {anterior} {simbolo} {dato}; módulo {MAXIMO + 1} -> {ACC}"
    if operacion == "INC":
        if ACC is None:
            return "ERROR: ACC no está inicializado; INC omitido"
        bruto = ACC + 1
        anterior = ACC
        ACC = bruto % (MAXIMO + 1)
        return f"{anterior} + 1 = {bruto}; módulo {MAXIMO + 1} -> {ACC}"
    if operacion == "STORE":
        if ACC is None:
            return "ERROR: ACC no está inicializado; RAM no cambia"
        ram[direccion] = ACC
        return f"RAM[{direccion}] <- {ACC}"
    return "ERROR: instrucción no reconocida"


def ejecutar_programa(paso_a_paso=True):
    """Captura instrucciones y representa Fetch, Decode y Execute.

    En modo paso a paso, Enter permite avanzar de una etapa a la siguiente.
    """
    global ACC, PC
    instrucciones = []
    print("\nIngresa instrucciones (escribe FIN para terminar la captura).")
    print("Formato: LOAD dir | ADD dir | SUB dir | MUL dir | INC | STORE dir")
    while True:
        try:
            linea = input("Instrucción: ").strip()
        except EOFError:
            print("\nFin de entrada; se ejecutará lo que se haya capturado.")
            break
        if linea.upper() == "FIN":
            break
        instruccion, error = analizar_instruccion(linea)
        if error:
            print(f"Instrucción omitida: {error}")
            continue
        instrucciones.append(instruccion)

    historial = []
    PC = 0
    while PC < len(instrucciones):
        # FETCH: el PC selecciona la instrucción almacenada en la lista del programa.
        instruccion_fetch = instrucciones[PC]
        operacion, direccion = instruccion_fetch
        nombre = f"{operacion} {direccion}" if direccion is not None else operacion
        mostrar_estado_cpu("FETCH", nombre)
        print(f"FETCH: se obtiene la instrucción ubicada en la posición {PC}.")
        if paso_a_paso:
            input("Presiona ENTER para continuar a DECODE...")

        # DECODE: se identifica la operación y el operando/dirección.
        mostrar_estado_cpu("DECODE", nombre)
        if direccion is None:
            print(f"DECODE: operación={operacion}; no requiere dirección de RAM.")
        else:
            print(f"DECODE: operación={operacion}; operando=dirección {direccion}.")
        if paso_a_paso:
            input("Presiona ENTER para continuar a EXECUTE...")

        # EXECUTE: se modifica ACC o RAM según la instrucción.
        antes = ACC
        mostrar_estado_cpu("EXECUTE", nombre)
        resultado = ejecutar_instruccion(operacion, direccion)
        despues = ACC
        print(f"EXECUTE: {resultado}")
        fila = {
            "pc": PC, "instruccion": nombre,
            "antes": "None" if antes is None else antes,
            "despues": "None" if despues is None else despues,
            "direccion": str(direccion) if direccion is not None else "—",
            "resultado": resultado,
        }
        historial.append(fila)
        imprimir_historial(historial)
        if paso_a_paso:
            input("Presiona ENTER para pasar a la siguiente instrucción...")
        PC += 1
        mostrar_estado_cpu("FIN DE INSTRUCCIÓN", "—")

    print("\nPrograma finalizado.")
    print(f"ACC final: {ACC}")
    print(f"PC final: {PC}")
    mostrar_memoria()
    return historial


def configurar_memoria_interactiva():
    """Permite cambiar tamaño y ancho, protegiendo datos ya almacenados"""
    nueva_capacidad = pedir_entero(f"Número de posiciones (1-{MAX_CAPACITY}): ")
    if not 1 <= nueva_capacidad <= MAX_CAPACITY:
        print(f"Error: la capacidad debe estar entre 1 y {MAX_CAPACITY}.")
        return
    nuevos_bits = pedir_entero(f"Ancho de cada dato en bits (1-{MAX_BITS}): ")
    if not 1 <= nuevos_bits <= MAX_BITS:
        print(f"Error: el ancho debe estar entre 1 y {MAX_BITS} bits.")
        return
    if any(dato is not None for dato in ram) or ACC is not None:
        confirmacion = input("Cambiar la configuración borrará RAM y CPU. ¿Continuar? (s/n): ").strip().lower()
        if confirmacion != "s":
            print("Configuración cancelada; los datos actuales se conservan.")
            return
    configurar_memoria(nueva_capacidad, nuevos_bits)
    print("Nueva configuración aplicada; RAM, ACC y PC reiniciados.")
    mostrar_datos_memoria()


def reiniciar():
    confirmacion = input("Se borrarán los datos de RAM y CPU. ¿Continuar? (s/n): ").strip().lower()
    if confirmacion == "s":
        configurar_memoria(CAPACIDAD, BITS)
        print("RAM y CPU reiniciadas.")
    else:
        print("Reinicio cancelado.")


def menu():
    while True:
        print("\n========== SIMULADOR DE RAM Y CPU ==========")
        print(f"Configuración actual: {CAPACIDAD} posiciones, {BITS} bits por dato, máximo {MAXIMO}")
        print("1. Mostrar memoria RAM")
        print("2. Escribir dato en RAM")
        print("3. Leer dato de RAM")
        print("4. Ingresar y ejecutar programa")
        print("5. Reiniciar RAM y CPU")
        print("6. Configurar capacidad y ancho de dato")
        print("0. Salir")
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "1":
            mostrar_memoria()
        elif opcion == "2":
            escribir()
        elif opcion == "3":
            leer()
        elif opcion == "4":
            ejecutar_programa()
        elif opcion == "5":
            reiniciar()
        elif opcion == "6":
            configurar_memoria_interactiva()
        elif opcion == "0":
            print("Simulador finalizado.")
            break
        else:
            print("Opción no válida. Usa 1, 2, 3, 4, 5, 6 o 0.")


if __name__ == "__main__":
    menu()
