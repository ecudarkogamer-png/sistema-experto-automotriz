# AutoExpert - Sistema Experto Automotriz

Sistema experto basado en reglas diseñado para el diagnóstico de fallas mecánicas en vehículos automotores. Implementa una base de conocimiento propia, un motor de inferencia explícito dividido formalmente en tres fases (equiparación, resolución de conflictos y ejecución) y una interfaz gráfica interactiva con recolección de 10 hechos observables.

---

## Estructura del Proyecto

```text
auto_expert/
├── base_conocimiento.py        # Definición de hechos y reglas de producción
├── motor_inferencia.py         # Motor de inferencia en 3 fases (Equiparación, Resolución, Ejecución)
├── app_web.py                  # Servidor local y servicio API REST para la interfaz gráfica
├── app_tkinter.py              # Versión de interfaz gráfica local de escritorio (Tkinter)
├── main.py                     # Punto de entrada principal y pruebas automatizadas
├── static/
│   └── index.html              # Interfaz gráfica interactiva de usuario
└── README.md                   # Documentación técnica del sistema
```

---

## Base de Conocimiento

### Hechos Observables (10 Entradas)
1. `arranque_motor`: Estado del encendido (normal, gira_lento, no_gira, gira_no_enciende).
2. `sonido_motor`: Ruidos mecánicos anómalos (ninguno, chirrido_agudo, golpeteo_metalico, explosiones_escape).
3. `humo_escape`: Color del humo del escape (ninguno_normal, humo_azul, humo_blanco_denso, humo_negro).
4. `comportamiento_frenos`: Respuesta del pedal de freno (normal, esponjoso_se_hunde, vibracion_frenado, pedal_muy_duro).
5. `temperatura_motor`: Indicador térmico del motor (normal, sobrecalentamiento_rojo, nunca_sube).
6. `fuga_fluidos`: Tipo de fuga en el suelo (ninguno, aceite_oscuro, refrigerante_verde_rosa, liquido_frenos).
7. `testigo_tablero`: Testigos activos en el tablero (ninguno, presion_aceite, check_engine, bateria_alternador, frenos_abs).
8. `comportamiento_direccion`: Respuesta del volante (normal, tira_hacia_un_lado, vibra_alta_velocidad, direccion_dura).
9. `respuesta_aceleracion`: Entrega de tracción y potencia (normal, tirones_jaleo, perdida_potencia_subidas, embrague_patina).
10. `tiempo_ultimo_mantenimiento`: Antigüedad del servicio (menor_6_meses, entre_6_y_12_meses, mayor_1_ano_o_nunca).

### Reglas de Producción

| ID | Prioridad | Severidad | Diagnóstico Emitido |
| :---: | :---: | :---: | :--- |
| **R01** | 1 | CRÍTICA | Falta Crítica de Presión de Aceite de Motor |
| **R02** | 1 | CRÍTICA | Falla Catastrófica en Circuito Hidráulico de Frenos |
| **R03** | 1 | CRÍTICA | Sobrecalentamiento Severo con Fuga Masiva de Refrigerante |
| **R04** | 2 | ALTA | Rotura de Junta de Culata (Filtración de Refrigerante) |
| **R05** | 2 | ALTA | Consumo y Quema de Aceite por Anillos o Retenes |
| **R06** | 2 | ALTA | Falla Eléctrica de Batería o Alternador |
| **R07** | 2 | ALTA | Mezcla Rica y Falla de Inyección / Sensores |
| **R08** | 2 | ALTA | Desgaste del Disco de Embrague (Clutch) |
| **R09** | 3 | MODERADA | Patinamiento o Desgaste de Correa de Accesorios |
| **R10** | 3 | MODERADA | Desalineación y Desbalanceo del Tren Delantero |
| **R11** | 3 | MODERADA | Discos de Freno Alabeados (Deformados) |
| **R12** | 4 | PREVENTIVA | Vehículo en Estado Operacional Normal |

---

## Arquitectura del Motor de Inferencia

El motor de inferencia ejecuta el ciclo clásico de razonamiento hacia adelante en tres etapas consecutivas:

1. **Fase 1: Equiparación (Pattern Matching)**:
   Evalúa los antecedentes de las 12 reglas contra los hechos ingresados en la memoria de trabajo. Las reglas cuyas condiciones se satisfacen en su totalidad pasan a conformar el Conjunto Conflicto (*Conflict Set*).

2. **Fase 2: Resolución de Conflictos (Conflict Resolution)**:
   Aplica criterios de desempate deterministas para seleccionar la regla activa:
   - Criterio de Prioridad de Severidad (Prioridad 1 > 2 > 3 > 4).
   - Criterio de Especificidad (se prioriza la regla con mayor cantidad de condiciones antecedentes).

3. **Fase 3: Ejecución (Act)**:
   Dispara la regla ganadora, emite el diagnóstico correspondiente, define las acciones correctivas recomendadas y construye la traza de auditoría del razonamiento.

---

## Instrucciones de Ejecución

### Requisitos
- Python 3.8 o superior.
- Utiliza únicamente módulos de la biblioteca estándar de Python (no requiere instalación de paquetes con `pip`).

### 1. Iniciar la Interfaz Gráfica
Ejecutar desde el directorio del proyecto:

```bash
python main.py
```

El servidor local se iniciará y abrirá automáticamente la interfaz gráfica interactiva en el navegador web predeterminado (`http://127.0.0.1:8080/`).

### 2. Ejecutar Pruebas Automatizadas
Para verificar el motor de inferencia y la resolución de las 3 fases mediante pruebas unitarias:

```bash
python main.py --test
```

### 3. Interfaz de Escritorio Tkinter (Opcional)
Si el entorno cuenta con soporte nativo para Tkinter:

```bash
python main.py --tkinter
```
