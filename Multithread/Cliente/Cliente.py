import socket
import threading
import os
import time

def receber_mensagens(cliente_socket):
    while True:
        try:
            msg = cliente_socket.recv(1024).decode()
            if msg:
                print(f"Servidor: {msg}")
            else:
                break
        except:
            print("Erro ao receber mensagem do servidor.")
            break

def enviar_mensagens(cliente_socket):
    while True:
        msg = input()
        if msg.startswith('ARQUIVO'):
            nome_arquivo = msg[8:]
            cliente_socket.send(f'ARQUIVO {nome_arquivo}'.encode())
            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, 'rb') as f:
                    while True:
                        bytes_para_enviar = f.read(1024)
                        if not bytes_para_enviar:
                            break
                        cliente_socket.send(bytes_para_enviar)
                print("Arquivo enviado com sucesso!")
                time.sleep(1)
            else:
                print("Arquivo não encontrado.")
        elif msg.startswith('ENVIAR'):
            cliente_socket.send(msg.encode())
        elif msg == 'SAIR':
            cliente_socket.send(b'SAIR')
            print("Saindo do chat...")
            break
        else:
            cliente_socket.send(msg.encode())

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 12345))
    
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.start()

    enviar_mensagens(cliente)
    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()
