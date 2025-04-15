 from datetime import date

 class Usuario():
    def __init__(self, 
    id:int,
    email:str,
    nome:str,
    tipo:str
    ):
        if "@" not in email:
            pass 
        if tipo not in ("locador", "locatário"):
            pass
        self.__id = id
        self.__email = email
        self.__nome = nome
        self.__tipo = tipo

        # Getters
        
        def get_id(self):
            return self.__id

        def get_email(self):
            return self.__email

        def get_nome(self):
            return self.__nome

        def get_tipo(self):
            return self.__tipo

        # Setters

        def set_email(self, email):
            if "@" not in email:
                pass
            self.__email = email
        def set_nome(self, nome):
            self.__nome = nome
        def set_tipo(self, tipo):
            if tipo not in ("locador", "locatário"):
                pass
            self.__tipo = tipo
            