# importações
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
from cryptography.fernet import Fernet
import socket
from datetime import datetime

# criação da senha
senha = ''
while(len(senha) not in (16, 24, 32)):
    senha = input("Crie uma senha de 16, 24 ou 32 caracteres: ")
    
# criação da chave inicial
chave_inicial = senha.encode()

# criação da IV, que possui o mesmo tamanho da chave inicial
IV = b'A' * len(chave_inicial) 

# geração da chave que será utilizada nas mensagens
chave_mensagens = Fernet.generate_key()
# print("Chave do fernet:", chave_mensagens)

# criação da função que garante que uma mensagem encriptografada 
# não pode ser manipulada ou lida sem a chave
funcao_cripto_mensagens = Fernet(chave_mensagens)

def encriptografar(mensagem):
    encryptor = AES.new(chave_inicial, AES.MODE_CBC, IV)
    padded_mensagem = Padding.pad(mensagem, 16)
    mensagem_encriptografada = encryptor.encrypt(padded_mensagem)
    return mensagem_encriptografada

# inicialização do socket
s = socket.socket()

# captura do host
host = socket.gethostname() 
print('Servidor vai começar no host: ', host)
port = 8080

# Vincula o socket ao endereço
s.bind((host, port))
print('Esperando conexão...\n')

# Quantidade de conexões do servidor
s.listen(1)
conn, addr = s.accept()
print(addr, 'conectou ao servidor.\n')

# Envio da chave criptografada
conn.send(encriptografar(chave_mensagens))

# Recebimento da confirmação da criptografia
mensagem_recebida = conn.recv(1024)
# print("Mensagem recebida: ", mensagem_recebida)

# Descriptografar a mensagem recebida
mensagem_recebida = funcao_cripto_mensagens.decrypt(mensagem_recebida).decode()
print('[{}] Cliente >> {}'.format(datetime.today().strftime('%H:%M'), mensagem_recebida))

while 1:
    mensagem = input('[{}] Servidor >> '.format(datetime.today().strftime('%H:%M')))
    mensagem = mensagem.encode()
    conn.send(funcao_cripto_mensagens.encrypt(mensagem))
    mensagem_recebida = conn.recv(1024)
    # print("Mensagem recebida: ", mensagem_recebida)
    mensagem_recebida = funcao_cripto_mensagens.decrypt(mensagem_recebida).decode()
    print('[{}] Cliente >> {}'.format(datetime.today().strftime('%H:%M'), mensagem_recebida))
    