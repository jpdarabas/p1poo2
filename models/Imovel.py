# título, descrição, endereço, valor da diária e disponibilidade

class Imovel:
    def __init__(self,
    id:int,
    titulo:str,
    descricao:str,
    endereco:str,
    valor_diaria:float,
    locador_id:int):
        if valor_diaria < 0:
            raise ValueError("Valor da diária não pode ser negativo.")
        self.__id = id
        self.__titulo = titulo
        self.__descricao = descricao
        self.__endereco = endereco
        self.__valor_diaria = valor_diaria
        self.__disponibilidade = disponibilidade
     
    # Getters

    def get_titulo(self):
        return self.__titulo
    def get_descricao(self):
        return self.__descricao

    def get_endereco(self):
        return self.__endereco

    def get_valor_diaria(self):
        return self.__valor_diaria

    def get_disponibilidade(self):
        return self.__disponibilidade

    # Setters

    def set_titulo(self, titulo):
        self.__titulo = titulo

    def set_descricao(self, descricao):
        self.__descricao = descricao

    def set_endereco(self, endereco):
        self.__endereco = endereco

    def set_valor_diaria(self, valor_diaria):
        if valor_diaria < 0:
            raise ValueError("Valor da diária não pode ser negativo.")
        self.__valor_diaria = valor_diaria

    def set_disponibilidade(self, disponibilidade):
        if disponibilidade not in (True, False):
            raise ValueError("Disponibilidade deve ser True ou False.")
        self.__disponibilidade = disponibilidade
    