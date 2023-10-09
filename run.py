import subprocess
import psutil

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()


def kill_processes_on_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.connections()
            for conn in connections:
                if conn.laddr.port == port:
                    print(f"Killing process {proc.name()} (PID: {proc.pid})")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

# Matando procesos en el puerto 8765
kill_processes_on_port(8765)

# Matando procesos en el puerto 8766
kill_processes_on_port(8766)

if __name__ == "__main__":
    # Comando para ejecutar "python -m http.server" en el puerto 8766
    #http_server_command = "python -m http.server 8766"

    # Comando para ejecutar "uvicorn app:app --reload" en el puerto 8765
    uvicorn_command = "uvicorn app:app --host 0.0.0.0 --port 8765"


    #Ejecutar ambos comandos en segundo plano
    #run_command(http_server_command + " &")
    run_command(uvicorn_command)