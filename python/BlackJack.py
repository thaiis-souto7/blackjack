# -*- coding: utf-8 -*-
from os import scandir
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
    p = AddPlayer(numPlayers, name, city, 1000, 0, [], 0)
     

class AddPlayer:
    def __init__(self, code, name, city, amount, victories, cards, punctuation):
        self.code = code
        self.name = name
        self.city = city
        self.amount = amount
        self.victories = victories
        self.cards = cards
        self.punctuation = punctuation

        ListPlayers.append([code, name, city, amount, victories, cards, punctuation])


def Round(ListPlayers,numRound):
    print("\n*********** BLACKJACK ***********")
    print("\n************ ROUND ",numRound+1," ************\n")
    
    for i in range(len(ListPlayers)):
        print("Vez do jogador", ListPlayers[i][1])
        ListPlayers[i] = Bet(ListPlayers[i], valueRound)

    
def Bet(player,valueRound):
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
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]*4
    random.shuffle(cards)
    return cards

def AddCheap():
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    suits = ["copas", "ouros", "paus", "espadas"]
    cheap = []

    for suit in suits:
       for card in cards:
           cheap.append("{}{}{}".format(card, " ", suit))
    print(cheap)
    return cheap

        ListPlayers[i][6] = CountCards(ListPlayers[i][5])

        print("\nSuas Cartas   |", ListPlayers[i][5], "TOTAL   |", ListPlayers[i][6])
        ShowAmount(ListPlayers[i])
        ListPlayers[i] = eat(ListPlayers[i], cheap) 
    
    print("O Vencedor foi   |", win(ListPlayers))


    print(ListPlayers)


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
                    cheap = AddCheap()
                    ShuffleCards(cheap)
                    print(cheap)

                    Round(ListPlayers,numRound,cheap)
                   
                    teste = "testando"

                    #Finaliza o game caso queira, ou continua
                    keepPlaying = input("Deseja continuar jogando? [s/n] \n----> ")
                    if(keepPlaying == "s" or keepPlaying == "S"):
                        numGame += 1
                    else:
                        print('\nO jogo será encerrado !!')
                        for i in range(len(ListPlayers)):
                            print("\n", ListPlayers[i][1],"\n------\nCidade: ",ListPlayers[i][2],"\nMontante", ListPlayers[i][3], "\nVitorias: ", ListPlayers[i][4])
                        s.close()
                        break

                    s.send(teste.encode()) #.encode - converte a string para bytes
                    data = s.recv(BUFFER_SIZE)
                    texto_recebido = repr(data) #converte de bytes para um formato "printável"
                    print('Recebido do servidor', texto_recebido)
                    texto_string = data.decode('utf-8') #converte os bytes em string
                    
                else:
                    print("Saindo do jogo")
                    for i in range(len(ListPlayers)):
                        print("\n", ListPlayers[i][1],"\n------\nCidade: ",ListPlayers[i][2],"\nMontante", ListPlayers[i][3], "\nVitorias: ", ListPlayers[i][4])
                    s.close()
                    break
                else:
                    print("Opção errada !!\n")
                    
                

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])
