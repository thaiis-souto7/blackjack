# -*- coding: utf-8 -*-
import socket, sys
import time
import random

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

ListPlayers = []
valueRound = 0

def InfoPlayer(numPlayers):
    name = input("\n----> Digite seu nome: ")
    city = input("----> Digite sua cidade: ")
    p = AddPlayer(numPlayers, name, city, 1000, 0, [])
     

class AddPlayer:
    def __init__(self, code, name, city, amount, victories, cards):
        self.code = code
        self.name = name
        self.city = city
        self.amount = amount
        self.victories = victories
        self.cards = cards

        ListPlayers.append([code, name, city, amount, victories, cards])

#Pergunta quanto que o jogador quer apostar e faz a aposta
def Bet(player):
    amountPlayer = int(player[3])
    value = int(input("Qual valor deseja apostar? \n----> "))
    while (value < 1 or value > amountPlayer):
        print("Não é permitido apostar esse valor")
        value = int(input("Qual valor deseja apostar? \n----> "))

    player[3] -= value

    global valueRound 
    valueRound += value
    
    return player
       

#Reseta o baralho já o embaralhando
def ResetCheap():
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    suits = ["♣", "♦", "♥", "♠"]
    cheap = []

    for suit in suits:
       for card in cards:
           cheap.append("{}{}{}".format(card," ", suit))

    random.shuffle(cheap)
    return cheap

#Distribui as duas cartas iniciais aos jogadores
def GiveCards(ListPlayers,cheap):

        for i in range(len(ListPlayers)):
            cards = []
            cards.append(cheap[0])
            cards.append(cheap[1])
            
            ListPlayers[i][5] = cards

            del(cheap[0:2])

#Da a opção de comer mais cartas
def eat(player,cheap):
    while(True):
        eating = input("----> Deseja comer uma nova carta ? [s/n] \n----> ")
        if(eating == "s" or eating == "S" or eating == "Sim" or eating == "SIM" or eating == "sim"):
            cards = player[5]
            cards.append(cheap[0])
            player[5] = cards
            del(cheap[0:1])
            print("Suas Cartas   |",player[5])
        else:
            break
    return player


#Mostra o total de cartas que tem na mão do jogador
"""def CountCards(cards):

    values = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10
    }"""

#Mostra o montande de dinheiro que o jogador tem
def ShowAmount(player):
    print("Seu montante é   |",player[3])


#Controla o decorrer da rodada
def Round(ListPlayers,numRound,cheap):
    print("\n*********** BLACKJACK ***********")
    print("\n************ ROUND ",numRound+1," ************\n")
    
    for i in range(len(ListPlayers)):
        print("\nVez do jogador", ListPlayers[i][1])
        ShowAmount(ListPlayers[i])
        ListPlayers[i] = Bet(ListPlayers[i])
    
    #Entrega duas cartas para os jogadores
    GiveCards(ListPlayers,cheap)

    #Da a opção de comer novamente ou não
    for i in range(len(ListPlayers)):
        print("\n*********************************\nVez do jogador", ListPlayers[i][1])
        print("\nSuas Cartas   |",ListPlayers[i][5])
        ShowAmount(ListPlayers[i])
        ListPlayers[i] = eat(ListPlayers[i],cheap) 


def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            print("\n*********** BLACKJACK ***********\n")
            numPlayers = 1
            numGame = 0

            while(True):
                
                if(numPlayers == 5):
                    print("Limite de jogadores atingido!")
                    break
                else:
                    InfoPlayer(numPlayers)
                    newPlayer = input("\n----> Deseja inserir um novo jogador? [s/n] \n----> ")
                    if(newPlayer == "s" or newPlayer == "S" or newPlayer == "Sim" or newPlayer == "SIM" or newPlayer == "sim"):
                        numPlayers += 1
                    else:
                        break

            while(True):       
                play = int(input("\n----> OPÇÕES DE JOGO: \n1 - Jogar\n2 - Sair\n----> "))
                
                if(play == 1):
                    
                    #Cria um novo Round de Jogo
                    numRound = 0

                    #Cria um baralho com 52 cartas e embaralha as cartas
                    cheap = ResetCheap()

                    Round(ListPlayers,numRound,cheap)
                   
                    teste = "testando"

                    #Finaliza o game caso queira, ou continua
                    keepPlaying = input("Deseja continuar jogando? [s/n] \n----> ")
                    if(keepPlaying == "s" or keepPlaying == "S"):
                        numGame += 1
                    else:
                        print('O jogo será encerrado !!')
                        print("O vencedor foi XXXX")
                        s.close()
                        break

                    time.sleep(10)
                    s.send(teste.encode()) #.encode - converte a string para bytes
                    data = s.recv(BUFFER_SIZE)
                    texto_recebido = repr(data) #converte de bytes para um formato "printável"
                    print('Recebido do servidor', texto_recebido)
                    texto_string = data.decode('utf-8') #converte os bytes em string
                    
                    
                elif(play == 2):
                    print("Saindo do jogo")
                    break
                else:
                    print("Opção errada !!\n")
                    
                

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])
