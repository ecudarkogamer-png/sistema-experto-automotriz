# =====================================================================
# SISTEMA EXPERTO AUTOMOTRIZ: AUTOEXPERT
# Módulo: Motor de Inferencia Explícito (3 Fases Clásicas)
# =====================================================================

"""
Este módulo implementa el motor de inferencia clásico basado en reglas,
separando de forma rigurosa y didáctica las tres fases fundamentales del ciclo:

1. FASE DE EQUIPARACIÓN (Match / Pattern Matching):
   Determina cuáles reglas de la base de conocimiento tienen todas sus
   condiciones ('SI') satisfechas por los hechos actuales en la memoria de trabajo.
   El resultado es el "Conjunto Conflicto" (Conflict Set).

2. FASE DE RESOLUCIÓN DE CONFLICTOS (Conflict Resolution):
   Cuando varias reglas son aplicables simultáneamente en el Conjunto Conflicto,
   se selecciona cuál debe dispararse primero aplicando estrategias formales:
   - Estrategia A: Prioridad de severidad (Prioridad 1 > 2 > 3 > 4).
   - Estrategia B: Especificidad (Reglas con mayor cantidad de condiciones específicas ganan).
   - Estrategia C: Orden de declaración como desempate final.

3. FASE DE EJECUCIÓN (Act / Execution):
   Dispara la regla ganadora, genera el diagnóstico final, aplica recomendaciones
   y construye la traza completa de justificación ("explicación del razonamiento").
"""

from typing import Dict, List, Any, Tuple, Optional


class TrazaFase:
    """Estructura para almacenar los detalles de cada fase del motor."""
    def __init__(self, nombre: str, descripcion: str, detalles: List[str]):
        self.nombre = nombre
        self.descripcion = descripcion
        self.detalles = detalles


class ResultadoInferencia:
    """Estructura que encapsula el veredicto y el razonamiento del sistema experto."""
    def __init__(
        self,
        exito: bool,
        diagnostico: str,
        severidad: str,
        explicacion: str,
        accion: str,
        costo_estimado: str,
        regla_disparada: Optional[Dict[str, Any]],
        conjunto_conflicto: List[Dict[str, Any]],
        trazas: List[TrazaFase],
        hechos_analizados: Dict[str, Any]
    ):
        self.exito = exito
        self.diagnostico = diagnostico
        self.severidad = severidad
        self.explicacion = explicacion
        self.accion = accion
        self.costo_estimado = costo_estimado
        self.regla_disparada = regla_disparada
        self.conjunto_conflicto = conjunto_conflicto
        self.trazas = trazas
        self.hechos_analizados = hechos_analizados


