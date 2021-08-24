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
    name = input("----> Digite seu nome: ")
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


#Pergunta quanto que o jogador quer apostar e faz a aposta
def Bet(player):
    amountPlayer = int(player[3])
    value = int(input("\nQual valor deseja apostar? \n----> R$"))
    print("---------------------------------")
    while (value < 1 or value > amountPlayer):
        print("Não é permitido apostar esse valor")
        value = int(input("Qual valor deseja apostar? \n----> R$"))
        print("---------------------------------")

    player[3] -= value

    global valueRound 
    valueRound += value
    
    return player
       

#Reseta o baralho já o embaralhando
def ResetCheap():
    cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]*4
    random.shuffle(cards)
    return cards


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
        if player[6] == 21:
            print("\nVocê já tem 21!")
            print("---------------------------------\n")
            break
        elif player[6] > 21:
            print("\nVocê estourou!")
            print("---------------------------------\n")
            break
        else:    
            eating = input("\n----> Comer nova carta? [s/n] \n----> ")
            if(eating == "s" or eating == "S" or eating == "Sim" or eating == "SIM" or eating == "sim"):
                cards = player[5]
                cards.append(cheap[0])
                player[5] = cards
                del(cheap[0:1])
                print("\nCartas: ", player[5], "\nValor Atual: ", CountCards(player[5]))
                player[6] = CountCards(player[5])
                
            else:
                break
    return player


#Mostra o total de cartas que tem na mão do jogador
def CountCards(cards):

    sum = 0
    for i in range(len(cards)):
        #Considera o A como 11 caso tenha um K Q J ou 10
        if cards[i] == "A":
            for j in range(len(cards)):
                if cards[j] == "K" or cards[j] == "Q" or cards[j] == "J" or cards[j] == "10":
                    sum += 10
            sum += 1
        elif cards[i] == "2":
            sum += 2
        elif cards[i] == "3":
            sum += 3
        elif cards[i] == "4":
            sum += 4
        elif cards[i] == "5":
            sum += 5
        elif cards[i] == "6":
            sum += 6
        elif cards[i] == "7":
            sum += 7
        elif cards[i] == "8":
            sum += 8
        elif cards[i] == "9":
            sum += 9
        elif cards[i] == "10":
            sum += 10
        elif cards[i] == "J":
            sum += 10
        elif cards[i] == "Q":
            sum += 10
        elif cards[i] == "K":
            sum += 10
    
    #Trata caso o A esteja sendo considerado 11 e esteje estourando, ai passa ela para 1 denovo
    for i in range(len(cards)):
        if sum > 21:
            if cards[i] == "A":
                for j in range(len(cards)):
                    if cards[j] == "K" or cards[j] == "Q" or cards[j] == "J" or cards[j] == "10":
                        sum -= 10

    return sum


#Define quem foi o vencedor  
def win(ListPlayers):
    large = 0
    blackjack = []
    codBlackjack = []
    codWinners = []
    winners = []
    points = []
    

    for i in range(len(ListPlayers)):
        
        points.append(ListPlayers[i][6])
        if points[i] > large and points[i] <= 21:
            large = points[i]
            winners.clear()
            codWinners.clear()
            winners.append(ListPlayers[i][1])
            codWinners.append(ListPlayers[i][0])
            
        elif points[i] == large:
            winners.append(ListPlayers[i][1])
            codWinners.append(ListPlayers[i][0])
            
        if points[i] == 21:
            for j in range(len(ListPlayers[i][5])):
                if ListPlayers[i][5][j] == "A":
                    blackjack.append(ListPlayers[i][1])
                    codBlackjack.append(ListPlayers[i][0])           

    global valueRound
    if len(blackjack) > 0:
        for i in range(len(blackjack)):
            ListPlayers[codBlackjack[i]-1][3] += valueRound/len(blackjack)
            ListPlayers[codBlackjack[i]-1][4] += 1
        print("TIVEMOS BLACKJACK")
        valueRound = 0
        return blackjack

    elif len(winners) > 0 :
        #Se tiver mais que um vencedor, vai dividir o lucro entre os dois e a vitoria para os dois tambem
        for i in range(len(winners)):
            ListPlayers[codWinners[i]-1][3] += valueRound/len(winners)
            ListPlayers[codWinners[i]-1][4] += 1
        valueRound = 0
        return winners

    #Caso ninguem tenha tido 21, da o valor total ao vencedor e a vitoria
    else:
        for i in range(len(ListPlayers)):
            ListPlayers[i][3] += valueRound/len(ListPlayers)
        valueRound = 0
        print("\nNão tivemos vencedores, todos estouraram! \nO valor foi redividido entre todos os jogadores!\n")
        return winners

    

