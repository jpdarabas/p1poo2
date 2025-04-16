class Avaliacao:
   def __init__(self,
   id:int,
   nota:int,
   comentario:str,
   imovel_id:int
   ):
      if nota not in range(1, 6):
            raise ValueError("Nota deve ser entre 1 e 5.")
      self.__id = id
      self.__nota = nota
      self.__comentario = comentario
      self.__imovel_id = imovel_id

   # Getters

   def get_id(self):
      return self.__id
   
   def get_nota(self):
      return self.__nota
   
   def get_comentario(self):
      return self.__comentario
   
   def get_imovel_id(self):
      return self.__imovel_id
   
   # Setters

   def set_id(self, id):
      self.__id = id

   def set_nota(self, nota):
      if nota not in range(1, 6):
         raise ValueError("Nota deve ser entre 1 e 5.")
      self.__nota = nota

   def set_comentario(self, comentario):
      self.__comentario = comentario

   def set_imovel_id(self, imovel_id):
      self.__imovel_id = imovel_id