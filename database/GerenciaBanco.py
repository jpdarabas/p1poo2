# Criar dados dos meses anteriores com faker
from models import *
import sqlite3
from datetime import date

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
        self.nome_banco = "aluguel.db"
        self.__conexao = None
        self.__usuario: Usuario | None = None
        self.__imoveis: list[Imovel] = []
        self.__reservas: list[Reserva] = []

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

    ## USUÁRIOS ##

    # Getter
    def get_usuario(self):
        return self.__usuario

    # Cadastro Usuário
    def cadastrar_usuario(self, email, nome, tipo, senha):
        if not self.__conexao:
            self.conectar()
        
        self.__cursor.execute("INSERT INTO usuarios (email, nome, tipo, senha) VALUES (?, ?, ?, ?)", (email, nome, tipo, senha))
        self.__conexao.commit()

    # Login
    def login(self, email, senha):
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = self.__cursor.fetchone()
        if usuario:
            self.__usuario = Usuario(usuario["id"], usuario["email"], usuario["nome"], usuario["tipo"])
            return True
        return False
    
    ## IMÓVEIS ##

    # Get imovel por id
    def get_imovel_por_id(self, id:int):
        for imovel in self.__imoveis:
            if imovel.get_id() == id:
                return imovel
        return None

    # Filtrar imóveis
    def filtrar_imoveis(self, 
                        localizacao:str|None = None,
                        valor_minimo:float|None = None,
                        valor_maximo:float|None = None,
                        data_inicio:date|None = None,
                        data_fim:date|None = None,
                        locador_id:int|None = None,
                        ):
        imoveis = self.__imoveis.copy()
        if locador_id:
            imoveis = [imovel for imovel in imoveis if imovel.get_locador_id() == locador_id]
        if localizacao:
            imoveis = [imovel for imovel in imoveis if localizacao.lower() in imovel.get_endereco().lower()]
        if valor_minimo:
            imoveis = [imovel for imovel in imoveis if imovel.get_valor_diaria() >= valor_minimo]
        if valor_maximo:
            imoveis = [imovel for imovel in imoveis if imovel.get_valor_diaria() <= valor_maximo]
        if data_inicio and data_fim:
            imoveis = [imovel for imovel in imoveis if not True in (reserva.get_imovel_id() == imovel.get_id() and 
            reserva.get_data_inicio() <= data_fim and 
            reserva.get_data_fim() >= data_inicio for reserva in self.__reservas)]
        return imoveis

    # Carregar Imóveis
    def carregar_imoveis(self):
        if not self.__conexao:
            self.conectar()
        if self.__usuario.get_tipo() == "locador":
            self.__cursor.execute("SELECT * FROM imoveis WHERE locador_id = ?", (self.__usuario.get_id(),))
        else:
            self.__cursor.execute("SELECT * FROM imoveis")

        imoveis = self.__cursor.fetchall()
        for imovel in imoveis:
            self.__imoveis.append(Imovel(imovel["id"], imovel["titulo"], imovel["descricao"], imovel["endereco"], imovel["valor_diaria"], imovel["locador_id"]))
        return self.__imoveis

    # Cadastro Imóvel
    def cadastrar_imovel(self, titulo, descricao, endereco, valor_diaria):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        if self.__usuario.get_tipo() != "Locador":
            raise ValueError("Usuário não tem permissão para cadastrar imóveis.")
        locador_id = self.__usuario.get_id()

        imovel = Imovel(None, titulo, descricao, endereco, valor_diaria, locador_id)

        # Insere no banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("INSERT INTO imoveis (titulo, descricao, endereco, valor_diaria, locador_id) VALUES (?, ?, ?, ?, ?)", (titulo, descricao, endereco, valor_diaria, locador_id))
        self.__conexao.commit()

        # Atualiza o ID do imóvel após a inserção
        id = self.__cursor.lastrowid
        imovel.set_id(id)
        self.__imoveis.append(imovel)

    # Editar Imóvel
    def editar_imovel(self, id, titulo, descricao, endereco, valor_diaria):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        if self.__usuario.get_tipo() != "Locador":
            raise ValueError("Usuário não tem permissão para editar imóveis.")
        
        imovel = Imovel(id, titulo, descricao, endereco, valor_diaria, self.__usuario.get_id())

        # Atualiza o imóvel no banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("UPDATE imoveis SET titulo = ?, descricao = ?, endereco = ?, valor_diaria = ? WHERE id = ?", (titulo, descricao, endereco, valor_diaria, id))
        self.__conexao.commit()

        # Atualiza o imóvel na lista
        for i, imovel_antigo in enumerate(self.__imoveis):
            if imovel_antigo.get_id() == id:
                self.__imoveis[i] = imovel
                break

    # Remover Imóvel
    def remover_imovel(self, id):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        if self.__usuario.get_tipo() != "Locador":
            raise ValueError("Usuário não tem permissão para remover imóveis.")

        # Remove o imóvel do banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("DELETE FROM imoveis WHERE id = ?", (id,))
        self.__conexao.commit()

        # Remove o imóvel da lista
        for i, imovel in enumerate(self.__imoveis):
            if imovel.get_id() == id:
                del self.__imoveis[i]
                break

    ## RESERVAS ##

    # Listar Reservas
    def listar_reservas(self, locador_id:int|None = None, locatario_id:int|None = None):
        lista_reservas = self.__reservas.copy()
        if locatario_id:
            lista_reservas = [reserva for reserva in lista_reservas if reserva.get_locatario_id() == locatario_id]
        if locador_id:
            lista_reservas = [reserva for reserva in lista_reservas if reserva.get_imovel_id() in [imovel.get_id() for imovel in self.__imoveis if imovel.get_locador_id() == locador_id]]
        return lista_reservas

    # Carregar Reservas
    def carregar_reservas(self):
        if not self.__conexao:
            self.conectar()
        if self.__usuario.get_tipo() == "Locador":
            self.__cursor.execute("SELECT * FROM reservas r INNER JOIN imoveis i ON r.imovel_id = i.id WHERE i.locador_id = ?", (self.__usuario.get_id(),))
        else:
            self.__cursor.execute("SELECT * FROM reservas WHERE locatario_id = ?", (self.__usuario.get_id(),))

        reservas = self.__cursor.fetchall()
        for reserva in reservas:
            self.__reservas.append(Reserva(reserva["id"], self.str_pra_date(reserva["data_inicio"]), self.str_pra_date(reserva["data_fim"]), reserva["valor_total"], reserva["imovel_id"], reserva["locatario_id"], reserva["status"]))
        return self.__reservas

    # Cadastro Reserva
    def cadastrar_reserva(self, data_inicio, data_fim, valor_total, imovel_id, locatario_id):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        if self.__usuario.get_tipo() != "Locatário":
            raise ValueError("Usuário não tem permissão para cadastrar reservas.")

        # Verifica se o imóvel está disponível
        for reserva_antiga in self.__reservas:
            if reserva_antiga.get_imovel_id() == imovel_id and reserva_antiga.get_data_inicio() <= data_fim and reserva_antiga.get_data_fim() >= data_inicio:
                raise ValueError("Imóvel já reservado para essas datas.")
            
        status = "pendente"

        reserva = Reserva(None, data_inicio, data_fim, valor_total, imovel_id, locatario_id, status)

        # Insere no banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("INSERT INTO reservas (data_inicio, data_fim, valor_total, imovel_id, locatario_id, status) VALUES (?, ?, ?, ?, ?, ?)", (data_inicio, data_fim, valor_total, imovel_id, locatario_id, status))
        self.__conexao.commit()

        # Atualiza o ID da reserva após a inserção
        id = self.__cursor.lastrowid
        reserva.set_id(id)
        self.__reservas.append(reserva)

    # Editar Reserva
    def editar_reserva(self, id, data_inicio, data_fim, valor_total, imovel_id):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        if self.__usuario.get_tipo() != "Locatário":
            raise ValueError("Usuário não tem permissão para editar reservas.")

        reserva = Reserva(id, data_inicio, data_fim, valor_total, imovel_id, self.__usuario.get_id(), "pendente")

        # Atualiza a reserva no banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("UPDATE reservas SET data_inicio = ?, data_fim = ?, valor_total = ? WHERE id = ?", (data_inicio, data_fim, valor_total, id))
        self.__conexao.commit()

        # Atualiza a reserva na lista
        for i, reserva_antiga in enumerate(self.__reservas):
            if reserva_antiga.get_id() == id:
                self.__reservas[i] = reserva
                break

    def confirmar_reserva(self, id):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        if self.__usuario.get_tipo() != "Locador":
            raise ValueError("Usuário não tem permissão para confirmar reservas.")

        # Atualiza o status da reserva no banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("UPDATE reservas SET status = 'confirmada' WHERE id = ?", (id,))
        self.__conexao.commit()

        # Atualiza o status da reserva na lista
        for reserva in self.__reservas:
            if reserva.get_id() == id:
                reserva.set_status("confirmada")
                break

    # Remover Reserva
    def remover_reserva(self, id):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        
        # Remove a reserva do banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("DELETE FROM reservas WHERE id = ?", (id,))
        self.__conexao.commit()

        # Remove a reserva da lista
        for i, reserva in enumerate(self.__reservas):
            if reserva.get_id() == id:
                del self.__reservas[i]
                break


    ## AVALIAÇÕES ##

    # Listar A

    # Cadastro Avaliação
    def cadastrar_avaliacao(self, avaliacao:Avaliacao):
        if not self.__usuario:
            raise ValueError("Usuário não está logado.")
        if self.__usuario.get_tipo() != "Locatário":
            raise ValueError("Usuário não tem permissão para cadastrar avaliações.")

        nota = avaliacao.get_nota()
        comentario = avaliacao.get_comentario()
        imovel_id = avaliacao.get_imovel_id()

        # Insere no banco de dados
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("INSERT INTO avaliacoes (nota, comentario, imovel_id) VALUES (?, ?, ?)", (nota, comentario, imovel_id))
        self.__conexao.commit()

    # Listar avaliações de um imóvel
    def listar_avaliacoes_imovel(self, imovel_id):
        if not self.__conexao:
            self.conectar()
        self.__cursor.execute("SELECT * FROM avaliacoes WHERE imovel_id = ?", (imovel_id,))
        avaliacoes = self.__cursor.fetchall()
        lista_avaliacoes = []
        for avaliacao in avaliacoes:
            lista_avaliacoes.append(Avaliacao(avaliacao["id"], avaliacao["nota"], avaliacao["comentario"], avaliacao["imovel_id"]))
        return lista_avaliacoes


    # Útil:

    def date_pra_str(self, data):
        if isinstance(data, str):
            return data
        return data.strftime("%d/%m/%Y")
    
    def str_pra_date(self, data_str):
        if isinstance(data_str, date):
            return data_str
        if "-" in data_str:
            return date(*[int(i) for i in data_str.split("-")])
        if "/" in data_str:
            return date(*[int(i) for i in data_str.split("/")[::-1]])
        else:
            return None
    
    def str_pra_float(self, valor_str):
        try:
            return float(valor_str)
        except ValueError:
            return None