#Mostra o montante de dinheiro que o jogador tem
def ShowAmount(player):
    print("Carteira: R$",player[3])


#Controla o decorrer da rodada
def Round(ListPlayers,numRound,cheap):
    print("\n\n*********** BLACKJACK ***********\n***********  ROUND ",numRound+1,"***********\n")
    
    for i in range(len(ListPlayers)):
        print("\nVez do jogador: ", ListPlayers[i][1])
        ShowAmount(ListPlayers[i])
        ListPlayers[i] = Bet(ListPlayers[i])
    
    #Entrega duas cartas para os jogadores
    GiveCards(ListPlayers,cheap)
    #Da a opção de comer novamente ou não
    for i in range(len(ListPlayers)):
        print("\n_____ JOGADA _____")
        print("\nVez do jogador: ", ListPlayers[i][1])
        ShowAmount(ListPlayers[i])

        ListPlayers[i][6] = CountCards(ListPlayers[i][5])

        print("\nCartas: ", ListPlayers[i][5], "\nValor Atual: ", ListPlayers[i][6])
        ListPlayers[i] = eat(ListPlayers[i], cheap) 
    
    print("\n\n*********************************\n** O Vencedor foi: ", win(ListPlayers), "**\n*********************************")


#Função principal do jogo
def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            print("\n*********************************\n*********** BLACKJACK ***********\n*********************************\n")
            numPlayers = 1
            numGame = 0
            numRound = 0

            while(True):
                
                if(numPlayers == 6):
                    print("Limite de jogadores atingido!")
                    break
                else:
                    InfoPlayer(numPlayers)
                    print("\n---------------------------------")
                    newPlayer = input("\n----> Inserir novo jogador? [s/n] \n----> ")
                    print("\n---------------------------------\n")
                    if(newPlayer == "s" or newPlayer == "S" or newPlayer == "Sim" or newPlayer == "SIM" or newPlayer == "sim"):
                        numPlayers += 1
                    else:
                        break

            while(True):       
                play = int(input("_____ OPÇÕES DE JOGO: _____\n\n1 - Jogar\n2 - Sair\n----> "))
                
                if(play == 1):                    

                    #Cria um baralho com 52 cartas e embaralha as cartas
                    cheap = ResetCheap()

                    #Inicia o primeiro Round do jogo
                    Round(ListPlayers,numRound,cheap)
                    numRound += 1
                   
                    #Finaliza o jogo ou inicia um novo Round 
                    keepPlaying = input("\nContinuar jogando? [s/n] \n----> ")
                    if(keepPlaying == "s" or keepPlaying == "S" or keepPlaying == "sim"):
                        Round(ListPlayers,numRound,cheap)
                        numGame +=1
                    else:
                        print('\n*********************************\n************ PLACAR ************\n*********************************\n')
                        for i in range(len(ListPlayers)):
                            print("\n", ListPlayers[i][1],"\n---------------------------------\nCidade: ",ListPlayers[i][2],"\nCarteira: R$", ListPlayers[i][3], "\nVitorias: ", ListPlayers[i][4], "\n")
                        s.close()
                        break


                    teste = ""
                    s.send(teste.encode()) #.encode - converte a string para bytes
                    data = s.recv(BUFFER_SIZE)
                    texto_recebido = repr(data) #converte de bytes para um formato "printável"
                    print('Recebido do servidor', texto_recebido)
                    texto_string = data.decode('utf-8') #converte os bytes em string
                    
                    
                elif(play == 2):
                    print("Saindo do jogo")
                    for i in range(len(ListPlayers)):
                        print("\n", ListPlayers[i][1],"\n---------------------------------\nCidade: ",ListPlayers[i][2],"\nCarteira: R$", ListPlayers[i][3], "\nVitorias: ", ListPlayers[i][4], "\n")
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
