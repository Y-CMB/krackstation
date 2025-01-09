import argparse
import json
import socket

parser = argparse.ArgumentParser(prog="krackclient.py")
parser.add_argument("-hash", help="hash to crack in a str format")
parser.add_argument("-o", help="name to save file as", required=False)
parser.add_argument("-s", help="IP to send the hash to")
parser.add_argument("-m", help="0: MD5 | 100: SHA1 | 1400: SHA256 | 1700: SHA512 | 1000: NTLM | 3000: LM | 5500: NetNTLMv1 | 5600: NetNTLMv2 | 1800: SHA512crypt (Unix) | 3200: bcrypt (Blowfish)", required=False)
args = parser.parse_args()

# define data to send
data = {
    "hash": args.hash
}
if args.m:
    data.update({"mode": args.m})

# save file locally
if args.o:
    filename = args.o
    print(filename)
    with open(filename, mode="w") as f:
        f.write(args.hash)
        print(f"[*] INFO: wrote {len(args.hash)} chars to {f.name}")
else:
    print("[*] INFO: -o not specified... Skipping")

# send to server from memory
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        print(f"[*] INFO: Attempting connection to {args.s}:13371")
        s.connect((args.s, 13371))
        print("[*] INFO: Success! Sending data... {}")
        s.sendall(json.dumps(data).encode())
        result = s.recv(4096).decode()
        print(f"[+] ACTION: Finished\n======================\n{result}")
    except socket.error as e:
        print(f"[-] ERROR: {e}")

