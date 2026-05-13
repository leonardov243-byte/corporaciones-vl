import sys
import datetime
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    _COLOR = True
except ImportError:
    _COLOR = False
    class Fore:
        CYAN = GREEN = YELLOW = RED = MAGENTA = BLUE = WHITE = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_LOG_PATH = os.path.join(_BASE_DIR, "historial_vl.txt")

_LEVELS = {
    "INFO":     ("◈", Fore.CYAN,    "INFO    "),
    "SUCCESS":  ("✔", Fore.GREEN,   "SUCCESS "),
    "WARNING":  ("⚠", Fore.YELLOW,  "WARNING "),
    "ERROR":    ("✖", Fore.RED,     "ERROR   "),
    "CRITICAL": ("☠", Fore.MAGENTA, "CRITICAL"),
}

_BANNER = """\
╔══════════════════════════════════════════════════════════╗
║          C O R P O R A C I O N E S   V L                ║
║                Sistema de Registro  v1.0                 ║
╚══════════════════════════════════════════════════════════╝"""


def _ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _write(line):
    with open(_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log(nivel, mensaje):
    nivel = nivel.upper()
    icon, color, label = _LEVELS.get(nivel, _LEVELS["INFO"])
    ts = _ts()

    _write(f"[{ts}]  {label}  │  {mensaje}")

    if _COLOR:
        print(
            f"{Style.DIM}[{ts}]{Style.RESET_ALL}  "
            f"{color}{Style.BRIGHT}{icon} {label}{Style.RESET_ALL}  "
            f"{mensaje}"
        )
    else:
        print(f"[{ts}]  {icon} {label}  {mensaje}")


def iniciar_sesion():
    ts = _ts()
    sep = "═" * 58
    _write(f"\n{sep}")
    _write(f"  NUEVA SESIÓN  —  {ts}")
    _write(f"{sep}")

    if _COLOR:
        print(Fore.BLUE + Style.BRIGHT + _BANNER + Style.RESET_ALL)
    else:
        print(_BANNER)

    log("INFO", "Sistema Corporaciones VL iniciado y en línea.")


def info(m):     log("INFO", m)
def success(m):  log("SUCCESS", m)
def warning(m):  log("WARNING", m)
def error(m):    log("ERROR", m)
def critical(m): log("CRITICAL", m)


if __name__ == "__main__":
    iniciar_sesion()
    success("Conexión a base de datos establecida.")
    warning("Acceso al panel admin desde 127.0.0.1")
    error("Fallo de prueba: esto es un ejemplo.")
    critical("Prueba de alerta crítica del sistema.")
