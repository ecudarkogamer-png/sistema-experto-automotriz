# =====================================================================
# SISTEMA EXPERTO AUTOMOTRIZ: AUTOEXPERT
# Módulo: Interfaz Gráfica de Escritorio (Tkinter / TTK)
# =====================================================================

"""
Este módulo implementa la interfaz gráfica nativa de escritorio en Tkinter.
Presenta el asistente interactivo de 10 pasos con botones de opción (Radiobuttons),
barra de progreso y pantalla de resultados con trazabilidad del razonamiento.
"""

import sys
from typing import Dict, Any

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    print("[AVISO] Tkinter no está disponible en este entorno de Python.")
    print("        Por favor ejecute 'python app_web.py' o 'python main.py'")
    print("        para usar la interfaz gráfica web nativa.")
    sys.exit(1)

from base_conocimiento import PREGUNTAS_HECHOS, REGLAS
from motor_inferencia import MotorInferencia


class AutoExpertTkinterApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AutoExpert - Sistema Experto Automotriz")
        self.root.geometry("820x680")
        self.root.minsize(780, 600)
        self.root.configure(bg="#0f172a")

        self.motor = MotorInferencia(REGLAS)
        self.current_step = 0
        self.user_answers: Dict[str, str] = {}
        self.selected_var = tk.StringVar()

        self._configure_styles()
        self._build_ui()
        self._show_step(0)

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configurar colores del tema oscuro
        style.configure("TProgressbar", thickness=10, troughcolor="#1e293b", background="#2563eb")
        style.configure("TNotebook", background="#0f172a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1e293b", foreground="#94a3b8", padding=[12, 6], font=("Helvetica", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#2563eb")], foreground=[("selected", "#ffffff")])

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#0f172a", pady=16)
        header_frame.pack(fill="x")

        title_lbl = tk.Label(
            header_frame,
            text="🚗 AutoExpert",
            font=("Helvetica", 22, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )
        title_lbl.pack()

        badge_lbl = tk.Label(
            header_frame,
            text=" SISTEMA EXPERTO BASADO EN REGLAS ",
            font=("Helvetica", 8, "bold"),
            fg="#38bdf8",
            bg="#1e293b",
            relief="groove",
            bd=1
        )
        badge_lbl.pack(pady=4)

        sub_lbl = tk.Label(
            header_frame,
            text="Diagnóstico Mecánico y Asesor de Seguridad Automotriz (10 Pasos)",
            font=("Helvetica", 10),
            fg="#94a3b8",
            bg="#0f172a"
        )
        sub_lbl.pack()

        # Contenedor central (Card)
        self.card_frame = tk.Frame(self.root, bg="#1e293b", bd=1, relief="ridge", padx=24, pady=20)
        self.card_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # Marco del Asistente
        self.wizard_frame = tk.Frame(self.card_frame, bg="#1e293b")
        self.wizard_frame.pack(fill="both", expand=True)

        # Progreso
        prog_frame = tk.Frame(self.wizard_frame, bg="#1e293b")
        prog_frame.pack(fill="x", pady=(0, 15))

        self.step_counter_lbl = tk.Label(
            prog_frame,
            text="Pregunta 1 de 10",
            font=("Helvetica", 10, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        self.step_counter_lbl.pack(side="left")

        self.percent_lbl = tk.Label(
            prog_frame,
            text="10% Completado",
            font=("Helvetica", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        self.percent_lbl.pack(side="right")

        self.progress_bar = ttk.Progressbar(self.wizard_frame, style="TProgressbar", maximum=100)
        self.progress_bar.pack(fill="x", pady=(0, 15))

        # Título y descripción de la pregunta
        self.q_title_lbl = tk.Label(
            self.wizard_frame,
            text="",
            font=("Helvetica", 13, "bold"),
            fg="#38bdf8",
            bg="#1e293b",
            anchor="w",
            justify="left"
        )
        self.q_title_lbl.pack(fill="x")

        self.q_desc_lbl = tk.Label(
            self.wizard_frame,
            text="",
            font=("Helvetica", 10),
            fg="#cbd5e1",
            bg="#1e293b",
            anchor="w",
            justify="left",
            wraplength=700
        )
        self.q_desc_lbl.pack(fill="x", pady=(4, 15))

        # Opciones de respuesta (Radiobuttons)
        self.options_container = tk.Frame(self.wizard_frame, bg="#1e293b")
        self.options_container.pack(fill="both", expand=True, pady=5)

        # Barra de navegación
        nav_frame = tk.Frame(self.wizard_frame, bg="#1e293b", pady=10)
        nav_frame.pack(fill="x", side="bottom")

        self.btn_prev = tk.Button(
            nav_frame,
            text="« Anterior",
            font=("Helvetica", 10, "bold"),
            bg="#334155",
            fg="#ffffff",
            activebackground="#475569",
            activeforeground="#ffffff",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._prev_step
        )
        self.btn_prev.pack(side="left")

        self.btn_next = tk.Button(
            nav_frame,
            text="Siguiente »",
            font=("Helvetica", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            bd=0,
            padx=18,
            pady=8,
            cursor="hand2",
            command=self._next_step
        )
        self.btn_next.pack(side="right")

        # Marco de Resultados (Oculto inicialmente)
        self.results_frame = tk.Frame(self.card_frame, bg="#1e293b")

    def _show_step(self, step_index: int):
        self.current_step = step_index
        q = PREGUNTAS_HECHOS[self.current_step]

        # Actualizar contadores
        self.step_counter_lbl.config(text=f"Pregunta {self.current_step + 1} de {len(PREGUNTAS_HECHOS)}")
        percent = int(((self.current_step + 1) / len(PREGUNTAS_HECHOS)) * 100)
        self.percent_lbl.config(text=f"{percent}% Completado")
        self.progress_bar["value"] = percent

        # Actualizar textos
        self.q_title_lbl.config(text=f"{q['icono']} {q['titulo']}")
        self.q_desc_lbl.config(text=q["descripcion"])

        # Limpiar opciones anteriores
        for widget in self.options_container.winfo_children():
            widget.destroy()

        # Cargar valor previo si existe
        current_val = self.user_answers.get(q["id"], "")
        self.selected_var.set(current_val)

        # Generar radio buttons
        for val, label, subtext in q["opciones"]:
            opt_box = tk.Frame(self.options_container, bg="#0f172a", bd=1, relief="solid", padx=12, pady=10)
            opt_box.pack(fill="x", pady=5)

            rb = tk.Radiobutton(
                opt_box,
                text=label,
                value=val,
                variable=self.selected_var,
                font=("Helvetica", 10, "bold"),
                fg="#f8fafc",
                bg="#0f172a",
                activebackground="#0f172a",
                activeforeground="#38bdf8",
                selectcolor="#0f172a",
                anchor="w",
                cursor="hand2",
                command=lambda v=val: self._on_select_option(q["id"], v)
            )
            rb.pack(fill="x")

            sub_lbl = tk.Label(
                opt_box,
                text=subtext,
                font=("Helvetica", 8),
                fg="#94a3b8",
                bg="#0f172a",
                anchor="w"
            )
            sub_lbl.pack(fill="x", padx=24)

        # Actualizar botones
        self.btn_prev.config(state="normal" if self.current_step > 0 else "disabled")
        if self.current_step == len(PREGUNTAS_HECHOS) - 1:
            self.btn_next.config(text="🔍 Analizar y Diagnosticar", bg="#059669", activebackground="#047857")
        else:
            self.btn_next.config(text="Siguiente »", bg="#2563eb", activebackground="#1d4ed8")

    def _on_select_option(self, fact_id: str, val: str):
        self.user_answers[fact_id] = val

    def _prev_step(self):
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _next_step(self):
        q = PREGUNTAS_HECHOS[self.current_step]
        if q["id"] not in self.user_answers:
            messagebox.showwarning("Atención", "Por favor seleccione una opción para continuar.")
            return

        if self.current_step < len(PREGUNTAS_HECHOS) - 1:
            self._show_step(self.current_step + 1)
        else:
            self._run_inference()

    def _run_inference(self):
        resultado = self.motor.ejecutar_inferencia(self.user_answers)
        self._display_results(resultado)

    def _display_results(self, res):
        self.wizard_frame.pack_forget()
        self.results_frame.pack(fill="both", expand=True)

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Banner de severidad
        colores = {
            "CRÍTICA": ("#ef4444", "#ffffff", "🚨"),
            "ALTA": ("#f59e0b", "#0f172a", "⚠️"),
            "MODERADA": ("#06b6d4", "#0f172a", "🔧"),
            "PREVENTIVA": ("#10b981", "#ffffff", "✅")
        }
        bg_col, fg_col, icon = colores.get(res.severidad, ("#334155", "#ffffff", "ℹ️"))

        banner = tk.Frame(self.results_frame, bg=bg_col, padx=16, pady=12)
        banner.pack(fill="x", pady=(0, 15))

        tk.Label(banner, text=f"{icon} SEVERIDAD: {res.severidad}", font=("Helvetica", 9, "bold"), bg=bg_col, fg=fg_col).pack(anchor="w")
        tk.Label(banner, text=res.diagnostico, font=("Helvetica", 13, "bold"), bg=bg_col, fg=fg_col, wraplength=700, justify="left").pack(anchor="w", pady=(3, 0))

        # Pestañas de detalle
        notebook = ttk.Notebook(self.results_frame)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Informe
        tab_info = tk.Frame(notebook, bg="#0f172a", padx=16, pady=12)
        notebook.add(tab_info, text="📋 Dictamen y Recomendaciones")

        tk.Label(tab_info, text="Explicación Técnica:", font=("Helvetica", 10, "bold"), fg="#38bdf8", bg="#0f172a").pack(anchor="w")
        tk.Label(tab_info, text=res.explicacion, font=("Helvetica", 9), fg="#cbd5e1", bg="#0f172a", wraplength=680, justify="left").pack(anchor="w", pady=(2, 10))

        tk.Label(tab_info, text="Acción Inmediata:", font=("Helvetica", 10, "bold"), fg="#38bdf8", bg="#0f172a").pack(anchor="w")
        tk.Label(tab_info, text=res.accion, font=("Helvetica", 9), fg="#cbd5e1", bg="#0f172a", wraplength=680, justify="left").pack(anchor="w", pady=(2, 10))

        tk.Label(tab_info, text="Costo Estimado:", font=("Helvetica", 10, "bold"), fg="#38bdf8", bg="#0f172a").pack(anchor="w")
        tk.Label(tab_info, text=res.costo_estimado, font=("Helvetica", 9), fg="#cbd5e1", bg="#0f172a").pack(anchor="w", pady=(2, 10))

        # Tab 2: Traza del motor
        tab_trace = tk.Frame(notebook, bg="#0f172a", padx=12, pady=10)
        notebook.add(tab_trace, text="⚙️ Traza del Motor (3 Fases)")

        txt_trace = tk.Text(tab_trace, bg="#0f172a", fg="#94a3b8", font=("Consolas", 8), bd=0)
        txt_trace.pack(fill="both", expand=True)

        for traza in res.trazas:
            txt_trace.insert("end", f"=== {traza.nombre} ===\n", "header")
            txt_trace.insert("end", f"{traza.descripcion}\n\n")
            for det in traza.detalles:
                txt_trace.insert("end", f"  {det}\n")
            txt_trace.insert("end", "\n")

        txt_trace.tag_config("header", foreground="#38bdf8", font=("Consolas", 9, "bold"))
        txt_trace.config(state="disabled")

        # Botón para reiniciar
        btn_frame = tk.Frame(self.results_frame, bg="#1e293b", pady=10)
        btn_frame.pack(fill="x")

        btn_restart = tk.Button(
            btn_frame,
            text="🔄 Iniciar Nuevo Diagnóstico",
            font=("Helvetica", 10, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self._restart
        )
        btn_restart.pack(side="left")

    def _restart(self):
        self.user_answers.clear()
        self.results_frame.pack_forget()
        self.wizard_frame.pack(fill="both", expand=True)
        self._show_step(0)


def iniciar_app_tkinter():
    root = tk.Tk()
    app = AutoExpertTkinterApp(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_app_tkinter()
