# -*- coding: utf-8 -*-
import socket, sys

HOST = '127.0.0.1'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados

Players = []

class AddPlayer:
    """User class for representing name, city, amount and victories of players"""
    def _init_(self, amount, victories):
        name_user = input('----> Digite seu nome: ')
        city_user = input('----> Digite sua cidade: ')
        """Create a new Player"""
        self.name = name_user
        self.city = city_user
        self.amount = amount
        self.victories = victories

    def getName(self):
        return self.name

    def getCity(self):
        return self.city

    def getAmount(self):
        return self.amount

    def getVictories(self):
        return self.victories

def main(argv): 

    users = [[]]

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            print("\n*********** BLACKJACK ***********")
            

            while(True):       
                    
                p1 = AddPlayer()
                

                #s.send(texto.encode()) #texto.encode - converte a string para bytes
                data = s.recv(BUFFER_SIZE)
                texto_recebido = repr(data) #converte de bytes para um formato "printável"
                print('Recebido do servidor', texto_recebido)
                texto_string = data.decode('utf-8') #converte os bytes em string
                if (texto_string == 'bye'):
                    print('vai encerrar o socket cliente!')
                    s.close()
                    break

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])
