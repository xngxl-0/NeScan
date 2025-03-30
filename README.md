# TCP Port Scanner for Local Networks

Welcome to the TCP Port Scanner project! This is a simple yet powerful tool for scanning ports on devices within a local network. It's perfect for network administrators, security researchers, or anyone curious about the status of ports in their network.

## What does this program do?

This scanner checks a local network for open and closed ports on devices within a specified IP range. You can specify which ports to scan (e.g., port 22 for SSH, 80 for HTTP, or 443 for HTTPS), and the program handles the rest.

## Features

- **Multithreaded scanning**: Scans multiple IPs and ports simultaneously for faster results.
- **Detailed results**: Displays results in real-time and saves them to a text file for future reference.
- **IP range compatibility**: Scans entire IP ranges within your network (e.g., 192.168.1.1 - 192.168.1.255).

## How it works

- **Port scanning**: The program checks if the specified ports are open or closed on each device in the given IP range.
- **Multithreading**: Uses multiple threads to speed up the scanning process.
- **Results saved**: After the scan, results are saved to a file named `resultados_escaner.txt`.

## Requirements

To run this script, you'll need the following Python libraries:

- `socket`: For handling network connections.
- `threading`: To enable multithreaded scanning.
- `argparse`: For handling command-line arguments.
- `tqdm`: To display a progress bar during the scan.

### Install the required dependencies:

```bash
pip install tqdm
```

## How to use the program

1. **Clone or download the project**: If you haven't already, clone the repository or download it as a ZIP file.

2. **Run the script from the command line**:

   Navigate to the project directory and use the following command:

   ```bash
   python NeScan.py <ip_range> <ports>
   ```

   - `ip_range`: The IP range of the network you want to scan (e.g., `192.168.1` to scan `192.168.1.1 - 192.168.1.255`).
   - `ports`: A list of ports to scan (e.g., `22 80 443` to scan SSH, HTTP, and HTTPS ports).

   **Example usage**:

   ```bash
   python NeScan.py 192.168.1 22 80 443
   ```

   This will scan IP addresses from `192.168.1.1` to `192.168.1.255`, checking ports 22, 80, and 443.

3. **View the results**:

   After the scan is complete, results will be displayed in the terminal and saved to a file called `resultados_escaner.txt` in the same directory.

## Sample Results

### Console output:

```
Starting scan...

Scan progress: 100%|██████████| 255/255 [00:15<00:00, 17.00it/s]

--- SCAN RESULTS ---

Open Ports:
[+++] 192.168.1.1:22 OPEN
[+++] 192.168.1.10:80 OPEN
...

Closed Ports:
[-] 192.168.1.2:443 CLOSED
[-] 192.168.1.15:22 CLOSED
...
```

### Results in `resultados_escaner.txt`:

```
--- OPEN PORTS ---
[+++] 192.168.1.1:22 OPEN
[+++] 192.168.1.10:80 OPEN
...

--- CLOSED PORTS ---
[-] 192.168.1.2:443 CLOSED
[-] 192.168.1.15:22 CLOSED
...
```

## Contributing

If you'd like to contribute to this project, don't mind opening issues or creating pull requests. I need some practice and learn about you, so feel free!
I would like to add a service discovery section in the code.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code as long as you comply with the terms of the license.
