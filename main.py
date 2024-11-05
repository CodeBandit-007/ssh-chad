import paramiko
import threading
from termcolor import colored
import time
import sys

# ASCII Art banner for SSH-CHAD
BANNER = colored("""
███╗   ███╗███████╗███████╗     ██████╗██╗  ██╗ █████╗ ██████╗ 
████╗ ████║██╔════╝██╔════╝    ██╔════╝██║  ██║██╔══██╗██╔══██╗
██╔████╔██║█████╗  ███████╗    ██║     ███████║███████║██║  ██║
██║╚██╔╝██║╔══╝██  ╚════██║    ██║     ██╔══██║██╔══██║██║  ██║
██║ ╚═╝ ██║███████╗███████║    ╚██████╗██║  ██║██║  ██║██████╔╝
╚═╝     ╚═╝╚══════╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
""", "cyan")

# Basic SSH Connection Manager class
class SSHChad:
    def __init__(self):
        self.connections = []

    def connect(self, hostname, port, username, password):
        """Establish SSH connection."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, port=port, username=username, password=password)
            self.connections.append(ssh)
            print(colored(f"[+] Connected to {hostname}:{port}", "green"))
        except Exception as e:
            print(colored(f"[!] Failed to connect to {hostname}:{port}: {e}", "red"))

    def execute_command_on_server(self, ssh, command, idx):
        """Execute command on a single server."""
        try:
            print(colored(f"\n[*] Executing on Server {idx + 1}:", "blue"))
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(colored(output, "green"))
            if error:
                print(colored(error, "red"))
        except Exception as e:
            print(colored(f"[!] Error on Server {idx + 1}: {e}", "red"))

    def execute_command(self, command):
        """Execute a command on all connected SSH instances in parallel using threading."""
        threads = []
        for idx, ssh in enumerate(self.connections):
            thread = threading.Thread(target=self.execute_command_on_server, args=(ssh, command, idx))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def close_connections(self):
        """Close all SSH connections."""
        for ssh in self.connections:
            ssh.close()
        self.connections.clear()
        print(colored("[*] All connections closed.", "blue"))

# Main function for UI and command handling
def main():
    print(BANNER)
    print(colored("Welcome to SSH-CHAD! Manage multiple SSH sessions like a pro.\n", "green"))

    ssh_chad = SSHChad()

    while True:
        print(colored("\nOptions:", "blue"))
        print(colored("1) Add SSH Connection", "cyan"))
        print(colored("2) Run Command on All Servers", "cyan"))
        print(colored("3) Close All Connections", "cyan"))
        print(colored("4) Exit", "cyan"))
        
        choice = input(colored("Select an option (1-4): ", "yellow"))

        if choice == "1":
            hostname = input(colored("Enter hostname: ", "blue"))
            port = int(input(colored("Enter port: ", "blue")))
            username = input(colored("Enter username: ", "blue"))
            password = input(colored("Enter password: ", "blue"))
            ssh_chad.connect(hostname, port, username, password)

        elif choice == "2":
            command = input(colored("Enter command to run on all servers: ", "blue"))
            ssh_chad.execute_command(command)

        elif choice == "3":
            ssh_chad.close_connections()

        elif choice == "4":
            ssh_chad.close_connections()
            print(colored("\nExiting SSH-CHAD. Goodbye!", "green"))
            break

        else:
            print(colored("Invalid option. Please try again.", "red"))

if __name__ == "__main__":
    main()

