
from src.usuario import Usuario
import psycopg2


class Sistema:

    def __init__(self):
        self.conexao = psycopg2.connect(host="localhost", database="dez_seis", user="postgres", password="postgres")
        self.usuario_logado = self.login()
        self.mostrar_menu()

    def cadastrar_conta(self):
        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")
        idade = int(input("Idade: "))
        apelido = input("Apelido: ")

        cursor = self.conexao.cursor()
        cursor.execute(
            'INSERT INTO usuario(nome, email, idade, senha, apelido) VALUES (%s, %s, %s, %s, %s)',
            (nome, email, idade, senha, apelido)
        )
        cursor.close()
        self.conexao.commit()

    def remover_conta(self, usuario_logado):
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM usuario WHERE email=\'{}\''.format(self.usuario_logado.email))
        cursor.close()
        exit()

    def listar_usuarios(self):
        for usuario in self.usuarios:
            print(usuario)

    def deslogar(self):
        self.usuario_logado = self.login()

    def mostrar_menu(self):

        while True:
            opcao = input('\n\tmenu principal:'
                          '\nC conta'
                          '\nU usuarios'
                          '\nd deslogar'
                          '\n> ')
            if opcao == 'C':
                while True:
                    opcao = input('\n\t\tconta:'
                                  '\nmudar:'
                                  '\n\ts status'
                                  '\n\ta apelido'
                                  '\n\ti idade'
                                  '\n\tn nome'
                                  '\n'
                                  '\nd desativar'
                                  '\n> ')
                    if opcao == 's':
                        novo_status = input('novo status: ')
                        self.usuario_logado.set_status(novo_status)
                    elif opcao == 'a':
                        novo_apelido = input('novo apelido: ')
                        self.usuario_logado.set_apelido(novo_apelido)
                    elif opcao == 'i':
                        nova_idade = int(input('Idade: '))
                        self.usuario_logado.set_idade(nova_idade)
                    elif opcao == 'n':
                        novo_nome = input('Nome: ')
                        self.usuario_logado.set_nome(novo_nome)
                    elif opcao == 'd':
                        self.remover_conta(self.usuario_logado)
                    elif opcao == '\\':
                        break
                    else:
                        print('opção inválida')

            elif opcao == 'U':
                while True:
                    opcao = input('\n\tusuarios:'
                                  '\nl listar'
                                  '\n> ')
                    if opcao == 'l':
                        self.listar_usuarios()
                    elif opcao == '\\':
                        break

            elif opcao == 'd':
                self.deslogar()
            elif opcao == '\\':
                print('nenhum menu acima deste')
            else:
                print('opção inválida')

    def login(self):
        tem_conta = input("Tens conta? (s/n): ")

        if tem_conta == "s":
            while True:
                email = input("Email: ")
                senha = input("Senha: ")

                cursor = self.conexao.cursor()
                cursor.execute('SELECT * from usuario where email=\'{}\''.format(email))
                tupla = cursor.fetchone()
                cursor.close()
                if tupla[3] == senha:
                    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5])
                else:
                    print('senha inválida')
        else:
            deseja_ter_conta = input("Desejas uma? (s/n): ")

            if deseja_ter_conta == "s":
                return self.cadastrar_conta()
            else:
                exit()
