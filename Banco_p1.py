import PySimpleGUI as Sg  # python -m pip install pysimplegui
import sqlite3 as sql  # pip install db-sqlite3
banco = sql.connect('dados_banco.db')
cursor = banco.cursor()
def pag_criar_banco():
    Sg.theme('DarkGreen4')
    layout_pag_criar = [
                        [Sg.Text('Deseja Criar um Banco De Dados?')],
                        [Sg.Button('Sim', button_color='#008000'), Sg.Button('Não', button_color='#FF0000'),]
                       ]
    tela_criar_banco = Sg.Window('Criar Banco', layout_pag_criar)
    while True:
        eventos, valores = tela_criar_banco.read()
        if eventos == Sg.WIN_CLOSED:
            tela_criar_banco.close()
            break
        if eventos == 'Sim':
            cursor.execute("CREATE TABLE cadastroB (email varchar(20), senha varchar(15), agencia int, dinheiro int)")
            banco.commit()
            tela_criar_banco.close()
            pag_cadastro()
        if eventos == 'Não':
            tela_criar_banco.close()
            pag_cadastro()
def pag_cadastro():
    Sg.theme('DarkGreen4')
    layout_Cadastro = [
        [Sg.Text('Cadastro')],
        [Sg.Text('Email: '), Sg.Input(key='Email')],
        [Sg.Text('Senha:'), Sg.Input(key='Senha')],
        [Sg.Radio("Banco Do Brasil", "agencias", key='Bb'), Sg.Radio("Bradesco", "agencias", key='Br'), Sg.Radio("Itaú", "agencias", key='It'), Sg.Radio("Outro","agencias", key='Ot')],
        [Sg.Button('Enviar'), Sg.Button('Login')]
    ]
    Tela_Cadastro = Sg.Window('Cadastro', layout_Cadastro)

    while True:
        evento, valor = Tela_Cadastro.read()
        email = (valor['Email'])
        senha = (valor['Senha'])
        agencia = 0
        if valor['Bb'] == True:
            agencia = 2
        if valor['Br'] == True:
            agencia = 3
        if valor['It'] == True:
            agencia = 4
        if valor['Ot'] == True:
            agencia = 5
        email = str(email)
        senha = str(senha)
        if evento == Sg.WIN_CLOSED:
            break
        if evento == 'Login':
            Tela_Cadastro.close()
            pag_Login()
            break
        if evento == 'Enviar' and email != "" and senha != "" and agencia != 0:
            cursor = banco.cursor()
            inserirdados = (f"INSERT INTO cadastroB VALUES('{email}', '{senha}', '{agencia}', 1000)")
            cursor.execute(inserirdados)
            banco.commit()
            cursor.close()
            Tela_Cadastro.close()
            pag_Login()
        elif evento == 'Enviar' and email == "" or senha == "" or agencia == 0:
            Sg.Popup('Email ou Senha ou agência Faltando')
def pag_Login():
    Sg.theme('DarkGreen4')
    layout_Login = [
        [Sg.Text('Digite o Email:'), Sg.Input(key='EmailC')],
        [Sg.Text('Digite a Senha'), Sg.Input(key='SenhaC')],
        [Sg.Radio("Banco Do Brasil", "agencias", key='Bb'), Sg.Radio("Bradesco", "agencias", key='Br'), Sg.Radio("Itaú", "agencias", key='It'), Sg.Radio("Outro", "agencias", key='Ot')],
        [Sg.Button('Entrar'), Sg.Button('Sair')]
    ]
    tela_Login = Sg.Window('Login', layout_Login)
    while True:
        eventos, valor = tela_Login.read()
        email = str(valor['EmailC'])
        senha = str(valor['SenhaC'])
        agencia = 0
        if valor['Bb'] == True:
            agencia = 2
        if valor['Br'] == True:
            agencia = 3
        if valor['It'] == True:
            agencia = 4
        if valor['Ot'] == True:
            agencia = 5
        if eventos == 'Entrar':
                validar = (f" SELECT senha FROM cadastroB WHERE email = '{email}' AND agencia = {agencia} ")
                cursor.execute(validar)
                dados = str(cursor.fetchall())
                dados = dados[3:(len(dados) - 4)]
                if senha == dados and senha != "" and email != "" and agencia != 0:
                    tela_Login.close()
                    pag_transac(email, senha)
                else:
                    Sg.popup('Errado')
        if eventos == Sg.WIN_CLOSED:
            break

def pag_transac(email, senha):
    cursor.execute(f"SELECT dinheiro FROM cadastroB WHERE email = '{email}' AND senha = '{senha}'")
    dinheiro_conta = cursor.fetchall()
    dinheiro_conta = str(dinheiro_conta[0])
    dinheiro_conta = (dinheiro_conta[1:len(dinheiro_conta) - 2])
    dinheiro_conta = int(dinheiro_conta)
    Sg.theme('DarkGreen4')
    layout = [
        [Sg.Text(f'Seu saldo é de {dinheiro_conta}')],
        [Sg.Text('Depositar:'), Sg.Input(key='Deposito')],
        [Sg.Text('Sacar:     '), Sg.Input(key='Saque')],
        [Sg.Button('Enviar')]
    ]
    tela = Sg.Window("Pag Transação", layout)
    while True:
        evento, valor = tela.read()
        if evento == Sg.WIN_CLOSED:
            break
        if evento == 'Enviar':
            saque = valor['Saque']
            if saque in ("", None):
                saque = 0
            saque = int(saque)
            deposito = valor['Deposito']
            if deposito in ("", None):
                deposito = 0
            deposito = int(deposito)
            if saque > dinheiro_conta or saque < 0:
                Sg.popup('Saldo insuficiênte em conta')
            elif saque <= dinheiro_conta:
                dinheiro_conta = (dinheiro_conta + (deposito - saque))
                layout = [
                    [Sg.Text(f'Seu saldo é de {dinheiro_conta}')],
                    [Sg.Text('Depositar:'), Sg.Input(key='Deposito')],
                    [Sg.Text('Sacar:     '), Sg.Input(key='Saque')],
                    [Sg.Button('Enviar')]
                ]
                tela.close()
                tela = Sg.Window("Pag Transação", layout)
                cursor.execute(f"UPDATE cadastroB SET Dinheiro = '{dinheiro_conta}' WHERE email = '{email}' AND senha = '{senha}'")
                banco.commit()
pag_criar_banco()