import socket
import threading
import os

clientes = {}
nomes_clientes = {}

def broadcast(mensagem, cliente_atual):
    for cliente in clientes.values():
        if cliente != cliente_atual:
            try:
                cliente.send(mensagem.encode())
            except:
                cliente.close()
                remover_cliente(cliente)

def enviar_para_cliente(mensagem, nome_destinatario, cliente_remetente):
    if nome_destinatario in nomes_clientes:
        cliente_destinatario = nomes_clientes[nome_destinatario]
        try:
            cliente_destinatario.send(mensagem)
        except:
            cliente_destinatario.close()
            remover_cliente(cliente_destinatario)
    else:
        cliente_remetente.send(f"Usuário {nome_destinatario} não encontrado.".encode())

def receber_arquivo(cliente_socket, nome_destinatario, nome_arquivo):
    dados = b""
    while True:
        parte = cliente_socket.recv(1024)
        if parte == b'FIM_ARQUIVO':
            break
        dados += parte
    if nome_destinatario in nomes_clientes:
        cliente_destinatario = nomes_clientes[nome_destinatario]
        try:
            cliente_destinatario.send(f"ARQUIVO {nome_arquivo}".encode())
            cliente_destinatario.send(dados)
            cliente_destinatario.send(b'FIM_ARQUIVO')
            print(f"Arquivo {nome_arquivo} enviado para {nome_destinatario}.")
        except:
            cliente_destinatario.close()
            remover_cliente(cliente_destinatario)
    else:
        cliente_socket.send(f"Usuário {nome_destinatario} não encontrado.".encode())

def lidar_com_cliente(cliente_socket, addr):
    nome = cliente_socket.recv(1024).decode()
    clientes[addr] = cliente_socket
    nomes_clientes[nome] = cliente_socket
    print(f"{nome} ({addr[0]}:{addr[1]}) entrou no chat.")
    cliente_socket.send(f"Bem-vindo ao servidor de chat, {nome}!".encode())
    broadcast(f"{nome} entrou no chat.", cliente_socket)

    while True:
        try:
            msg = cliente_socket.recv(1024).decode()
            if msg.startswith('ARQUIVO'):
                partes = msg.split(' ', 2)
                if len(partes) < 3:
                    cliente_socket.send("Uso correto: ARQUIVO <nome_do_destinatario> <nome_do_arquivo>".encode())
                    continue
                nome_destinatario = partes[1]
                nome_arquivo = partes[2]
                receber_arquivo(cliente_socket, nome_destinatario, nome_arquivo)
            elif msg == 'SAIR':
                print(f"{nome} ({addr[0]}:{addr[1]}) saiu do chat.")
                broadcast(f"{nome} saiu do chat.", cliente_socket)
                break
            else:
                print(f"{msg}")
                broadcast(msg, cliente_socket)
        except Exception as e:
            print(f"Erro na comunicação com {nome} ({addr[0]}:{addr[1]}): {e}")
            break

    remover_cliente(cliente_socket)

def remover_cliente(cliente_socket):
    global clientes, nomes_clientes
    addr = None
    nome = None
    for endereco, socket in clientes.items():
        if socket == cliente_socket:
            addr = endereco
            break
    if addr:
        del clientes[addr]
    for nome_usuario, socket in nomes_clientes.items():
        if socket == cliente_socket:
            nome = nome_usuario
            break
    if nome:
        del nomes_clientes[nome]
    if not clientes:
        print("Todos os clientes se desconectaram. Desligando o servidor...")
        os._exit(0)

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
