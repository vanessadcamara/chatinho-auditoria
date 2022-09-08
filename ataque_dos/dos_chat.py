import socket
import sys
import threading
import os
import time
import names
from datetime import datetime

class Cliente:
	'''Usuário do bate-papo'''

	def __init__(self, host = '127.0.0.1', port = 9999):
		'''Inicializa as variáveis iniciais do cliente'''
		self.host = host
		self.port = port


	def cria_conexao_tcp(self):
		'''Cria conexão TCP com o servidor'''
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#Cria a conexão TCP 
		except:
			print('Erro ao criar o socket')
			os._exit(1)

		dest = (self.host, self.port)
		try:
			self.s.connect(dest)	#conecta ao servidor

		except:
			print("Servidor não está conectado no momento.")
			sys.exit()

	def main(self):
		'''Começa a execução do cliente, conecta socket TCP '''

		self.cria_conexao_tcp()

		# pegando a chave publica do servidor
		self.SERVIDOR_KEY = self.s.recv(2048).decode('utf-8')
		# enviando a minha chave publica
		self.s.send(b'key')
		# mandando o apelido para o servidor
		msg = self.s.recv(4096).decode('utf-8')
		apelido = names.get_full_name()
		self.s.sendall(apelido.encode('utf-8'))
		arq = open('contador.txt', 'r')
		contador = int(arq.readline())
		arq.close()
		print(f"Usuario {apelido} de numero {contador} criado!")
		arq = open('contador.txt', 'w')
		arq.write(str(contador+1))
		arq.close()

if __name__ == "__main__":
	cliente = Cliente()
	cliente.main()