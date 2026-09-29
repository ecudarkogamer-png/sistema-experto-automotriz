# =====================================================================
# SISTEMA EXPERTO AUTOMOTRIZ: AUTOEXPERT
# Archivo Principal de Ejecución (Launcher)
# =====================================================================

"""
Punto de entrada principal para el Sistema Experto 'AutoExpert'.
Modos de ejecución disponibles:
  1. Gráfico Web (Por defecto): python main.py
     Inicia el servidor local y abre la interfaz interactiva en su navegador.
  2. Gráfico Tkinter (Opcional): python main.py --tkinter
     Inicia la aplicación de escritorio nativa (requiere Tkinter instalado).
  3. Prueba de Inferencia: python main.py --test
     Ejecuta casos de prueba automáticos para verificar las 3 fases del motor.
"""

import sys
import os

# Asegurar que el directorio de auto_expert esté en sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def ejecutar_pruebas():
    """Ejecuta una batería de pruebas de inferencia para validar las 3 fases."""
    from base_conocimiento import REGLAS
    from motor_inferencia import MotorInferencia

    motor = MotorInferencia(REGLAS)

    print("\n" + "=" * 65)
    print("EJECUTANDO BATERÍA DE PRUEBAS DE INFERENCIA EN AUTOEXPERT")
    print("=" * 65)

    casos = [
        {
            "nombre": "Caso 1: Emergencia por Presión de Aceite (Prioridad 1)",
            "hechos": {
                "arranque_motor": "normal",
                "sonido_motor": "golpeteo_metalico",
                "humo_escape": "ninguno_normal",
                "comportamiento_frenos": "normal",
                "temperatura_motor": "normal",
                "fuga_fluidos": "aceite_oscuro",
                "testigo_tablero": "presion_aceite",
                "comportamiento_direccion": "normal",
                "respuesta_aceleracion": "normal",
                "tiempo_ultimo_mantenimiento": "mayor_1_ano_o_nunca"
            },
            "regla_esperada": "R01"
        },
        {
            "nombre": "Caso 2: Emergencia de Frenos Hidráulicos (Prioridad 1)",
            "hechos": {
                "arranque_motor": "normal",
                "sonido_motor": "ninguno",
                "humo_escape": "ninguno_normal",
                "comportamiento_frenos": "esponjoso_se_hunde",
                "temperatura_motor": "normal",
                "fuga_fluidos": "liquido_frenos",
                "testigo_tablero": "frenos_abs",
                "comportamiento_direccion": "normal",
                "respuesta_aceleracion": "normal",
                "tiempo_ultimo_mantenimiento": "entre_6_y_12_meses"
            },
            "regla_esperada": "R02"
        },
        {
            "nombre": "Caso 3: Batería Agotada / Sistema Eléctrico (Prioridad 2)",
            "hechos": {
                "arranque_motor": "no_gira",
                "sonido_motor": "ninguno",
                "humo_escape": "ninguno_normal",
                "comportamiento_frenos": "normal",
                "temperatura_motor": "normal",
                "fuga_fluidos": "ninguno",
                "testigo_tablero": "bateria_alternador",
                "comportamiento_direccion": "normal",
                "respuesta_aceleracion": "normal",
                "tiempo_ultimo_mantenimiento": "menor_6_meses"
            },
            "regla_esperada": "R06"
        },
        {
            "nombre": "Caso 4: Vehículo en Buen Estado Operativo (Prioridad 4)",
            "hechos": {
                "arranque_motor": "normal",
                "sonido_motor": "ninguno",
                "humo_escape": "ninguno_normal",
                "comportamiento_frenos": "normal",
                "temperatura_motor": "normal",
                "fuga_fluidos": "ninguno",
                "testigo_tablero": "ninguno",
                "comportamiento_direccion": "normal",
                "respuesta_aceleracion": "normal",
                "tiempo_ultimo_mantenimiento": "menor_6_meses"
            },
            "regla_esperada": "R12"
        }
    ]

    for caso in casos:
        print(f"\n--- {caso['nombre']} ---")
        res = motor.ejecutar_inferencia(caso["hechos"])
        regla_obtenida = res.regla_disparada["id"] if res.regla_disparada else "NINGUNA"

        print(f"  Regla Esperada : {caso['regla_esperada']}")
        print(f"  Regla Disparada: {regla_obtenida}")
        print(f"  Severidad      : {res.severidad}")
        print(f"  Diagnóstico    : {res.diagnostico}")
        print(f"  Conflicto      : {len(res.conjunto_conflicto)} regla(s) equipararon.")

        assert regla_obtenida == caso["regla_esperada"], (
            f"Fallo en prueba: Se esperaba {caso['regla_esperada']} pero se obtuvo {regla_obtenida}"
        )
        print("  -> PRUEBA SUPERADA CON EXITO! [OK]")

    print("\n" + "=" * 65)
    print("TODAS LAS PRUEBAS DE INFERENCIA EN LAS 3 FASES HAN SIDO SUPERADAS.")
    print("=" * 65)


def main():
    args = sys.argv[1:]

    if "--test" in args:
        ejecutar_pruebas()
        return

    if "--tkinter" in args:
        try:
            from app_tkinter import iniciar_app_tkinter
            iniciar_app_tkinter()
            return
        except ImportError:
            print("[AVISO] Tkinter no está presente. Iniciando interfaz web por defecto...")

    # Modo por defecto: Interfaz Gráfica Web
    from app_web import iniciar_servidor
    iniciar_servidor()


if __name__ == "__main__":
    main()
