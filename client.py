# importações
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
from cryptography.fernet import Fernet
import socket

# inserção da senha para conexão
senha = ''
while(len(senha) not in (16, 24, 32)):
    senha = input("Insira a senha: ")

# criação da chave inicial
chave_inicial = senha.encode()

# criação da IV, que possui o mesmo tamanho da chave inicial
IV = b"A" * len(chave_inicial)

def descriptografar(mensagem):
    descriptografador = AES.new(chave_inicial, AES.MODE_CBC, IV)
    decrypted_padded_message = descriptografador.decrypt(mensagem)
    mensagem_descriptografada = Padding.unpad(decrypted_padded_message, 16)
    return mensagem_descriptografada
    
# inicialização do socket
s = socket.socket()

# captura do host
host = input('Entre com hostname: ')
port = 8080

# Vincula o socket ao endereço
s.connect((host, port))
print('Conectado com o servidor do chat')

# Envio da confirmação da criptografia
chave_mensagens = s.recv(1024)
# print("Chave recebida criptografada: ", chave_mensagens)

# Descriptografar a chave das mensagens
chave_mensagens = descriptografar(chave_mensagens)
# print("Chave recebida descriptografada: ", chave_mensagens)
funcao_cripto_mensagens = Fernet(chave_mensagens)

# Envio da confirmação da criptografia
s.send(funcao_cripto_mensagens.encrypt(b'criptografia iniciada'))

while 1:
    incoming_message = s.recv(1024)
    # print("Mensagem recebida: ", incoming_message)
    incoming_message = funcao_cripto_mensagens.decrypt(incoming_message).decode()
    print('Servidor >> ', incoming_message)
    mensagem = input('Cliente >> ')
    mensagem = mensagem.encode()
    s.send(funcao_cripto_mensagens.encrypt(mensagem))