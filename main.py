from PyQt6.QtWidgets import QApplication
import sys

from database import GerenciaBanco
from interface import NavigationController

class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.banco = GerenciaBanco()
        
        try:
            self.banco.conectar()
            self.banco.criar_tabelas()
            
            # Cria o navigator com as páginas pré-registradas
            self.navigator = NavigationController()
            
            # Navega para a tela inicial
            self.navigator.navigate_to("TelaLogin")
            self.navigator.show()  # Mostra a janela principal
            
            sys.exit(self.app.exec())  # inicia o loop da aplicação
        finally:
            self.banco.desconectar()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    main_app = Main()
    main_app.run()