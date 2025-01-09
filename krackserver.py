import socket 
import json
import subprocess
import os
import time

def crack_it(data):
    try:
        # separate hash and mode
        hash_data = data["hash"]
        mode = data["mode"]

        # define paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        wordlist_filename = "rockyou.txt"
        hashcat_filename = "hashcat.exe"
        hash_filename = "tocrack.txt"
        wordlist_path = os.path.join(current_dir, wordlist_filename)
        hashcat_path = os.path.join(current_dir, hashcat_filename)
        hash_path = os.path.join(current_dir, hash_filename)

        # save hash to file. windows cmdline is weird
        with open(hash_path, 'w') as f:
            f.write(hash_data)
            print(f"Writing to file:\n{hash_data}")

        # define command and run it
        command = f'{hashcat_path} -a 0 -m {mode} {hash_path} {wordlist_path}'
        print(f"Running command: {command}")
        process = subprocess.run(command.split(), capture_output=True, text=True, shell=True, cwd=current_dir)

        ### DEBUG
        if process.returncode != 0:
            print(f"DEBUG Failed: {process.stderr}\nCurrent dir: {current_dir}")
        else:
            print(f"DEBUG Success: {process.stdout}")

        return process.stdout
    
    except KeyError as e:
        return f"Missing required data key: {e}"
    except FileNotFoundError as e:
        return f"File not found: {e}"
    except subprocess.SubprocessError as e:
        return f"Error running Hashcat: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def main():
    # start and listen for connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 13371)) # any incoming connection on port 13371
        print("[*] INFO: Server listening on port 13371...")
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = json.loads(conn.recv(4096).decode())
            print(f"Received: {data}")
            result = crack_it(data) 
            print(f"[+] Sending: {result}")
            conn.sendall(result.encode())
            

try:
    while True:
        main()
        time.sleep(1)
except KeyboardInterrupt:
    print("[+] ACTION: Keyboard interrupt.")