import socket
import threading
import os

def enviar_mensagens(cliente_socket):
    while True:
        msg = input()
        if msg.startswith('ARQUIVO'):
            nome_arquivo = msg[8:]
            cliente_socket.send(f'ARQUIVO {nome_arquivo}'.encode())
            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, 'rb') as f:
                    bytes_para_enviar = f.read(1024)
                    cliente_socket.send(bytes_para_enviar)
                    while bytes_para_enviar:
                        bytes_para_enviar = f.read(1024)
                        cliente_socket.send(bytes_para_enviar)
                print("Arquivo enviado com sucesso!")
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

def receber_mensagens(cliente_socket):
    while True:
        try:
            msg = cliente_socket.recv(1024).decode()
            if msg.startswith('EXISTE'):
                tamanho_arquivo = int(msg.split()[1])
                nome_arquivo = input("Digite o nome para salvar o arquivo: ")
                with open(nome_arquivo, 'wb') as f:
                    dados = cliente_socket.recv(1024)
                    total_recebido = len(dados)
                    f.write(dados)
                    while total_recebido < tamanho_arquivo:
                        dados = cliente_socket.recv(1024)
                        total_recebido += len(dados)
                        f.write(dados)
                print("Arquivo recebido com sucesso!")
            elif msg == 'ERRO':
                print("Erro ao enviar o arquivo.")
            else:
                print(f"Servidor diz: {msg}")
        except:
            print("Conexão encerrada pelo servidor.")
            break

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 12345))
    
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.start()

    enviar_mensagens(cliente)
    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()
