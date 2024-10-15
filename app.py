import serial
import time

# Configure a porta serial
ser = serial.Serial('COM4', 9600, timeout=1)  # Substitua 'COM4' pela sua porta serial

# Dicionário para armazenar os usuários cadastrados (UID -> Nome)
users = {}

# Função para ler o UID do cartão RFID (somente quando solicitado)
def read_serial():
    while True:
        if ser.in_waiting > 0:
            try:
                raw_data = ser.readline()  # Lê os bytes brutos
                uid = raw_data.decode(errors='replace').strip()  # Decodifica e remove espaços
                if uid:  # Verifica se UID não está vazio
                    print(f"UID lido: {uid}")  # Exibe o UID lido
                    return uid
            except Exception as e:
                print(f"Erro ao ler da serial: {e}")
        time.sleep(0.1)  # Pequeno atraso para não sobrecarregar a leitura

# Função para registrar um novo usuário
def register_user():
    name = input("Digite o nome do usuário: ")  # Solicita o nome do usuário
    print(f"Aproxime o cartão para associar ao usuário '{name}'...")

    uid = read_serial()  # Captura o UID do cartão RFID
    if uid in users:
        print(f"O UID {uid} já está cadastrado para o usuário: {users[uid]}. Tente outro cartão.")
    else:
        users[uid] = name  # Cadastra o nome associado ao UID
        print(f"Usuário '{name}' cadastrado com sucesso com o UID: {uid}")

# Função para remover um usuário
def remove_user():
    print("Aproxime o cartão que deseja remover...")

    uid = read_serial()  # Captura o UID do cartão RFID
    if uid in users:
        del users[uid]
        print(f"Usuário com UID {uid} removido com sucesso.")
    else:
        print(f"UID {uid} não encontrado no sistema.")

# Função para acessar um usuário
def access_user():
    print("Aproxime o cartão para acessar...")

    uid = read_serial()  # Captura o UID do cartão RFID
    if uid in users:
        print(f"Acesso concedido. Usuário: {users[uid]}")
    else:
        print(f"UID {uid} não encontrado.")

# Função para listar todos os usuários
def list_users():
    if users:
        print("\nUsuários cadastrados:")
        for uid, name in users.items():
            print(f"UID: {uid}, Nome: {name}")
    else:
        print("Nenhum usuário cadastrado.")

# Função principal para gerenciamento do terminal
def handle_user_input():
    while True:
        print("\nOpções disponíveis:")
        print("1. Adicionar um novo usuário")
        print("2. Remover um usuário")
        print("3. Acessar um usuário")
        print("4. Listar todos os usuários")
        print("5. Sair")

        choice = input("Digite o número da opção: ")

        if choice == '1':
            register_user()  # Função para registrar novo usuário
        elif choice == '2':
            remove_user()  # Função para remover um usuário
        elif choice == '3':
            access_user()  # Função para acessar um usuário
        elif choice == '4':
            list_users()  # Função para listar todos os usuários
        elif choice == '5':
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    handle_user_input()
