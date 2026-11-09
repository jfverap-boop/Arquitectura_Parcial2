"""Evidencia 4: configuración de RAM a 32 posiciones de 8 bits"""
import simulador_ram_mejorado as sim


def main():
    sim.configurar_memoria(32, 8)
    print("EVIDENCIA 4 - MEMORIA CONFIGURABLE")
    print("$ python evidencia_4_configuracion.py")
    print("Nueva configuración aplicada; RAM, ACC y PC reiniciados.")
    sim.mostrar_datos_memoria()


if __name__ == "__main__":
    main()
