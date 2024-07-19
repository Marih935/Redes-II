import socket
import threading
import os
import time

def receber_mensagens(cliente_socket):
    while True:
        try:
            msg = cliente_socket.recv(1024).decode()
            if msg:
                print(f"{msg}")
            else:
                break
        except:
            print("Erro ao receber mensagem do servidor.")
            break

def enviar_mensagens(cliente_socket, nome):
    while True:
        msg = input()
        if msg.startswith('ARQUIVO'):
            partes = msg.split(' ', 2)
            if len(partes) < 3:
                print("Uso correto: ARQUIVO <nome_do_destinatario> <nome_do_arquivo>")
                continue
            nome_destinatario = partes[1]
            nome_arquivo = partes[2]
            if os.path.exists(nome_arquivo):
                cliente_socket.send(f'ARQUIVO {nome_destinatario} {nome_arquivo}'.encode())
                time.sleep(1)
                with open(nome_arquivo, 'rb') as f:
                    while True:
                        bytes_para_enviar = f.read(1024)
                        if not bytes_para_enviar:
                            break
                        cliente_socket.send(bytes_para_enviar)
                time.sleep(1)
                cliente_socket.send(b'FIM_ARQUIVO')
                print("Arquivo enviado com sucesso!")
            else:
                print("Arquivo não encontrado.")
        elif msg.startswith('ENVIAR'):
            cliente_socket.send(f"{nome}: {msg[7:]}".encode())
        elif msg == 'SAIR':
            cliente_socket.send(b'SAIR')
            print("Saindo do chat...")
            break
        else:
            cliente_socket.send(f"{nome}: {msg}".encode())

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('10.26.6.11', 12345))
    
    nome = input("Digite seu nome: ")
    cliente.send(nome.encode())
    
    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente,))
    thread_receber.start()

    enviar_mensagens(cliente, nome)
    cliente.close()

if __name__ == "__main__":
    print("Bem-vindo ao chat!")
    print("Comandos disponíveis:")
    print("1. Enviar mensagem: digite sua mensagem e pressione Enter.")
    print("2. Enviar arquivo: ARQUIVO <nome_do_destinatario> <nome_do_arquivo>")
    print("3. Sair do chat: SAIR")
    iniciar_cliente()
