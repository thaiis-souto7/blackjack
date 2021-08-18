# -*- coding: utf-8 -*-
import socket, sys
import time

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

ListPlayers = []

def InfoPlayer(numPlayers):
    name = input("----> Digite seu nome: ")
    city = input("----> Digite sua cidade: ")
    p = AddPlayer(numPlayers, name, city, 1000, 0)


class AddPlayer:
    def __init__(self, code, name, city, amount, victories):
        self.code = code
        self.name = name
        self.city = city
        self.amount = amount
        self.victories = victories

        ListPlayers.append((code, name, city, amount, victories))


def main(argv): 

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            print("\n*********** BLACKJACK ***********")
            numPlayers = 1
            numGame = 0

            while(True):
                
                if(numPlayers == 5):
                    print("Limite de jogadores atingido!")
                    time.sleep(5)
                    break

                InfoPlayer(numPlayers)
                newPlayer = input("Deseja inserir novo jogador? [s/n] \n----> ")
                if(newPlayer == "s" or newPlayer == "S"):
                    numPlayers += 1
                    print(ListPlayers)
                else:
                    break

            while(True):       
                teste = "testando"
                time.sleep(20)
                s.send(teste.encode()) #.encode - converte a string para bytes
                data = s.recv(BUFFER_SIZE)
                texto_recebido = repr(data) #converte de bytes para um formato "printável"
                print('Recebido do servidor', texto_recebido)
                texto_string = data.decode('utf-8') #converte os bytes em string
                
                #Finaliza o game caso queira, ou continua
                keepPlaying = input("Deseja continuar jogando? [s/n] \n----> ")
                if(keepPlaying == "s" or keepPlaying == "S"):
                    numGame += 1
                else:
                    print('O jogo será encerrado !!')
                    print("O vencedor foi XXXX")
                    s.close()
                    break

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])
