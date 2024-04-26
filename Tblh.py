import PySimpleGUI as Sg  # python -m pip install pysimplegui
import mysql.connector  # pip install mysql-connector-python
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mneto0710@',
    database='testecoisa',
)
def pag_cadastro():
    layout_Cadastro = [
        [Sg.Text('Cadastro')],
        [Sg.Text('Email:'), Sg.Input(key='Email')],
        [Sg.Text('Senha:'), Sg.Input(key='Senha')],
        [Sg.Button('Confirmar'), Sg.Button('Login')]
    ]
    Tela_Cadastro = Sg.Window('Cadastro', layout_Cadastro)

    while True:
        evento, valor = Tela_Cadastro.read()
        email = (valor['Email'])
        senha = (valor['Senha'])
        email = str(email)
        senha = str(senha)
        if email and senha != "":
            if evento == 'Confirmar':
                cursor = conexao.cursor()
                inserirdados = f""" INSERT INTO cadastro_banco VALUES ("{email}", "{senha}")"""
                cursor.execute(inserirdados)
                conexao.commit()
                cursor.close()
                Tela_Cadastro.close()
                pag_Login()
        else:
            Sg.Popup('Errado')
        if evento == Sg.WIN_CLOSED:
            break
        if evento == 'Login':
            Tela_Cadastro.close()
            pag_Login()
def pag_Login():
    layout_Login = [
        [Sg.Text('Digite o Email:'), Sg.Input(key='EmailC')],
        [Sg.Text('Digite a Senha'), Sg.Input(key='SenhaC')],
        [Sg.Button('Entrar'), Sg.Button('Sair')]
    ]
    Tela_Login = Sg.Window('Login', layout_Login)
    while True:
        eventos, valores = Tela_Login.read()
        email = str(valores['EmailC'])
        senha = str(valores['SenhaC'])
        if eventos == 'Entrar':
                cursor = conexao.cursor()
                Validar = f""" SELECT senha FROM cadastro_banco WHERE email = "{email}" """
                cursor.execute(Validar)
                dados = str(cursor.fetchall())
                dados = dados[3:(len(dados) - 4)]
                if senha == dados and senha != "" and email != "":
                    Tela_Login.close()
                    pag_Inic(1000)
                else:
                    Sg.popup('Errado')

def pag_Inic(z):  # Função Para Definir A Tela De Depositos E Saques
    layoutA = [  # Vai Definir As Posições e o Estilo Das Funcionalidades
        [Sg.Text(f"Seu Saldo é de {z}R$")],
        [Sg.Text("Depositar"), Sg.Input(key='Depositar')],  # Input De Deposito
        [Sg.Text("Sacar"), Sg.Input(key='Sacar')],  # Input De Saque
        [Sg.Button('Inserir'), Sg.Button('Sair')],
    ]
    telaA = Sg.Window('Tela Banco', layoutA)
    while True:
        evento, valor = telaA.read()
        if evento in (Sg.WIN_CLOSED, 'Sair'):
            break
        deposito = valor['Depositar']
        saque = valor['Sacar']
        if deposito in ("", None):
            deposito = 0
        if saque in ("", None):
            saque = 0
        deposito = int(deposito)
        saque = int(saque)
        if evento == 'Inserir' and deposito < 0:
            Sg.popup('Deposito Inválido')
        if evento == 'Inserir' and saque > z:
            Sg.popup('Saldo Insuficiente')
        if evento == 'Inserir' and saque <= z and deposito >= 0:
            z = (z - saque + deposito)
            pag_operacao(z)
            telaA.hide()
            telaA.close()
        layoutA = [
            [Sg.Text(f"Seu Saldo é de {z}R$")],
            [Sg.Text("Depositar"), Sg.Input(key='Depositar')],
            [Sg.Text("Sacar"), Sg.Input(key='Sacar')],
            [Sg.Button('Inserir'), Sg.Button('Sair')],
        ]
        telaA = Sg.Window('Tela Banco', layoutA)
def pag_operacao(y):
    layoutB = [
        [Sg.Text(f"Sua conta possui {y}R$")],
        [Sg.Button('Voltar'), Sg.Button('Sair')]
    ]
    telaB = Sg.Window('Tela Extrato', layoutB)
    while True:
        events,values = telaB.read()
        if events == 'Sair':
            quit()
        if events in (Sg.WIN_CLOSED, 'Voltar'):
            telaB.close()
            break
pag_cadastro()
