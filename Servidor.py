import socket

def main():
    # Criando um socket TCP/IP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Definindo o endereço do servidor e a porta
    endereco_servidor = ('localhost', 5555)

    # Vinculando o socket ao endereço e porta especificados
    servidor_socket.bind(endereco_servidor)

    # Escutando por conexões entrantes
    servidor_socket.listen(1)

    print("Servidor pronto para receber conexões...")

    # Aceitando a conexão do cliente
    conexao_cliente, endereco_cliente = servidor_socket.accept()
    print(f"Conexão estabelecida com {endereco_cliente}")

    while True:
        # Recebendo mensagem do cliente
        mensagem_cliente = conexao_cliente.recv(1024).decode() # 1024 é o tamanho do buffer = 1KB
        print(f"Cliente: {mensagem_cliente}")

        # Se a mensagem for 'sair', encerra a conexão
        if mensagem_cliente.lower() == 'sair':
            print("Cliente desconectado.")
            break

        # Enviando mensagem de volta para o cliente
        mensagem_servidor = input("Servidor: ")
        conexao_cliente.sendall(mensagem_servidor.encode())

    # Fechando a conexão
    conexao_cliente.close()
    servidor_socket.close()

if __name__ == "__main__":
    main()
