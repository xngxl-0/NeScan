import socket
import threading
import argparse
from tqdm import tqdm  # Progress bar


# Lists to store the results
total_puertos_abiertos = []
total_puertos_cerrados = []
lock = threading.Lock()  # Prevents errors when multiple threads write to the lists


def escanear_puerto(ip, puerto):
    """
    Scans a specific port on a given IP.
    If the port is open, it adds it to the open ports list.
    If it's closed, it adds it to the closed ports list.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Timeout of 0.5 seconds
            if s.connect_ex((ip, puerto)) == 0:  # Successful connection
                with lock:  # Lock to avoid conflicts when writing to the list
                    total_puertos_abiertos.append(f"[+++] {ip}:{puerto} OPEN")
            else:
                with lock:
                    total_puertos_cerrados.append(f"[-] {ip}:{puerto} CLOSED")
    except Exception as e:
        print(f"Error scanning {ip}:{puerto}: {e}")


def validar_ip(ip):
    """
    Checks if an IP address is valid.
    Returns True if the IP format is correct, False otherwise.
    """
    partes = ip.split(".")
    return len(partes) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in partes)


def escanear_rango_ips(rango_ip, puertos):
    """
    Scans a range of IPs in a given network.
    Calls 'escanear_puerto' for each combination of IP and port.
    """
    if not validar_ip(f"{rango_ip}.1"):  # Make sure the base IP is valid
        print(f"Error: The IP range '{rango_ip}' is not valid.")
        return

    hilos = []  # List to store threads
    print("Starting scan...")
    
    # Iterate over the IPs in the range (e.g., 192.168.1.1 to 192.168.1.255)
    for i in tqdm(range(1, 256), desc="Scan progress"):
        ip = f"{rango_ip}.{i}"  # Build the full IP
        
        for puerto in puertos:
            # Create a thread to scan each port on the current IP
            hilo = threading.Thread(target=escanear_puerto, args=(ip, puerto))
            hilos.append(hilo)
            hilo.start()  # Start the thread
    
    # Wait for all threads to finish
    for hilo in hilos:
        hilo.join()

    # Display the scan results
    print("\n--- SCAN RESULTS ---")
    if total_puertos_abiertos:
        print("\nOpen Ports:")
        for resultado in total_puertos_abiertos:
            print(resultado)
    else:
        print("No open ports found.")
    
    # Save the results to a file
    guardar_resultados()


def guardar_resultados():
    """
    Saves the scan results to a text file.
    Creates two sections: one for open ports and another for closed ports.
    """
    try:
        with open("resultados_escaner.txt", "w") as archivo:
            archivo.write("--- OPEN PORTS ---\n")
            archivo.writelines(f"{linea}\n" for linea in total_puertos_abiertos)
            archivo.write("\n--- CLOSED PORTS ---\n")
            archivo.writelines(f"{linea}\n" for linea in total_puertos_cerrados)
        print("Results saved to 'resultados_escaner.txt'.")
    except IOError as e:
        print(f"Error saving results: {e}")


def main():
    """
    Main function that handles command-line arguments and runs the scan.
    Calls `escanear_rango_ips` with the parameters provided by the user.
    """
    parser = argparse.ArgumentParser(description="TCP port scanner for a local network.")
    parser.add_argument("rango_ip", help="Network IP range (e.g., 192.168.1)")
    parser.add_argument("puertos", nargs="+", type=int, help="List of ports to scan, separated by spaces (e.g., 22 80 443)")
    args = parser.parse_args()

    try:
        # Call the function that performs the IP range scan
        escanear_rango_ips(args.rango_ip, args.puertos)
    except Exception as e:
        print(f"Error during the scan: {e}")


if __name__ == "__main__":
    main()
