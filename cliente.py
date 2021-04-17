import socket, threading

#recebe mensagens enviadas pelo servidor e mostra elas ao usuário
def mensagens(conexao: socket.socket):
    while True:
        try:
            msg = conexao.recv(1024)

            # caso há mensagem tentará decodificar a mensagem para mostrar ao usuário
            if msg:
                print(msg.decode())
                
            # se não há mensagem, há uma chance que a conexão foi fechada.
            # então a conexão será fechada e um erro será mostrado.
            else:
                conexao.close()
                break

        except Exception as e:
            print(f'Erro ao lidar com a mensagem do servidor: {e}')
            conexao.close()
            break

#inicia a conexão cliente ao servidor e lida com suas mensagens de entrada
def cliente():
    ENDERECO_SERVER = '127.0.0.1'
    PORTA_SERVER = 12000

    try:
        #instância o socket e inicia a conexão com o servidor
        #TCP/IP socket
        socket_instancia = socket.socket()
        #conecta o socket a porta onde o server "escuta"
        socket_instancia.connect((ENDERECO_SERVER, PORTA_SERVER))
        #cria uma thread para lidar com as mensagens enviadas pelo servidor
        threading.Thread(target=mensagens, args=[socket_instancia]).start()

        print('Conectado ao chat!')

        #lê a entrada do usuário até que saia do chat e feche a conexão
        while True:
            msg = input()

            if msg == 'sair':
                break

            #converte a mensagem para utf-8
            socket_instancia.send(msg.encode())

        #encerra a conexão com o servidor
        socket_instancia.close()

    except Exception as e:
        print(f'Erro ao conectar ao socket do servidor: {e}')
        socket_instancia.close()


if __name__ == "__main__":
    cliente()
