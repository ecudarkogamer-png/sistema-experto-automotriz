# =====================================================================
# SISTEMA EXPERTO AUTOMOTRIZ: AUTOEXPERT
# Módulo: Base de Conocimiento (Hechos, Preguntas y Reglas de Producción)
# =====================================================================

"""
Este módulo contiene la base de conocimiento completa del sistema experto:
1. PREGUNTAS_HECHOS: 10 hechos observables que se recopilan mediante interacción
   con el usuario en la interfaz gráfica (interacción media-alta).
2. REGLAS: 12 reglas de producción con prioridades de severidad y especificidad
   para la resolución de conflictos.
"""

# ---------------------------------------------------------------------
# 1. HECHOS OBSERVABLES (10 Preguntas secuenciales para el usuario)
# ---------------------------------------------------------------------
PREGUNTAS_HECHOS = [
    {
        "id": "arranque_motor",
        "numero": 1,
        "titulo": "1. Comportamiento del Arranque",
        "descripcion": "¿Qué ocurre al girar la llave o pulsar el botón de encendido?",
        "icono": "🔑",
        "opciones": [
            ("normal", "Enciende normal y rápido al primer intento", "El motor de arranque y batería responden de inmediato."),
            ("gira_lento", "El motor gira pesado o con dificultad antes de encender", "Se percibe falta de fuerza en el arranque."),
            ("no_gira", "No gira en absoluto (hace un 'clic' o silencio total)", "El motor de combustión no hace ningún intento de girar."),
            ("gira_no_enciende", "Gira con velocidad normal pero nunca llega a arrancar", "Hay giro del motor pero no se produce combustión.")
        ]
    },
    {
        "id": "sonido_motor",
        "numero": 2,
        "titulo": "2. Ruidos Anómalos del Motor",
        "descripcion": "¿Se percibe algún sonido extraño proveniente del compartimento del motor?",
        "icono": "🔊",
        "opciones": [
            ("ninguno", "Sonido suave y regular de marcha normal", "Sin ruidos metálicos ni chillidos extraños."),
            ("chirrido_agudo", "Chirrido agudo continuo o al acelerar", "Típico chillido de correa patinando en poleas."),
            ("golpeteo_metalico", "Golpeteo metálico rítmico ('tac-tac-tac') en el bloque", "Sonido seco en la parte interna del motor."),
            ("explosiones_escape", "Explosiones o petardeos en el tubo de escape", "Detonaciones irregulares en el sistema de salida.")
        ]
    },
    {
        "id": "humo_escape",
        "numero": 3,
        "titulo": "3. Color y Tipo de Humo del Escape",
        "descripcion": "¿Qué aspecto tiene el humo emitido por el tubo de escape con el motor tibio?",
        "icono": "💨",
        "opciones": [
            ("ninguno_normal", "Transparente o leve vapor blanquecino en frío", "Comportamiento normal de condensación."),
            ("humo_azul", "Humo azulado continuo con fuerte olor a aceite quemado", "Indica presencia de aceite en la cámara de combustión."),
            ("humo_blanco_denso", "Humo blanco espeso y constante con olor dulzón", "Indica ingreso de refrigerante a los cilindros."),
            ("humo_negro", "Humo negro oscuro al acelerar con olor a gasolina cruda", "Indica mezcla con exceso de combustible no quemado.")
        ]
    },
    {
        "id": "comportamiento_frenos",
        "numero": 4,
        "titulo": "4. Estado y Sensación del Pedal de Freno",
        "descripcion": "¿Cómo responde el pedal de freno al ser accionado durante la marcha?",
        "icono": "🛑",
        "opciones": [
            ("normal", "Pedal firme y frenado parejo y progresivo", "El sistema responde según los estándares del fabricante."),
            ("esponjoso_se_hunde", "Pedal blando / esponjoso que se hunde hasta el fondo", "Pérdida de presión en el circuito hidráulico."),
            ("vibracion_frenado", "Pedal y volante vibran al frenar a media o alta velocidad", "Sensación pulsante bajo el pie al reducir velocidad."),
            ("pedal_muy_duro", "Pedal extremadamente rígido y el vehículo apenas se detiene", "Falta de asistencia del servofreno (booster).")
        ]
    },
    {
        "id": "temperatura_motor",
        "numero": 5,
        "titulo": "5. Medidor de Temperatura del Motor",
        "descripcion": "¿Qué indica la aguja o testigo de temperatura en el panel de instrumentos?",
        "icono": "🌡️",
        "opciones": [
            ("normal", "Aguja estable en la mitad (aprox. 85°C - 95°C)", "Temperatura de operación óptima."),
            ("sobrecalentamiento_rojo", "Aguja en la zona roja o testigo de alta temperatura activo", "Riesgo inminente de sobrecalentamiento crítico."),
            ("nunca_sube", "La aguja permanece siempre en frío, incluso tras conducir", "El motor no alcanza su temperatura térmica normal.")
        ]
    },
    {
        "id": "fuga_fluidos",
        "numero": 6,
        "titulo": "6. Fuga o Pérdida de Líquidos",
        "descripcion": "¿Se observa algún goteo o mancha fresca en el suelo donde estuvo estacionado?",
        "icono": "💧",
        "opciones": [
            ("ninguno", "Suelo totalmente limpio y seco", "Sin presencia de fugas visibles."),
            ("aceite_oscuro", "Mancha viscosa negra o café oscuro bajo el motor", "Fuga en cárter, empaque de tapa o filtro de aceite."),
            ("refrigerante_verde_rosa", "Líquido verde, rosa o amarillo brillante de tacto acuoso", "Fuga en radiador, mangueras o bomba de agua."),
            ("liquido_frenos", "Líquido amarillento claro resbaloso cerca de las ruedas", "Fuga en caliper, bombín o latiguillo de freno.")
        ]
    },
    {
        "id": "testigo_tablero",
        "numero": 7,
        "titulo": "7. Testigos de Advertencia en el Tablero",
        "descripcion": "¿Qué testigo permanece encendido en el cuadro tras arrancar el motor?",
        "icono": "⚠️",
        "opciones": [
            ("ninguno", "Ningún testigo encendido (todos se apagan tras arrancar)", "Tablero libre de códigos de advertencia."),
            ("presion_aceite", "Luz roja con forma de lámpara de aceite (Aladdín)", "Presión de aceite insuficiente en el circuito."),
            ("check_engine", "Luz ámbar con silueta de motor (Check Engine)", "Código de falla registrado por la computadora (ECU)."),
            ("bateria_alternador", "Luz roja con símbolo de batería (+ / -)", "El alternador no está cargando el acumulador."),
            ("frenos_abs", "Luz de advertencia de freno (!) o símbolo de ABS", "Anomalía en el sistema antibloqueo o nivel de frenos.")
        ]
    },
    {
        "id": "comportamiento_direccion",
        "numero": 8,
        "titulo": "8. Respuesta de la Dirección y Alineación",
        "descripcion": "¿Cómo se comporta el volante en línea recta sobre pavimento plano?",
        "icono": "🎯",
        "opciones": [
            ("normal", "Vehículo mantiene la línea recta sin esfuerzo", "Dirección alineada y balanceada."),
            ("tira_hacia_un_lado", "El auto se desvía fuertemente hacia la izquierda o derecha", "Falta de alineación o diferencia de presión de aire."),
            ("vibra_alta_velocidad", "El volante tiembla de forma rítmica a más de 80 km/h", "Desbalanceo en las ruedas delanteras."),
            ("direccion_dura", "El volante se siente excesivamente pesado al maniobrar", "Falta de fluido hidráulico o falla en bomba/asistencia.")
        ]
    },
    {
        "id": "respuesta_aceleracion",
        "numero": 9,
        "titulo": "9. Potencia y Respuesta al Acelerador",
        "descripcion": "¿Cómo responde la aceleración al exigir potencia en subidas o adelantamientos?",
        "icono": "⚡",
        "opciones": [
            ("normal", "Aceleración progresiva y entrega de potencia firme", "Respuesta correcta del tren motriz."),
            ("tirones_jaleo", "Tirones, vacilaciones o pérdida súbita de potencia", "Falla de encendido, bujías o inyección."),
            ("perdida_potencia_subidas", "Pérdida notable de fuerza en pendientes pronunciadas", "Filtro de combustible obstruido o baja compresión."),
            ("embrague_patina", "El motor se revoluciona pero el vehículo no acelera a la par", "Desgaste del disco de embrague (transmisión manual).")
        ]
    },
    {
        "id": "tiempo_ultimo_mantenimiento",
        "numero": 10,
        "titulo": "10. Tiempo del Último Mantenimiento Preventivo",
        "descripcion": "¿Cuánto tiempo o kilometraje ha pasado desde el último servicio integral?",
        "icono": "📅",
        "opciones": [
            ("menor_6_meses", "Hace menos de 6 meses (o menos de 5,000 km)", "Vehículo con mantenimiento reciente y al día."),
            ("entre_6_y_12_meses", "Entre 6 y 12 meses (entre 5,000 km y 10,000 km)", "Próximo a requerir servicio de rutina."),
            ("mayor_1_ano_o_nunca", "Más de 1 año, kilometraje vencido o historial desconocido", "Mantenimiento preventivo gravemente postergado.")
        ]
    }
]


