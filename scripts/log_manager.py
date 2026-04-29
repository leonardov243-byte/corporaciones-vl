import datetime
import os

def registrar_evento(mensaje):
    # Esto busca la carpeta donde está el script para guardar el archivo ahí mismo
    ruta_carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_log = os.path.join(ruta_carpeta, "historial_vl.txt")
    
    # Obtener la fecha y hora actual
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Escribir en el archivo (la 'a' es para añadir sin borrar lo anterior)
    with open(ruta_log, "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha_hora}] - {mensaje}\n")
    
    print(f"✅ Registrado en AWS: {mensaje}")

# --- Prueba del sistema ---
if __name__ == "__main__":
    registrar_evento("Sesión iniciada: El sistema de Corporaciones VL está online.")