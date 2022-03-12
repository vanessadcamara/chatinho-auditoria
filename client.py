from ctypes import sizeof
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
from cryptography.fernet import Fernet
import socket

senha = ''
while(len(senha) != 16):
    senha = input("Insira a senha: ")

chave_inicial = senha.encode()
IV = b"A" * len(chave_inicial)

def decrypt(cipher):
    decryptor = AES.new(chave_inicial, AES.MODE_CBC, IV)
    decrypted_padded_message = decryptor.decrypt(cipher)
    decrypted_message = Padding.unpad(decrypted_padded_message, 16)
    return decrypted_message

s = socket.socket()
host = input(str('Enter hostname or host IP: '))
port = 8080
s.connect((host, port))
print('Connected to chat server')

chave_mensagens = s.recv(1024)
chave_mensagens = decrypt(chave_mensagens)
funcao_cripto_mensagens = Fernet(chave_mensagens)
s.send(b'criptografia iniciada')

while 1:
    incoming_message = s.recv(1024)
    incoming_message = funcao_cripto_mensagens.decrypt(incoming_message).decode()
    print('Server : ', incoming_message, "\n")
    message = input(str('>> '))
    message = message.encode()
    s.send(funcao_cripto_mensagens.encrypt(message))
    print('Sent\n')