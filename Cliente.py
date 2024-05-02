import socket

def main():
    # Criando um socket TCP/IP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Definindo o endereço do servidor e a porta
    endereco_servidor = ('localhost', 5555)

    # Conectando ao servidor remoto
    cliente_socket.connect(endereco_servidor)

    while True:
        # Enviando mensagem para o servidor
        mensagem_cliente = input("Cliente: ")
        cliente_socket.sendall(mensagem_cliente.encode())

        # Se a mensagem for 'sair', encerra a conexão
        if mensagem_cliente.lower() == 'sair':
            break

        # Recebendo mensagem do servidor
        mensagem_servidor = cliente_socket.recv(1024).decode()
        print(f"Servidor: {mensagem_servidor}")

    # Fechando a conexão
    cliente_socket.close()

if __name__ == "__main__":
    main()
