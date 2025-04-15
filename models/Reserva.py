from datetime import date
class Reserva:
    def __init__(self,
    id:int,
    data_inicio:date,
    data_fim:date,
    valor_total:float,
    imovel_id:int,
    locatario_id:int,
    status:str
    ):
        if status not in ("pendente", "confirmada", "cancelada"):
            raise ValueError("Status inválido.")
        self.__id = id
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.__valor_total = valor_total
        self.__imovel_id = imovel_id
        self.__locatario_id = locatario_id
        self.__status = status

    # Getters
    def get_id(self):
        return self.__id

    def get_data_inicio(self):
        return self.__data_inicio

    def get_data_fim(self):
        return self.__data_fim

    def get_valor_total(self):
        return self.__valor_total

    def get_imovel_id(self):
        return self.__imovel_id

    def get_locatario_id(self):
        return self.__locatario_id

    def get_status(self):
        return self.__status

    # Setters
    def set_data_inicio(self, data_inicio):
        self.__data_inicio = data_inicio

    def set_data_fim(self, data_fim):
        self.__data_fim = data_fim

    def set_valor_total(self, valor_total):
        self.__valor_total = valor_total

    