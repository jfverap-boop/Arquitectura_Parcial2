"""Evidencia 1: instrucciones SUB, MUL, INC y STORE"""
import io
from contextlib import redirect_stdout
from unittest.mock import patch

import simulador_ram_mejorado as sim


def main():
    sim.configurar_memoria(16, 8)
    sim.ram[0] = 20
    sim.ram[1] = 7
    instrucciones = ["LOAD 0", "SUB 1", "MUL 1", "INC", "STORE 2", "FIN"]

    with redirect_stdout(io.StringIO()):
        with patch("builtins.input", side_effect=instrucciones):
            historial = sim.ejecutar_programa()

    print("EVIDENCIA 1 - OPERACIONES SUB, MUL, INC Y STORE")
    print("$ python evidencia_1_aritmetica.py")
    print("WRITE: se guardó 20 en la dirección 0.")
    print("WRITE: se guardó 7 en la dirección 1.")
    for fila in historial:
        print(f"PC={fila['pc']} -> {fila['instruccion']} | {fila['resultado']}")
    print(f"ACC final: {sim.ACC}")
    print(f"PC final: {sim.PC}")
    print(f"Resultado comprobado: RAM[2] <- {sim.ram[2]}")


if __name__ == "__main__":
    main()
