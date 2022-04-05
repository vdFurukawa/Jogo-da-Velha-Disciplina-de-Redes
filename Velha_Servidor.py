from calendar import c
from http import client
from msilib.schema import Class
from pydoc import cli
import socket
import threading

class Velha:

    def __init__(self):
        self.tabuleiro = [ ["-", "-", "-"], 
                         ["-", "-", "-"], 
                         ["-", "-", "-"] ]
        self.turno = "X"
        self.voce = "X"
        self.oponente = "O"
        self.vencedor = None
        self.gameOver = False

        self.contador = 0

    def Host(self ,host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(5)

        client, addr = server.accept()

        self.voce = "X"
        self.oponente = "O"
        threading.Thread(target=self.handleConnection, args=(client,)).start()
        
    
    def connectGame(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.voce = "O"
        self.oponente = "X"
        threading.Thread(target=self.handleConnection, args=(client,)).start()

    def handleConnection(self, client):
        while not self.gameOver:
            if self.turno == self.voce:
                move = input("Faça um movimento (Ex: 0(linha),1(coluna)): ")
                if self.checkMovimentoValido(move.split(',')):
                    client.send(move.encode('utf-8'))
                    self.applyMove(move.split(','), self.voce)
                    self.turno = self.oponente
                else: 
                    print("Alguém já escolheu esse lugar!!")
            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                    break
                else:
                    self.applyMove(data.decode('utf-8').split(','), self.oponente)
                    self.turno = self.voce
        client.close()
    
    def applyMove(self, move, jogador):
        if self.gameOver:
            return
        self.contador += 1
        self.tabuleiro[int(move[0])] [int(move[1])] = jogador
        self.printTabuleiro()
        if self.checkSeGanhou():
            if self.vencedor == self.voce:
                print("Você Ganhou!!")
                exit()
            elif self.vencedor == self.oponente:
                print("Você Perdeu!!")
                exit()
        else:
            if self.contador == 9:
                print("EMPATOU!!")
                exit()
    
    def checkMovimentoValido(self, move):
        return self.tabuleiro[int(move[0])][int(move[1])] == "-"

    def checkSeGanhou(self):
        for row in range (3):
            if self.tabuleiro[row][0] == self.tabuleiro[row][1] == self.tabuleiro[row][2] != "-":
                self.vencedor == self.tabuleiro[row][0]
                self.gameOver == True
                return True
        for col in range (3):
            if self.tabuleiro[0][col] == self.tabuleiro[1][col] == self.tabuleiro[2][col] != "-":
                self.vencedor == self.tabuleiro[0][col]
                self.gameOver == True
                return True
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != "-":
            self.vencedor == self.tabuleiro[0][0]
            self.gameOver = True
            return True
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != "-":
            self.vencedor == self.tabuleiro[0][2]
            self.gameOver = True
            return True
        return False

    def printTabuleiro(self):
        for row in range (3):
            print(" | ".join(self.tabuleiro[row]))
            if row != 2: 
                print("__|___|___")

game = Velha()
game.Host("", 1200)