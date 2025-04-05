import socket
import threading
import argparse
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor  # Thread pool for better management

# Lists to store the results
total_puertos_abiertos = []
total_puertos_cerrados = []
lock = threading.Lock()  # Prevents errors when multiple threads write to the lists


def escanear_puerto(ip, puerto):
    """
    Scans a specific port on a given IP.
    Returns the result as a string.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Timeout of 0.5 seconds
            if s.connect_ex((ip, puerto)) == 0:  # 0 means Successful connection
                return f"[+++] {ip}:{puerto} OPEN"
            else:
                return f"[-] {ip}:{puerto} CLOSED"
    except Exception as e:
        print(f"Error scanning {ip}:{puerto}: {e}")
        return None


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

    print("Starting scan...")
    resultados = []  # List to store results in order

    # Use a thread pool for better threading management
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for i in tqdm(range(1, 256), desc="Scan progress"):
            ip = f"{rango_ip}.{i}"  # Build the full IP
            for puerto in puertos:
                futures.append(executor.submit(escanear_puerto, ip, puerto))

        # Collect results in order
        for future in futures:
            resultado = future.result()
            if resultado:
                resultados.append(resultado)

    # Separate results into open and closed ports
    for resultado in resultados:
        if "OPEN" in resultado:
            total_puertos_abiertos.append(resultado)
        else:
            total_puertos_cerrados.append(resultado)

    # Display the scan results
    print("\n--- SCAN RESULTS ---")
    if total_puertos_abiertos:
        print("\nOpen Ports:")
        for resultado in total_puertos_abiertos:
            print(resultado)
    else:
        print("No open ports found.")
    
    # Save the results to separate files
    guardar_resultados()


def guardar_resultados():
    """
    Saves the scan results to two separate text files.
    One for open ports and another for closed ports.
    """
    try:
        with open("open_ports.txt", "w") as archivo_abiertos:
            archivo_abiertos.write("--- OPEN PORTS ---\n")
            archivo_abiertos.writelines(f"{linea}\n" for linea in total_puertos_abiertos)
        print("Open ports saved to 'open_ports.txt'.")

        with open("closed_ports.txt", "w") as archivo_cerrados:
            archivo_cerrados.write("--- CLOSED PORTS ---\n")
            archivo_cerrados.writelines(f"{linea}\n" for linea in total_puertos_cerrados)
        print("Closed ports saved to 'closed_ports.txt'.")
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
