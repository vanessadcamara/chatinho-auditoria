import socket

from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
from cryptography.fernet import Fernet
import socket

senha = ''
while(len(senha) not in (16, 24, 32)):
    senha = input("Crie uma senha de 16, 24 ou 32 caracteres: ")
# criação da chave inicial
chave_inicial = senha.encode()
#criação da IV, que possui o mesmo tamanho da chave inicial
IV = b"A" * len(chave_inicial) 
# geração da chave que será utilizada nas mensagens
chave_mensagens = Fernet.generate_key() 
# criação da função que garante que uma mensagem encriptografada não pode ser manipulada ou lida sem a chave.
funcao_cripto_mensagens = Fernet(chave_mensagens)

def encrypt(message):
    encryptor = AES.new(chave_inicial, AES.MODE_CBC, IV)
    padded_message = Padding.pad(message, 16)
    encrypted_message = encryptor.encrypt(padded_message)
    return encrypted_message
s = socket.socket()
host = socket.gethostname()
print(' Server will start on host : ', host)
port = 8080
s.bind((host, port))
print('Waiting for connection\n')
s.listen(1)
conn, addr = s.accept()
print(addr, 'Has connected to the server\n')
conn.send(encrypt(chave_mensagens))
incoming_message = conn.recv(1024)
incoming_message = funcao_cripto_mensagens.decrypt(incoming_message).decode()
print(' Client : ', incoming_message)
while 1:
    message = input(str('>> '))
    message = message.encode()
    conn.send(funcao_cripto_mensagens.encrypt(message))
    print('Sent\n')
    incoming_message = conn.recv(1024)
    incoming_message = funcao_cripto_mensagens.decrypt(incoming_message).decode()
    print(' Client: ', incoming_message, "\n")
    