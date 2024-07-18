import socket
import threading
import os

clientes_conectados = 0
clientes_conectados_lock = threading.Lock()

def receber_arquivo(cliente_socket, nome_arquivo):
    with open(nome_arquivo, 'wb') as f:
        while True:
            dados = cliente_socket.recv(1024)
            if not dados:
                break
            f.write(dados)
    print("Arquivo recebido com sucesso!")

def lidar_com_cliente(cliente_socket, addr):
    global clientes_conectados
    print(f"Conexão aceita de {addr}")
    cliente_socket.send(b'Bem-vindo ao servidor de chat!')

    while True:
        try:
            msg = cliente_socket.recv(1024).decode()
            if msg.startswith('ARQUIVO'):
                nome_arquivo = msg[8:]
                receber_arquivo(cliente_socket, nome_arquivo)
            elif msg == 'SAIR':
                print(f"Conexão encerrada com {addr}")
                break
            else:
                print(f"Cliente {addr} diz: {msg}")
                cliente_socket.send(f"{msg}".encode())
        except Exception as e:
            print(f"Erro na comunicação com {addr}: {e}")
            break

    cliente_socket.close()
    with clientes_conectados_lock:
        clientes_conectados -= 1
        if clientes_conectados == 0:
            print("Todos os clientes se desconectaram. Desligando o servidor...")
            os._exit(0)

def iniciar_servidor():
    global clientes_conectados
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 12345))
    servidor.listen(5)
    print("Servidor aguardando conexões...")

    while True:
        cliente_socket, addr = servidor.accept()
        with clientes_conectados_lock:
            clientes_conectados += 1
        cliente_thread = threading.Thread(target=lidar_com_cliente, args=(cliente_socket, addr))
        cliente_thread.start()

if __name__ == "__main__":
    iniciar_servidor()