# ---------------------------------------------------------------------
# 2. BASE DE CONOCIMIENTO (REGLAS DE PRODUCCIÓN)
# Prioridades:
#   1 = Emergencia Crítica (Riesgo de accidente o daño irreparable al motor)
#   2 = Falla Severa (Requiere grúa o taller mecánico urgente)
#   3 = Falla Moderada (Conducción limitada, reparación recomendada)
#   4 = Mantenimiento Preventivo (Estado operacional óptimo)
# ---------------------------------------------------------------------
REGLAS = [
    {
        "id": "R01",
        "nombre": "Falta Crítica de Presión de Aceite",
        "prioridad": 1,
        "severidad": "CRÍTICA",
        "condiciones": [
            ("testigo_tablero", "presion_aceite")
        ],
        "diagnostico": "PELIGRO CRÍTICO: Pérdida Inmediata de Presión de Aceite de Motor",
        "explicacion": "El sensor de lubricación detectó que la presión del circuito de aceite cayó a niveles peligrosos. Continuar con el motor encendido provocará fundición de cojinetes y rotura de bielas en minutos.",
        "accion": "Apagar el motor de inmediato y no volver a encenderlo. Verificar nivel de aceite con la varilla. Si el nivel es correcto, la bomba de aceite falló; trasladar únicamente en grúa.",
        "costo_estimado": "Muy Alto si se ignora (reparación completa de motor)"
    },
    {
        "id": "R02",
        "nombre": "Falla Catastrófica en Frenos Hidráulicos",
        "prioridad": 1,
        "severidad": "CRÍTICA",
        "condiciones": [
            ("comportamiento_frenos", "esponjoso_se_hunde")
        ],
        "diagnostico": "EMERGENCIA DE SEGURIDAD: Falla en Circuito Hidráulico de Frenos",
        "explicacion": "El pedal esponjoso que se hunde al fondo evidencia presencia de aire en las líneas, fuga severa de líquido de frenos o falla de la bomba principal (cilindro maestro).",
        "accion": "NO CONDUCIR EL VEHÍCULO. Riesgo inminente de perder por completo la capacidad de frenado. Requiere purgado urgente y reemplazo de tuberías o cilindro maestro.",
        "costo_estimado": "Medio (reparación de seguridad obligatoria)"
    },
    {
        "id": "R03",
        "nombre": "Sobrecalentamiento Severo con Fuga de Refrigerante",
        "prioridad": 1,
        "severidad": "CRÍTICA",
        "condiciones": [
            ("temperatura_motor", "sobrecalentamiento_rojo"),
            ("fuga_fluidos", "refrigerante_verde_rosa")
        ],
        "diagnostico": "SOBRECALENTAMIENTO CRÍTICO: Fuga Masiva de Líquido Refrigerante",
        "explicacion": "El sistema de enfriamiento perdió su fluido térmico debido a rotura de manguera, radiador fisurado o falla en la bomba de agua. La temperatura extrema deforma la culata de aluminio.",
        "accion": "Detener el vehículo de forma segura y apagar el motor. NUNCA abrir la tapa del radiador en caliente (riesgo de quemaduras severas por vapor a presión). Esperar grúa.",
        "costo_estimado": "Alto si se recalentó la culata; Medio si solo es manguera"
    },
    {
        "id": "R04",
        "nombre": "Junta de Culata Quemada (Empaque de Cabeza)",
        "prioridad": 2,
        "severidad": "ALTA",
        "condiciones": [
            ("humo_escape", "humo_blanco_denso"),
            ("temperatura_motor", "sobrecalentamiento_rojo")
        ],
        "diagnostico": "ROTURA DE JUNTA DE CULATA: Filtración de Refrigerante al Motor",
        "explicacion": "El humo blanco espeso con olor dulce junto al sobrecalentamiento indica que el empaque de la culata se quemó y el líquido refrigerante se está filtrando a los cilindros.",
        "accion": "No usar el vehículo para evitar el 'bloqueo hidráulico' de los pistones y la contaminación del aceite con agua. Requiere rectificación de culata y cambio de empaque.",
        "costo_estimado": "Alto (desarme parcial de motor)"
    },
    {
        "id": "R05",
        "nombre": "Consumo y Quema Excesiva de Aceite",
        "prioridad": 2,
        "severidad": "ALTA",
        "condiciones": [
            ("humo_escape", "humo_azul"),
            ("tiempo_ultimo_mantenimiento", "mayor_1_ano_o_nunca")
        ],
        "diagnostico": "DESGASTE INTERNO: Quema de Aceite por Anillos o Retenes de Válvula",
        "explicacion": "El humo azulado es evidencia directa de aceite lubricante ingresando a la cámara de combustión, agravado por la degradación del lubricante debido a mantenimientos vencidos.",
        "accion": "Revisar y rellenar periódicamente el nivel de aceite para no secar el motor. Agendar revisión de compresión de cilindros y reemplazo de retenes de válvulas o aros de pistón.",
        "costo_estimado": "Medio a Alto según el estado de las camisas de cilindro"
    },
    {
        "id": "R06",
        "nombre": "Fallo Eléctrico de Carga o Batería Agotada",
        "prioridad": 2,
        "severidad": "ALTA",
        "condiciones": [
            ("arranque_motor", "no_gira"),
            ("testigo_tablero", "bateria_alternador")
        ],
        "diagnostico": "FALLA ELÉCTRICA: Batería Descargada o Alternador Averiado",
        "explicacion": "El motor de arranque no recibe suficiente voltaje debido a que la batería está totalmente descargada o el alternador dejó de generar carga, agotando el acumulador durante la marcha.",
        "accion": "Comprobar voltaje de batería con multímetro (debe superar 12.6V en reposo y 13.8V con alternador activo). Cargar o sustituir la batería y verificar la correa del alternador.",
        "costo_estimado": "Bajo a Medio (batería nueva o regulador de alternador)"
    },
    {
        "id": "R07",
        "nombre": "Mezcla Rica y Falla de Inyección",
        "prioridad": 2,
        "severidad": "ALTA",
        "condiciones": [
            ("humo_escape", "humo_negro"),
            ("respuesta_aceleracion", "tirones_jaleo")
        ],
        "diagnostico": "MEZCLA RICA: Exceso de Combustible no Quemado / Falla de Sensores",
        "explicacion": "El motor está recibiendo más combustible del que puede combustionar. Provoca tirones, carbonización de bujías y puede derretir el catalizador del escape.",
        "accion": "Escanear computadora OBD-II para verificar el sensor de flujo de aire (MAF), sensor de oxígeno (sonda Lambda) e inyectores de combustible que puedan estar goteando.",
        "costo_estimado": "Medio (limpieza de inyectores o cambio de sensor)"
    },
    {
        "id": "R08",
        "nombre": "Desgaste Severo de Embrague (Clutch)",
        "prioridad": 2,
        "severidad": "ALTA",
        "condiciones": [
            ("respuesta_aceleracion", "embrague_patina")
        ],
        "diagnostico": "DESGASTE DEL DISCO DE EMBRAGUE: Pérdida de Tracción Mecánica",
        "explicacion": "El disco de embrague ha perdido su material de fricción. Al acelerar, el motor sube de revoluciones pero la fuerza no se transmite eficientemente a la caja de cambios.",
        "accion": "Evitar forzar el auto en pendientes pronunciadas. Programar el reemplazo del kit de embrague (disco, plato de presión y rulemán de empuje).",
        "costo_estimado": "Medio a Alto (mano de obra intensiva para bajar caja)"
    },
    {
        "id": "R09",
        "nombre": "Patinamiento o Desgaste de Correa de Accesorios",
        "prioridad": 3,
        "severidad": "MODERADA",
        "condiciones": [
            ("sonido_motor", "chirrido_agudo")
        ],
        "diagnostico": "DESALINEACIÓN O DESGASTE DE CORREA DE ACCESORIOS (SERPENTINA)",
        "explicacion": "El chillido agudo proviene de la fricción entre la correa de goma y las poleas del alternador, bomba de agua o compresor de aire acondicionado al patinar por falta de tensión.",
        "accion": "Inspeccionar tensión y grietas en la correa de accesorios. Tensar o cambiar la correa y verificar poleas locas o tensor automático.",
        "costo_estimado": "Bajo (cambio rápido de correa de goma)"
    },
    {
        "id": "R10",
        "nombre": "Desalineación y Desbalanceo del Tren Delantero",
        "prioridad": 3,
        "severidad": "MODERADA",
        "condiciones": [
            ("comportamiento_direccion", "tira_hacia_un_lado")
        ],
        "diagnostico": "DESALINEACIÓN DE DIRECCIÓN Y SUSPENSIÓN",
        "explicacion": "Las ruedas delanteras han perdido su paralelismo geométrico, generalmente tras caer en baches o por desgaste de terminales de dirección, desgastando desigualmente los neumáticos.",
        "accion": "Llevar el vehículo a un centro de alineación computarizada y balanceo. Revisar presión de inflado uniforme en las 4 ruedas.",
        "costo_estimado": "Bajo (servicio de alineación y balanceo)"
    },
    {
        "id": "R11",
        "nombre": "Vibración por Discos de Freno Deformados",
        "prioridad": 3,
        "severidad": "MODERADA",
        "condiciones": [
            ("comportamiento_frenos", "vibracion_frenado")
        ],
        "diagnostico": "DISCOS DE FRENO ALABEADOS (DEFORMADOS POR CHOQUE TÉRMICO)",
        "explicacion": "Los discos metálicos de freno sufrieron una deformación ondulatoria, usualmente al pasar por charcos fríos tras frenadas intensas, provocando vibraciones rítmicas al frenar.",
        "accion": "Rectificar discos si están dentro del grosor mínimo de seguridad, o cambiarlos junto a un juego nuevo de pastillas de freno.",
        "costo_estimado": "Medio (rectificación o cambio de discos)"
    },
    {
        "id": "R12",
        "nombre": "Condición Operativa Regular / Mantenimiento Preventivo",
        "prioridad": 4,
        "severidad": "PREVENTIVA",
        "condiciones": [
            ("arranque_motor", "normal"),
            ("temperatura_motor", "normal")
        ],
        "diagnostico": "VEHÍCULO EN ESTADO OPERACIONAL NORMAL: Servicio Preventivo Sugerido",
        "explicacion": "No se detectaron fallas mecánicas de gravedad inmediata en los sistemas principales (motor, frenos, transmisión y temperatura).",
        "accion": "Continuar con el cronograma de revisiones preventivas periódicas (cambio de aceite y filtro cada 5,000 km, revisión de niveles y rotación de neumáticos).",
        "costo_estimado": "Bajo (mantenimiento preventivo regular)"
    }
]
