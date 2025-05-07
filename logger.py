import datetime
import os

def log_evento(evento, arquivo="log_portaria_virtual.log"):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    caminho = os.path.join(os.path.dirname(__file__), arquivo)
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {evento}\n")
