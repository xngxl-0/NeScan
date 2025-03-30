import socket
import threading
import argparse
from tqdm import tqdm  # Barra de progreso


# Listas para almacenar los resultados
total_puertos_abiertos = []
total_puertos_cerrados = []
lock = threading.Lock()  # Evita errores al escribir en listas desde múltiples hilos


def escanear_puerto(ip, puerto):
    """Escanea un puerto específico en una IP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Tiempo de espera de 0.5 segundos
            if s.connect_ex((ip, puerto)) == 0:  # Conexión exitosa
                with lock:
                    total_puertos_abiertos.append(f"[+++] {ip}:{puerto} ABIERTO")
            else:
                with lock:
                    total_puertos_cerrados.append(f"[-] {ip}:{puerto} CERRADO")
    except Exception as e:
        print(f"Error al escanear {ip}:{puerto}: {e}")


def validar_ip(ip):
    """Valida si una dirección IP es correcta."""
    partes = ip.split(".")
    return len(partes) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in partes)


def escanear_rango_ips(rango_ip, puertos):
    """Escanea un rango de IPs en una red dada."""
    if not validar_ip(f"{rango_ip}.1"):  # Verifica que la IP base es válida
        print(f"Error: El rango de IP '{rango_ip}' no es válido.")
        return
 
    hilos = []
    print("Iniciando escaneo...")
    
    # Iteramos sobre las IPs del rango (192.168.1.1 hasta 192.168.1.255)
    for i in tqdm(range(1, 256), desc="Progreso del escaneo"):
        ip = f"{rango_ip}.{i}"
        
        for puerto in puertos:
            hilo = threading.Thread(target=escanear_puerto, args=(ip, puerto))
            hilos.append(hilo)
            hilo.start()
    
    for hilo in hilos:
        hilo.join()

    print("\n--- RESULTADOS DEL ESCANEO ---")
    if total_puertos_abiertos:
        print("\nPuertos Abiertos:")
        for resultado in total_puertos_abiertos:
            print(resultado)
    else:
        print("No se encontraron puertos abiertos.")
    
    guardar_resultados()


def guardar_resultados():
    """Guarda los resultados en un archivo de texto."""
    try:
        with open("resultados_escaner.txt", "w") as archivo:
            archivo.write("--- PUERTOS ABIERTOS ---\n")
            archivo.writelines(f"{linea}\n" for linea in total_puertos_abiertos)
            archivo.write("\n--- PUERTOS CERRADOS ---\n")
            archivo.writelines(f"{linea}\n" for linea in total_puertos_cerrados)
        print("Resultados guardados en 'resultados_escaner.txt'.")
    except IOError as e:
        print(f"Error al guardar los resultados: {e}")


def main():
    """Función principal que maneja los argumentos y ejecuta el escaneo."""
    parser = argparse.ArgumentParser(description="Escáner de puertos TCP en una red local.")
    parser.add_argument("rango_ip", help="Rango de IPs de red (Ej: 192.168.1)")
    parser.add_argument("puertos", nargs="+", type=int, help="Lista de puertos a escanear separados por espacio (Ej: 22 80 443)")
    args = parser.parse_args()

    try:
        escanear_rango_ips(args.rango_ip, args.puertos)
    except Exception as e:
        print(f"Error durante el escaneo: {e}")


if __name__ == "__main__":
    main()
