import textwrap

def menu():
    menu = '''\n
    ================ MENU ================
    Escolha a operação:

    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [0]\tSair
    =>'''
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R${valor:.2f}\n'
        print('\n=== Depósito realizado com sucesso. ===')
    else:
        print('\n@@@ Valor inválido para depósito. @@@')

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques < limite_saques:
        
        if valor <= 0:
            print('\n@@@ Valor de saque inválido. @@@')
        elif valor > limite:
            print('\n@@@ Valor solicitado maior que o limite por saque. @@@')
        elif valor > saldo:
            print('\n@@@ Saldo insuficiente. @@@')
        else:
            numero_saques += 1
            saldo -= valor
            extrato += f'Saque:\t\t R${valor:.2f}\n'
            print('\n=== Saque realizado com sucesso. ===')

    else:
        print('\n@@@ Limite de Saques excedido. @@@')

    return saldo, extrato

def extrato_bancario(saldo, /, *, extrato):
    print('\n\nExtrato: \n')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'\nSaldo atual:\t\tR$ {saldo:.2f}\n')

def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n@@@ Já existe usuário para o CPF informado. @@@')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, n - bairro - cidade/estado): ')

    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})

    print('=== Usuário criado com sucesso. ===')

def filtrar_usuario(cpf, usuarios):
    usuario_filtrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuario_filtrado[0] if usuario_filtrado else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('=== Usuário criado com sucesso. ===')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    
    print('\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado. @@@')

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUE = 3
    AGENCIA = '0001'
    
    saldo = 0.00
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == '1':
            valor = float(input('Informe o valor do depósito: '))

            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opcao == '2':
            valor = float(input('Informe o valor do saque: '))

            saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUE,)

        elif opcao == '3':
            extrato_bancario(saldo, extrato=extrato)

        elif opcao == '4':
            criar_usuario(usuarios)

        elif opcao == '5':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == '6':
            listar_contas(contas)


        elif opcao == '0':
            break

        else:
            print('Opção inválida, favor selecionar uma operação válida.')

main()