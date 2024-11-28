import subprocess
import time
import os
import sys

# Define rutas absolutas para los scripts
base_dir = os.path.dirname(os.path.abspath(__file__))
scripts = [
    os.path.join(base_dir, "departamentos/depto1.py"),
    os.path.join(base_dir, "departamentos/depto2.py"),
    os.path.join(base_dir, "control/hvac_control.py"),
    os.path.join(base_dir, "monitoreo/monitor.py"),
    

]

processes = []

def start_scripts():
    """Inicia todos los scripts en procesos independientes."""
    global processes
    for script in scripts:
        print(f"[MAIN] Iniciando {script}...")
        process = subprocess.Popen(
    [sys.executable, script],  # sys.executable usa el mismo intérprete de Python en ejecución
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
    env=os.environ.copy()
)
        processes.append((script, process))
        time.sleep(5)  # Retraso para evitar conflictos

import threading

def stream_reader(pipe, callback):
    """Lee las líneas de un flujo (pipe) y ejecuta un callback por cada línea."""
    for line in iter(pipe.readline, ''):
        callback(line.strip())
    pipe.close()

def monitor_processes():
    """Monitorea las salidas de los procesos en tiempo real usando hilos."""
    global processes
    try:
        threads = []
        for script, process in processes:
            # Maneja stdout
            t_stdout = threading.Thread(
                target=stream_reader,
                args=(process.stdout, lambda line: print(f"[{script}][STDOUT]: {line}"))
            )
            t_stdout.daemon = True
            t_stdout.start()
            threads.append(t_stdout)

            # Maneja stderr
            t_stderr = threading.Thread(
                target=stream_reader,
                args=(process.stderr, lambda line: print(f"[{script}][STDERR]: {line}"))
            )
            t_stderr.daemon = True
            t_stderr.start()
            threads.append(t_stderr)

        # Mantén el proceso principal corriendo
        while any(t.is_alive() for t in threads):
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n[MAIN] Interrupción detectada. Cerrando...")

def stop_scripts():
    """Detiene todos los scripts en ejecución."""
    global processes
    print("[MAIN] Deteniendo todos los procesos...")
    for script, process in processes:
        process.terminate()
        stdout, stderr = process.communicate(timeout=5)
        if stdout:
            print(f"[{script}][STDOUT Final]: {stdout.strip()}")
        if stderr:
            print(f"[{script}][STDERR Final]: {stderr.strip()}")
    processes = []

if __name__ == "__main__":
    try:
        start_scripts()
        print("[MAIN] Todos los procesos iniciados. Presiona Ctrl+C para detener.")
        monitor_processes()
    finally:
        stop_scripts()
        print("[MAIN] Sistema detenido correctamente.")
