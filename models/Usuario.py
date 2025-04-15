 from datetime import date

 class Usuario():
    def __init__(self, 
    email:str,
    nome:str,
    tipo:str
    ):
        if "@" not in email:
            pass 
        if tipo not in ("locador", "locatário"):
            pass
        self.__email = email
        self.__nome = nome
        self.__tipo = tipo

        # Getters

        # Setters