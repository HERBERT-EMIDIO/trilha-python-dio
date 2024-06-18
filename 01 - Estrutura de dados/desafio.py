# Importa o módulo textwrap, que será usado para manipular strings com quebras de linha e indentação
import textwrap

# Define a função que exibe o menu e solicita a entrada do usuário
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    # Usa textwrap.dedent para remover indentação comum
    return input(textwrap.dedent(menu))

# Define a função para realizar depósitos
def depositar(saldo, valor, extrato, /): # '/'para ser passado na ordem correta 
    if valor > 0:  # Verifica se o valor do depósito é positivo
        saldo += valor  # Adiciona o valor ao saldo
        extrato += f"Depósito:\tR$ {valor:.2f}\n"  # Registra o depósito no extrato
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato  # Retorna o saldo atualizado e o extrato

# Define a função para realizar saques
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo  # Verifica se o valor do saque é maior que o saldo
    excedeu_limite = valor > limite  # Verifica se o valor do saque é maior que o limite permitido
    excedeu_saques = numero_saques >= limite_saques  # Verifica se o número de saques excedeu o limite diário

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor  # Subtrai o valor do saque do saldo
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"  # Registra o saque no extrato
        numero_saques += 1  # Incrementa o número de saques realizados
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato  # Retorna o saldo atualizado e o extrato

# Define a função para exibir o extrato
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    # Verifica se há movimentações no extrato e imprime
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

# Define a função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")  # Solicita o CPF do usuário
    usuario = filtrar_usuario(cpf, usuarios)  # Verifica se o usuário já existe

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")  # Solicita o nome do usuário
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")  # Solicita a data de nascimento
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")  # Solicita o endereço

    # Adiciona o novo usuário à lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

# Define a função para filtrar um usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    # Retorna o primeiro usuário encontrado com o CPF informado ou None se não encontrar
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Define a função para criar uma nova conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")  # Solicita o CPF do usuário
    usuario = filtrar_usuario(cpf, usuarios)  # Busca o usuário pelo CPF

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        # Retorna os dados da nova conta
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

# Define a função para listar todas as contas
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        # Imprime os dados da conta formatados
        print(textwrap.dedent(linha))

# Define a função principal que controla o fluxo do programa
def main():
    LIMITE_SAQUES = 3  # Define o limite de saques diários
    AGENCIA = "0001"  # Define o número da agência

    saldo = 0  # Inicializa o saldo
    limite = 500  # Define o limite de saque
    extrato = ""  # Inicializa o extrato
    numero_saques = 0  # Inicializa o contador de saques
    usuarios = []  # Inicializa a lista de usuários
    contas = []  # Inicializa a lista de contas

    while True:
        opcao = menu()  # Exibe o menu e solicita uma opção do usuário

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)  # Realiza o depósito

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )  # Realiza o saque

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)  # Exibe o extrato

        elif opcao == "nu":
            criar_usuario(usuarios)  # Cria um novo usuário

        elif opcao == "nc":
            numero_conta = len(contas) + 1  # Gera um novo número de conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios)  # Cria a nova conta

            if conta:
                contas.append(conta)  # Adiciona a conta à lista de contas

        elif opcao == "lc":
            listar_contas(contas)  # Lista todas as contas

        elif opcao == "q":
            break  # Encerra o loop e finaliza o programa

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Executa a função principal
main()
