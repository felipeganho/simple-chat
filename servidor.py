import socket, threading

#variável global que mantém as conexões dos clientes
conexoes = []

#transmite mensagem para todos os usuários conectados ao servidor
def transmissao(mensagem: str, conexao: socket.socket):
    #iteração de conexões para enviar mensagem a todos os clientes conectados
    for cliente_conexao in conexoes:
        #verifica se não é a conexão de quem envia a mensagem
        if cliente_conexao != conexao:
            try:
                #envia a mensagem a conexão cliente
                cliente_conexao.send(mensagem.encode())

            #caso falhe, possível que o socket tenha morrido
            except Exception as e:
                print('Mensagem de erro de transmissao: {e}')
                remove_conexao(cliente_conexao)

#obtém a conexão do usuário para continuar recebendo e enviando mensagens
def userConexao(conexao: socket.socket, endereco: str):
    while True:
        try:
            #com a conexão estabelecida, recv recebe a mensagem do cliente
            msg = conexao.recv(1024)

            #se não há mensagem recebida, há uma chance que a conexão encerrou
            #nesse caso, precisamos fechar a conexão e removê-lo da lista de conexões.
            if msg:
                #mensagem de log enviada pelo usuário
                print(f'{endereco[0]}:{endereco[1]} - {msg.decode()}')
                
                #constrói o formato da mensagem e transmite para os usuários conectados ao servidor
                msg_to_send = f'From {endereco[0]}:{endereco[1]} - {msg.decode()}'
                transmissao(msg_to_send, conexao)

            #encerra a conexão se não há mensagem para enviar
            else:
                remove_conexao(conexao)
                break

        except Exception as e:
            print(f'Erro ao lidar com a conexão do usuário: {e}')
            remove_conexao(conexao)
            break

#remove um conexão específica da lista de conexões
def remove_conexao(conexao: socket.socket):
    #checa se a conexão existe na lista de conexões
    if conexao in conexoes:
        #encerra a conexão do socket e remove a conexão da lista de conexões
        conexao.close()
        conexoes.remove(conexao)

#inicia server, recebe conexões de clientes e inicia um novo thread para lidar com as mensagens
def servidor():
    #porta do servidor
    PORTA_OUVINDO = 12000
    
    try:
        #cria o servidor e especifica que permite apenas 4 conexões por vez 
        socket_instancia = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #associa o socket a porta
        socket_instancia.bind(('', PORTA_OUVINDO))
        #coloca o socket em modo server
        socket_instancia.listen(4)

        print('Servidor rodando!')
        
        while True:

            #aceita conexão cliente
            socket_conexao, endereco = socket_instancia.accept()
            #adiciona conexão cliente a lista de conexões
            conexoes.append(socket_conexao)
            #começa uma nova thread para lidar com a conexão cliente e receber suas mensagens
            threading.Thread(target=userConexao, args=[socket_conexao, endereco]).start()

    except Exception as e:
        print(f'Um erro ocorreu quando instânciou o socket: {e}')
        
    #garantimos que será encerrado
    finally:
        #em caso de algum problema limpamos todas as conexões e fechamos a conexão do servidor
        if len(conexoes) > 0:
            for conexao in conexoes:
                remove_conexao(conexao)

        socket_instancia.close()


if __name__ == "__main__":
    servidor()