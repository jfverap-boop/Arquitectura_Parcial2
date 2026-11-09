"""Tres pruebas reproducibles para las ampliaciones del Examen 2."""
import contextlib
import io
from unittest.mock import patch
import simulador_ram_mejorado as sim


def ejecutar(nombre, instrucciones):
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        with patch("builtins.input", side_effect=instrucciones):
            historial = sim.ejecutar_programa(paso_a_paso=False)
    texto = salida.getvalue()
    print(f"\n===== {nombre} =====")
    print(texto)
    return historial, texto


def prueba_1_fetch_decode_execute():
    sim.configurar_memoria(16, 8)
    sim.ram[0], sim.ram[1] = 20, 7
    historial, salida = ejecutar(
        "PRUEBA 1 - CICLO FETCH-DECODE-EXECUTE",
        ["LOAD 0", "SUB 1", "MUL 1", "INC", "STORE 2", "FIN"],
    )
    assert sim.ACC == 92 and sim.ram[2] == 92 and sim.PC == 5
    assert "ETAPA FETCH" in salida and "ETAPA DECODE" in salida and "ETAPA EXECUTE" in salida
    assert len(historial) == 5
    print("RESULTADO: APROBADA. ACC=92, RAM[2]=92, PC=5.")


def prueba_2_desbordamiento():
    sim.configurar_memoria(16, 8)
    sim.ram[0], sim.ram[1] = 200, 100
    ejecutar("PRUEBA 2 - DESBORDAMIENTO DE 8 BITS", ["LOAD 0", "ADD 1", "INC", "FIN"])
    assert sim.ACC == 45 and sim.PC == 3
    print("RESULTADO: APROBADA. 200+100=300; 300 módulo 256=44; INC=45.")


def prueba_3_configuracion_validacion():
    sim.configurar_memoria(32, 8)
    assert sim.CAPACIDAD == 32 and sim.BITS == 8 and sim.MAXIMO == 255
    assert sim.CAPACIDAD * sim.BITS == 256
    assert (sim.CAPACIDAD * sim.BITS) / 8 == 32
    assert sim.analizar_instruccion("LOAD 32")[1] is not None
    assert sim.analizar_instruccion("XYZ")[1] is not None
    sim.ram[0] = 255
    assert sim.formato_binario(255) == "11111111"
    print("\n===== PRUEBA 3 - CONFIGURACIÓN Y VALIDACIONES =====")
    print("Configuración: 32 posiciones x 8 bits")
    print("Máximo por posición: 255")
    print("Capacidad: 256 bits = 32 bytes")
    print("Dirección 32 rechazada; operación XYZ rechazada.")
    print("Dato 255 en binario: 11111111")
    print("RESULTADO: APROBADA.")


if __name__ == "__main__":
    prueba_1_fetch_decode_execute()
    prueba_2_desbordamiento()
    prueba_3_configuracion_validacion()
    print("\nTODAS LAS PRUEBAS DEL EXAMEN 2 FINALIZARON CORRECTAMENTE.")
