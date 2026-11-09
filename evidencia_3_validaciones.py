"""Evidencia 3: validación de direcciones e instrucciones y protección de RAM vacía"""
import io
from contextlib import redirect_stdout
from unittest.mock import patch

import simulador_ram_mejorado as sim


def main():
    sim.configurar_memoria(16, 8)
    # LOAD 99 está fuera de rango; XYZ es una operación desconocida
    instrucciones = ["LOAD 99", "LOAD 3", "ADD 0", "INC", "XYZ", "FIN"]

    with redirect_stdout(io.StringIO()) as salida:
        with patch("builtins.input", side_effect=instrucciones):
            historial = sim.ejecutar_programa()

    lineas = salida.getvalue().splitlines()
    errores_validacion = [linea for linea in lineas if "Instrucción omitida:" in linea]

    print("EVIDENCIA 3 - VALIDACIÓN Y POSICIONES VACÍAS")
    print("$ python evidencia_3_validaciones.py")
    print("Instrucción: LOAD 99")
    for error in errores_validacion:
        if "Dirección fuera de rango" in error:
            print(error)
    print("Instrucción: LOAD 3")
    print("Instrucción: ADD 0")
    print("Instrucción: INC")
    print("Instrucción: XYZ")
    for error in errores_validacion:
        if "Operación desconocida" in error:
            print(error)

    for fila in historial:
        print(f"PC={fila['pc']} -> {fila['instruccion']} | {fila['resultado']}")
    print(f"ACC final: {sim.ACC}")
    print(f"PC final: {sim.PC}")


if __name__ == "__main__":
    main()
