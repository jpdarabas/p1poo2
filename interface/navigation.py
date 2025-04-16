from PyQt6.QtWidgets import QStackedWidget
from interface import *
from .styles import styles

class NavigationController(QStackedWidget):
    def __init__(self):
        super().__init__()
        self._paginas_criadas = {}  # Dicionário para armazenar páginas
        self._historico = []  # Histórico de navegação
        self._paginas = {
            "TelaLogin": TelaLogin,
            "TelaCadastro": TelaCadastro,
            "TelaPrincipal": TelaPrincipal
        }

        self.setStyleSheet(styles)
        self.setWindowTitle("Aluguel de Imóveis")

    def registrar_pagina(self, page_name, page_class):
        """Registra uma classe de página manualmente"""
        self._paginas[page_name] = page_class

    def navigate_to(self, page_name, refresh=False, **kwargs):
        """Navega para uma página, recriando-a se refresh=True"""
        # Se estiver no histórico e for refresh, remove última entrada do histórico
        if refresh and self._historico and self._historico[-1] == page_name:
            self._historico.pop()

        # Se a tela já existe e for refresh, remova-a completamente
        if refresh and page_name in self._paginas_criadas:
            old_widget = self._paginas_criadas.pop(page_name)
            self.removeWidget(old_widget)
            old_widget.deleteLater()

        # Cria a página se ainda não foi criada
        if page_name not in self._paginas_criadas:
            page = self._paginas[page_name](self, **kwargs)
            self._paginas_criadas[page_name] = page
            self.addWidget(page)
        else:
            page = self._paginas_criadas[page_name]

        # Mostra a tela e atualiza histórico
        self.setCurrentWidget(page)
        self._historico.append(page_name)

        # Chama on_navigate_to se existir
        if hasattr(page, 'on_navigate_to'):
            page.on_navigate_to(**kwargs)

        return page

    def go_back(self):
        """Volta para a página anterior"""
        if len(self._historico) > 1:
            self._historico.pop()
            self.navigate_to(self._historico[-1])

    def reset_app(self):
        """Remove todas as páginas criadas e volta para a tela inicial"""
        for widget in self._paginas_criadas.values():
            self.removeWidget(widget)
            widget.deleteLater()
        self._paginas_criadas.clear()
        self._historico.clear()

        # Recomeça pela tela de login
        self.navigate_to("TelaLogin", refresh=True)
