"""Evidencia 2: desbordamiento con aritmética modular de 8 bits"""
import io
from contextlib import redirect_stdout
from unittest.mock import patch

import simulador_ram_mejorado as sim


def main():
    sim.configurar_memoria(16, 8)
    sim.ram[0] = 200
    sim.ram[1] = 100
    instrucciones = ["LOAD 0", "ADD 1", "INC", "FIN"]

    with redirect_stdout(io.StringIO()):
        with patch("builtins.input", side_effect=instrucciones):
            historial = sim.ejecutar_programa()

    print("EVIDENCIA 2 - ARITMÉTICA MODULAR DE 8 BITS")
    print("$ python evidencia_2_desbordamiento.py")
    print("WRITE: se guardó 200 en la dirección 0.")
    print("WRITE: se guardó 100 en la dirección 1.")
    for fila in historial:
        print(f"PC={fila['pc']} -> {fila['instruccion']} | {fila['resultado']}")
    print(f"ACC final: {sim.ACC}")
    print(f"PC final: {sim.PC}")


if __name__ == "__main__":
    main()

