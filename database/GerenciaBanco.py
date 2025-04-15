# Criar dados dos meses anteriores com faker
from models import *
import sqlite3

class GerenciaBanco():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GerenciaBanco, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._inicializado = True
        self.nome_banco = "reservas.db"
        self.__conexao = None
        self.__usuario = None

    def conectar(self):
        self.__conexao = sqlite3.connect(self.nome_banco)
        self.__conexao.row_factory = sqlite3.Row
        self.__cursor = self.__conexao.cursor()
        self.__conexao.execute("PRAGMA foreign_keys = ON")

    def desconectar(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__conexao:
            self.__conexao.close()

    def criar_tabelas(self):
        if not self.__conexao:
            self.conectar()

        arquivos_sql = ["database/avaliacoes.sql", "database/imoveis.sql", "database/reservas.sql", "database/usuarios.sql"]
        
        for arquivo in arquivos_sql:
            with open(arquivo, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            self.__cursor.execute(sql_script)
        
        self.__conexao.commit()

    def carregar_dados(self):
        if not self.__conexao:
            self.conectar()

    def cadastrar_usuario(self, email, nome, tipo, senha):
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("INSERT INTO usuario (email, nome, tipo, senha) VALUES (?, ?, ?, ?)", (email, nome, tipo, senha))
        self.__conexao.commit()

    def login(self, email, senha):
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("SELECT * FROM usuario WHERE email = ? AND senha = ?", (email, senha))
        usuario = self.__cursor.fetchone()
        if usuario:
            self.__usuario = Usuario(usuario["id"], usuario["email"], usuario["nome"], usuario["tipo"])
            self.__usuario = usuario
            return True
        return False