class MotorInferencia:
    """Motor de inferencia hacia adelante con separación explícita de las 3 fases."""

    def __init__(self, base_reglas: List[Dict[str, Any]]):
        self.base_reglas = base_reglas

    # -----------------------------------------------------------------
    # FASE 1: EQUIPARACIÓN (PATTERN MATCHING)
    # -----------------------------------------------------------------
    def equiparacion(self, hechos: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], TrazaFase]:
        """
        Examina todas las reglas de la base de conocimiento y evalúa
        si sus condiciones antecedentes se cumplen en la memoria de hechos.
        Retorna el Conjunto Conflicto (reglas candidatas aplicables).
        """
        conjunto_conflicto = []
        detalles = []

        detalles.append(f"Iniciando evaluación de {len(self.base_reglas)} reglas contra {len(hechos)} hechos observados...")

        for regla in self.base_reglas:
            regla_id = regla["id"]
            nombre = regla["nombre"]
            condiciones = regla["condiciones"]

            # Comprobar si TODAS las condiciones de la regla coinciden con los hechos
            todas_cumplen = True
            condiciones_evaluadas = []

            for clave, valor_esperado in condiciones:
                valor_real = hechos.get(clave)
                if valor_real == valor_esperado:
                    condiciones_evaluadas.append(f"✓ {clave} == '{valor_esperado}' (CUMPLE)")
                else:
                    condiciones_evaluadas.append(f"✗ {clave} == '{valor_esperado}' (FALLA: valor real es '{valor_real}')")
                    todas_cumplen = False

            if todas_cumplen:
                conjunto_conflicto.append(regla)
                detalles.append(
                    f"-> [EQUIPARADA] Regla {regla_id} ('{nombre}'): "
                    f"Todas las condiciones se satisfacen. ({', '.join(condiciones_evaluadas)})"
                )
            else:
                detalles.append(
                    f"   [DESCARTADA] Regla {regla_id} ('{nombre}'): "
                    f"{', '.join(condiciones_evaluadas)}"
                )

        detalles.append(f"Fin de Fase 1. Se encontraron {len(conjunto_conflicto)} reglas en el Conjunto Conflicto.")

        traza = TrazaFase(
            nombre="Fase 1: Equiparación (Pattern Matching)",
            descripcion="Búsqueda de reglas cuyos antecedentes 'SI' se cumplen en la memoria de trabajo.",
            detalles=detalles
        )

        return conjunto_conflicto, traza

    # -----------------------------------------------------------------
    # FASE 2: RESOLUCIÓN DE CONFLICTOS (CONFLICT RESOLUTION)
    # -----------------------------------------------------------------
    def resolucion_conflictos(self, conjunto_conflicto: List[Dict[str, Any]]) -> Tuple[Optional[Dict[str, Any]], TrazaFase]:
        """
        Aplica estrategias formales para desempatar y seleccionar una única regla
        ganadora cuando múltiples reglas han equiparado:
        1. Prioridad de Severidad (menor número = mayor urgencia: 1 > 2 > 3 > 4).
        2. Especificidad (mayor cantidad de condiciones = regla más precisa).
        """
        detalles = []

        if not conjunto_conflicto:
            detalles.append("El Conjunto Conflicto está vacío. No hay reglas aplicables para desempatar.")
            traza = TrazaFase(
                nombre="Fase 2: Resolución de Conflictos",
                descripcion="Ordenamiento y selección de la regla más prioritaria del conjunto conflicto.",
                detalles=detalles
            )
            return None, traza

        detalles.append(f"Resolviendo conflicto entre {len(conjunto_conflicto)} regla(s) candidata(s)...")

        # Criterio de ordenación:
        # 1) prioridad ascendente (1 es más prioritario que 2)
        # 2) especificidad descendente (-len(condiciones) para que más condiciones vayan primero)
        # 3) id alfabético como desempate determinista
        candidatas_ordenadas = sorted(
            conjunto_conflicto,
            key=lambda r: (r["prioridad"], -len(r["condiciones"]), r["id"])
        )

        for i, r in enumerate(candidatas_ordenadas, start=1):
            detalles.append(
                f"   Opción {i}: [{r['id']}] '{r['nombre']}' | "
                f"Prioridad={r['prioridad']} ({r['severidad']}) | "
                f"Especificidad={len(r['condiciones'])} condición(es)"
            )

        regla_ganadora = candidatas_ordenadas[0]
        detalles.append(
            f"-> [SELECCIONADA]: Regla {regla_ganadora['id']} ('{regla_ganadora['nombre']}') "
            f"por criterio de máxima prioridad ({regla_ganadora['severidad']}) "
            f"y especificidad ({len(regla_ganadora['condiciones'])} condiciones)."
        )

        traza = TrazaFase(
            nombre="Fase 2: Resolución de Conflictos",
            descripcion="Selección de la regla activa mediante estrategias de Prioridad y Especificidad.",
            detalles=detalles
        )

        return regla_ganadora, traza

    # -----------------------------------------------------------------
    # FASE 3: EJECUCIÓN (ACT / EXECUTION)
    # -----------------------------------------------------------------
    def ejecucion(self, regla_ganadora: Optional[Dict[str, Any]], hechos: Dict[str, Any]) -> Tuple[Dict[str, Any], TrazaFase]:
        """
        Dispara la regla seleccionada, genera el diagnóstico final,
        las explicaciones técnicas y las acciones correctivas recomendadas.
        """
        detalles = []

        if regla_ganadora is None:
            detalles.append("No hubo ninguna regla disparada. Se emite un dictamen neutro o indeterminado.")
            dictamen = {
                "exito": False,
                "diagnostico": "DIAGNÓSTICO INDETERMINADO: Cuadro de Síntomas No Concluyente",
                "severidad": "DESCONOCIDA",
                "explicacion": "Los síntomas ingresados no coinciden con ningún patrón de falla conocido en la base de conocimiento actual.",
                "accion": "Se sugiere una inspección física detallada por parte de un mecánico automotriz calificado.",
                "costo_estimado": "Costo de diagnóstico básico en taller."
            }
        else:
            detalles.append(f"Disparando la Regla {regla_ganadora['id']} ('{regla_ganadora['nombre']}')...")
            detalles.append(f"-> Acción ejecutada: Asignación de diagnóstico '{regla_ganadora['diagnostico']}'")
            detalles.append(f"-> Nivel de severidad asignado: {regla_ganadora['severidad']}")
            detalles.append(f"-> Justificación técnica: {regla_ganadora['explicacion']}")
            detalles.append(f"-> Protocolo de seguridad: {regla_ganadora['accion']}")

            dictamen = {
                "exito": True,
                "diagnostico": regla_ganadora["diagnostico"],
                "severidad": regla_ganadora["severidad"],
                "explicacion": regla_ganadora["explicacion"],
                "accion": regla_ganadora["accion"],
                "costo_estimado": regla_ganadora["costo_estimado"]
            }

        traza = TrazaFase(
            nombre="Fase 3: Ejecución / Actuación (Act)",
            descripcion="Disparo de la regla ganadora y generación del dictamen diagnóstico final.",
            detalles=detalles
        )

        return dictamen, traza

    # -----------------------------------------------------------------
    # MÉTODO INTEGRAL: CICLO COMPLETO DE INFERENCIA
    # -----------------------------------------------------------------
    def ejecutar_inferencia(self, hechos: Dict[str, Any]) -> ResultadoInferencia:
        """
        Ejecuta el ciclo de razonamiento completo invocando secuencialmente
        las tres fases explícitas del motor.
        """
        # Fase 1: Equiparación
        conjunto_conflicto, traza_fase1 = self.equiparacion(hechos)

        # Fase 2: Resolución de Conflictos
        regla_ganadora, traza_fase2 = self.resolucion_conflictos(conjunto_conflicto)

        # Fase 3: Ejecución
        dictamen, traza_fase3 = self.ejecucion(regla_ganadora, hechos)

        return ResultadoInferencia(
            exito=dictamen["exito"],
            diagnostico=dictamen["diagnostico"],
            severidad=dictamen["severidad"],
            explicacion=dictamen["explicacion"],
            accion=dictamen["accion"],
            costo_estimado=dictamen["costo_estimado"],
            regla_disparada=regla_ganadora,
            conjunto_conflicto=conjunto_conflicto,
            trazas=[traza_fase1, traza_fase2, traza_fase3],
            hechos_analizados=hechos
        )
