import socket
import threading
import os

def enviar_arquivo(cliente_socket, nome_arquivo):
    if os.path.exists(nome_arquivo):
        cliente_socket.send(f'EXISTE {os.path.getsize(nome_arquivo)}'.encode())
        with open(nome_arquivo, 'rb') as f:
            bytes_para_enviar = f.read(1024)
            cliente_socket.send(bytes_para_enviar)
            while bytes_para_enviar:
                bytes_para_enviar = f.read(1024)
                cliente_socket.send(bytes_para_enviar)
        print("Arquivo enviado com sucesso!")
    else:
        cliente_socket.send(b'ERRO')

def receber_arquivo(cliente_socket, nome_arquivo):
    with open(nome_arquivo, 'wb') as f:
        dados = cliente_socket.recv(1024)
        while dados:
            f.write(dados)
            dados = cliente_socket.recv(1024)
    print("Arquivo recebido com sucesso!")

def lidar_com_cliente(cliente_socket, addr):
    print(f"Conexão aceita de {addr}")
    cliente_socket.send(b'Bem-vindo ao servidor de chat!')

    while True:
        try:
            msg = cliente_socket.recv(1024).decode()
            if msg.startswith('ARQUIVO'):
                nome_arquivo = msg[8:]
                receber_arquivo(cliente_socket, nome_arquivo)
            elif msg.startswith('ENVIAR'):
                nome_arquivo = msg[7:]
                enviar_arquivo(cliente_socket, nome_arquivo)
            elif msg == 'SAIR':
                print(f"Conexão encerrada com {addr}")
                break
            else:
                print(f"Cliente {addr} diz: {msg}")
                cliente_socket.send(f"{msg}".encode())
        except:
            print(f"Erro na comunicação com {addr}")
            break

    cliente_socket.close()

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 12345))
    servidor.listen(5)
    print("Servidor aguardando conexões...")

    while True:
        cliente_socket, addr = servidor.accept()
        cliente_thread = threading.Thread(target=lidar_com_cliente, args=(cliente_socket, addr))
        cliente_thread.start()

if __name__ == "__main__":
    iniciar_servidor()
