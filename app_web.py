# =====================================================================
# SISTEMA EXPERTO AUTOMOTRIZ: AUTOEXPERT
# Módulo: Servidor de Interfaz Gráfica Web Local
# =====================================================================

"""
Este módulo implementa el servidor web local utilizando exclusivamente
la biblioteca estándar de Python (http.server, json, webbrowser, threading).
No requiere dependencias externas como pip, Flask o Streamlit.

Al ejecutarse, levanta el servicio local y abre de inmediato la interfaz
gráfica en el navegador web predeterminado del usuario.
"""

import http.server
import json
import os
import sys
import threading
import urllib.parse
import webbrowser
from typing import Dict, Any

from base_conocimiento import PREGUNTAS_HECHOS, REGLAS
from motor_inferencia import MotorInferencia

# Inicializar motor de inferencia con la base de reglas
motor = MotorInferencia(REGLAS)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


class AutoExpertHandler(http.server.SimpleHTTPRequestHandler):
    """Manejador HTTP para la API de inferencia y la interfaz gráfica."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):
        """Maneja solicitudes GET para la interfaz gráfica y la lista de preguntas."""
        parsed_url = urllib.parse.urlparse(self.path)

        if parsed_url.path == "/" or parsed_url.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(STATIC_DIR, "index.html"), "rb") as f:
                self.wfile.write(f.read())
            return

        elif parsed_url.path == "/api/preguntas":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            payload = json.dumps(PREGUNTAS_HECHOS, ensure_ascii=False)
            self.wfile.write(payload.encode("utf-8"))
            return

        elif parsed_url.path == "/api/reglas":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            payload = json.dumps(REGLAS, ensure_ascii=False)
            self.wfile.write(payload.encode("utf-8"))
            return

        # Servir archivos estáticos por defecto
        super().do_GET()

    def do_POST(self):
        """Maneja solicitudes POST para ejecutar la inferencia experta."""
        parsed_url = urllib.parse.urlparse(self.path)

        if parsed_url.path == "/api/diagnosticar":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode("utf-8"))
                hechos = data.get("hechos", {})

                # Ejecutar el ciclo de las 3 fases en el motor
                resultado = motor.ejecutar_inferencia(hechos)

                # Construir respuesta serializable
                respuesta = {
                    "exito": resultado.exito,
                    "diagnostico": resultado.diagnostico,
                    "severidad": resultado.severidad,
                    "explicacion": resultado.explicacion,
                    "accion": resultado.accion,
                    "costo_estimado": resultado.costo_estimado,
                    "regla_disparada": resultado.regla_disparada,
                    "cantidad_candidatas": len(resultado.conjunto_conflicto),
                    "trazas": [
                        {
                            "nombre": t.nombre,
                            "descripcion": t.descripcion,
                            "detalles": t.detalles
                        }
                        for t in resultado.trazas
                    ],
                    "hechos_analizados": resultado.hechos_analizados
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(respuesta, ensure_ascii=False).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                error_resp = {"error": str(e)}
                self.wfile.write(json.dumps(error_resp).encode("utf-8"))
            return

        self.send_error(404, "Endpoint no encontrado")

    def log_message(self, format, *args):
        """Suprimir registros innecesarios en consola para una salida limpia."""
        return


def iniciar_servidor(puerto: int = 8080, abrir_navegador: bool = True):
    """Inicia el servidor local y abre la interfaz en el navegador."""
    server_address = ("127.0.0.1", puerto)

    # Intentar puertos alternativos si 8080 está ocupado
    for p in range(puerto, puerto + 10):
        try:
            httpd = http.server.ThreadingHTTPServer(("127.0.0.1", p), AutoExpertHandler)
            puerto = p
            break
        except OSError:
            continue
    else:
        print("[ERROR] No se pudo encontrar un puerto libre entre 8080 y 8090.")
        sys.exit(1)

    url = f"http://127.0.0.1:{puerto}/"
    print("=" * 65)
    print("SISTEMA EXPERTO AUTOMOTRIZ: AUTOEXPERT")
    print("=" * 65)
    print(f"-> Servidor grafico activo en: {url}")
    print("-> Abriendo interfaz grafica en su navegador web...")
    print("-> Presione Ctrl + C en esta consola para detener el sistema.")
    print("=" * 65)

    if abrir_navegador:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Servidor detenido por el usuario.")
        httpd.server_close()


if __name__ == "__main__":
    iniciar_servidor()
