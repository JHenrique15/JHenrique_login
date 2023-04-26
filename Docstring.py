import bcrypt
import mysql.connector
import tkinter as tk


class UsuarioDAO:
    """
    Classe que gerencia o acesso e manipulação dos usuários na base de dados.
    """

    def __init__(self):
        """
        Inicializa uma conexão com a base de dados.
        """

        self.__conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='usuarios_db'
        )

    def criar_usuario(self, nome, email, senha):
        """
        Cria um novo usuário na base de dados.

        :param nome: nome do usuário a ser criado.
        :param email: e-mail do usuário a ser criado.
        :param senha: senha do usuário a ser criado.
        """

        cursor = self.__conexao.cursor()
        hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)', (nome, email, hashed))
        self.__conexao.commit()
        cursor.close()

    def buscar_usuario_por_email(self, email):
        """
        Busca um usuário na base de dados pelo seu e-mail.

        :param email: e-mail do usuário a ser buscado.
        :return: dicionário com as informações do usuário encontrado, ou None se não encontrar.
        """

        cursor = self.__conexao.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario

    def buscar_usuario_por_id(self, id):
        """
        Busca um usuário na base de dados pelo seu id.

        :param id: id do usuário a ser buscado.
        :return: dicionário com as informações do usuário encontrado, ou None se não encontrar.
        """

        cursor = self.__conexao.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario


class Usuario:
    """
    Classe que representa um usuário do sistema.
    """

    def __init__(self, nome, email, senha):
        """
        Inicializa um novo objeto usuário.

        :param nome: nome do usuário.
        :param email: e-mail do usuário.
        :param senha: senha do usuário.
        """

        self.__nome = nome
        self.__email = email
        self.__senha = senha

    def get_nome(self):
        """
        Retorna o nome do usuário.

        :return: nome do usuário.
        """

        return self.__nome

    def set_nome(self, nome):
        """
        Altera o nome do usuário.

        :param nome: novo nome do usuário.
        """

        self.__nome = nome

    def get_email(self):
        """
        Retorna o e-mail do usuário.

        :return: e-mail do usuário.
        """

        return self.__email

    def set_email(self, email):
        """
        Altera o e-mail do usuário.

        :param email: novo e-mail do usuário.
        """

        self.__email = email

    def get_senha(self):
        """
        Retorna a senha do usuário.

        :return: senha do usuário.
        """

        return self.__senha

class LoginWindow:
    """
    Classe responsável por criar a janela de login.

    Attributes
    ----------
    dao : UsuarioDAO
        Instância da classe UsuarioDAO que será utilizada para acessar os dados dos usuários.

    Methods
    -------
    abrir_janela_cadastro()
        Abre a janela de cadastro de usuários.

    login()
        Realiza o login do usuário ao verificar o email e a senha fornecidos pelo usuário na janela de login.
    """

    def __init__(self, dao):
        """
        Inicializa a janela de login.

        Parameters
        ----------
        dao : UsuarioDAO
            Instância da classe UsuarioDAO que será utilizada para acessar os dados dos usuários.
        """
        self.__dao = dao

        self.window = tk.Tk()
        self.window.title("Login")
        self.window.geometry("300x150")

        tk.Label(self.window, text="Email").grid(row=0)
        tk.Label(self.window, text="Senha").grid(row=1)

        self.email_entry = tk.Entry(self.window)
        self.email_entry.grid(row=0, column=1)

        self.senha_entry = tk.Entry(self.window, show="*")
        self.senha_entry.grid(row=1, column=1)

        tk.Button(self.window, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        tk.Button(self.window, text="Criar conta", command=self.abrir_janela_cadastro).grid(row=2, column=1, pady=10)

    def abrir_janela_cadastro(self):
        """
        Abre a janela de cadastro de usuários.
        """
        CadastroWindow(self.__dao)

    def login(self):
        """
        Realiza o login do usuário ao verificar o email e a senha fornecidos pelo usuário na janela de login.
        """
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        usuario = self.__dao.buscar_usuario_por_email(email)
        if usuario:
            if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha']):
                print("Login realizado com sucesso!")
            else:
                print("Senha incorreta!")
        else:
            print("Usuário não encontrado!")

class CadastroWindow:
    def __init__(self, dao):
        self.__dao = dao

        self.window = tk.Toplevel()
        self.window.title("Cadastro")
        self.window.geometry("300x150")

        tk.Label(self.window, text="Nome").grid(row=0)
        tk.Label(self.window, text="Email").grid(row=1)
        tk.Label(self.window, text="Senha").grid(row=2)

        self.nome_entry = tk.Entry(self.window)
        self.nome_entry.grid(row=0, column=1)

        self.email_entry = tk.Entry(self.window)
        self.email_entry.grid(row=1, column=1)

        self.senha_entry = tk.Entry(self.window, show="*")
        self.senha_entry.grid(row=2, column=1)

        tk.Button(self.window, text="Criar conta", command=self.criar_conta).grid(row=3, columnspan=2, pady=10)

    def criar_conta(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        self.__dao.criar_usuario(nome, email, senha)
        print("Conta criada com sucesso!")
        self.window.destroy()


if __name__ == '__main__':
    dao = UsuarioDAO()
    LoginWindow(dao)
    tk.mainloop()
