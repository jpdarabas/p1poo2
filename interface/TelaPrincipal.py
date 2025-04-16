from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt
from database import GerenciaBanco
from functools import partial 
from models import *
from .componentes import *
from .styles import styles
from datetime import date

class TelaPrincipal(QWidget):
    recarregar_ui = pyqtSignal()  # Sinal para recarregar toda a tela

    def __init__(self, navigator):
        super().__init__()
        self._navigator = navigator
        self._db = GerenciaBanco()
        self._widget_primario = None
        self._widget_secundario = None
        self.setStyleSheet(styles)
        self.tipo = self._db.get_usuario().get_tipo()
        
        self.filtro_localizacao = None
        self.filtro_valor_minimo = None
        self.filtro_valor_maximo = None
        self.filtro_data_inicio = None
        self.filtro_data_fim = None

        self._db.carregar_imoveis()
        self._db.carregar_reservas()
        
        self.init_ui()
        self.carregar_widgets()
        self.recarregar_ui.connect(self.reload_ui)


    def init_ui(self):
        """Configuração básica da UI com scroll"""
        self.setMinimumSize(800, 600)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Área de scroll
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        
        # Container do conteúdo (dentro do scroll)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)
        
        # Stacked widget para alternar entre views
        self.stacked_widgets = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widgets)
        
        
        
        # Cabeçalho (barra de navegação)
        header = QHBoxLayout()

        # Botões de navegação
        botoes = ["Imóveis", "Reservas"]
        
        self.botoes_header = []
        for i, texto in enumerate(botoes):
            btn = QPushButton(texto)
            btn.clicked.connect(partial(self.mostrar_widget, i))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            header.addWidget(btn)
            self.botoes_header.append(btn)
        
        self.main_layout.addLayout(header)
        self.main_layout.addWidget(self.scroll)
        
        self.scroll.setWidget(self.content_widget)

    def carregar_widgets(self):
        """Cria os widgets principais vazios"""
        # Widget Primário (ex: lista de itens)
        self._widget_primario = QWidget()
        layout_primario = QVBoxLayout(self._widget_primario)
        layout_primario.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Adicionar imovel
        locador_id = None
        if self.tipo == "Locador":
            adicionar_imovel = QPushButton("Adicionar Imóvel")
            adicionar_imovel.clicked.connect(self.editarObjeto)
            adicionar_imovel.setCursor(Qt.CursorShape.PointingHandCursor)
            layout_primario.addWidget(adicionar_imovel)
            layout_primario.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            locador_id = self._db.get_usuario().get_id()
        else:
            filtros = QHBoxLayout()

            edit_localizacao = QLineEdit(self.filtro_localizacao)
            edit_localizacao.setPlaceholderText("Localização")
            edit_localizacao.textChanged.connect(lambda text=edit_localizacao.text(): setattr(self, 'filtro_localizacao', text))

            edit_valor_minimo = QLineEdit(self.filtro_valor_minimo)
            edit_valor_minimo.setPlaceholderText("Valor mínimo")
            edit_valor_minimo.textChanged.connect(lambda text=edit_valor_minimo.text(): setattr(self, 'filtro_valor_minimo', text))

            edit_valor_maximo = QLineEdit(self.filtro_valor_maximo)
            edit_valor_maximo.setPlaceholderText("Valor máximo")
            edit_valor_maximo.textChanged.connect(lambda text=edit_valor_maximo.text(): setattr(self, 'filtro_valor_maximo', text))

            edit_data_inicio = QLineEdit(self.filtro_data_inicio)
            edit_data_inicio.setPlaceholderText("Data início (dd/mm/yyyy)")
            edit_data_inicio.textChanged.connect(lambda text=edit_data_inicio.text(): setattr(self, 'filtro_data_inicio', text))

            edit_data_fim = QLineEdit(self.filtro_data_fim)
            edit_data_fim.setPlaceholderText("Data fim (dd/mm/yyyy)")
            edit_data_fim.textChanged.connect(lambda text=edit_data_fim.text(): setattr(self, 'filtro_data_fim', text))

            filtros.addWidget(edit_localizacao)
            filtros.addWidget(edit_valor_minimo)
            filtros.addWidget(edit_valor_maximo)
            filtros.addWidget(edit_data_inicio)
            filtros.addWidget(edit_data_fim)
            layout_primario.addLayout(filtros)

            botao_filtrar = QPushButton("Filtrar")
            botao_filtrar.clicked.connect(lambda: self.reload_ui())
            botao_filtrar.setCursor(Qt.CursorShape.PointingHandCursor)
            layout_primario.addWidget(botao_filtrar)



        # Lista imóveis
        for imovel in self._db.filtrar_imoveis(
            localizacao=edit_localizacao.text() if self.tipo == "Locatário" else None,
            valor_minimo=self._db.str_pra_float(edit_valor_minimo.text()) if self.tipo == "Locatário" else None,
            valor_maximo=self._db.str_pra_float(edit_valor_maximo.text()) if self.tipo == "Locatário" else None,
            data_inicio=self._db.str_pra_date(edit_data_inicio.text()) if self.tipo == "Locatário" else None,
            data_fim=self._db.str_pra_date(edit_data_fim.text()) if self.tipo == "Locatário" else None,
            locador_id=locador_id):
            item_layout = QHBoxLayout()
            item_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            
            # Informações do imóvel	
            texto = f"Título: {imovel.get_titulo()}\n\
Descrição: {imovel.get_descricao()}\n\
Endereço: {imovel.get_endereco()}\n\
Valor diária: {imovel.get_valor_diaria()}\n"
            label = QLabel(texto)
            item_layout.addWidget(label)

            # Avaliações do imóvel
            botao_avaliacoes = QPushButton("Avaliações")
            botao_avaliacoes.clicked.connect(lambda _, i=imovel: self.mostrar_avaliacoes(i))
            botao_avaliacoes.setCursor(Qt.CursorShape.PointingHandCursor)
            item_layout.addWidget(botao_avaliacoes)

            if self.tipo == "Locador":
                # Editar
                botao_editar = QPushButton("Editar")
                botao_editar.clicked.connect(lambda _, i=imovel: self.editarObjeto(i))
                botao_editar.setCursor(Qt.CursorShape.PointingHandCursor)
                item_layout.addWidget(botao_editar)

                # Remover
                botao_remover = QPushButton("Remover")
                botao_remover.clicked.connect(lambda _, i=imovel: self.remover_imovel(i))
                botao_remover.setCursor(Qt.CursorShape.PointingHandCursor)
                item_layout.addWidget(botao_remover)
            else:
                # Reservar
                botao_reservar = QPushButton("Reservar")
                botao_reservar.clicked.connect(lambda _, i=imovel: self.editarObjeto(i))
                botao_reservar.setCursor(Qt.CursorShape.PointingHandCursor)
                item_layout.addWidget(botao_reservar)
            layout_primario.addLayout(item_layout)

        
        # Widget Secundário (ex: detalhes)
        self._widget_secundario = QWidget()
        layout_secundario = QVBoxLayout(self._widget_secundario)
        layout_secundario.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        locatario_id = None
        if self.tipo == "Locatário":
            locatario_id = self._db.get_usuario().get_id()

        # Lista reservas
        for reserva in self._db.listar_reservas(
            locatario_id=locatario_id,
            locador_id=locador_id
        ):
            item_layout = QHBoxLayout()
            item_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            
            # Informações do imóvel
            imovel = self._db.get_imovel_por_id(reserva.get_imovel_id())

            texto = f"Imóvel: {imovel.get_titulo()}\n\
Data início: {self._db.date_pra_str(reserva.get_data_inicio())}\n\
Data fim: {self._db.date_pra_str(reserva.get_data_fim())}\n\
Valor total: {reserva.get_valor_total()}\n\
Status: {reserva.get_status()}\n"
            label = QLabel(texto)
            item_layout.addWidget(label)

            if self.tipo == "Locatário":
                if reserva.get_status() == "pendente":
                    # Editar
                    botao_editar = QPushButton("Editar")
                    botao_editar.clicked.connect(lambda _, i=imovel, r=reserva: self.editarObjeto(i, r))
                    botao_editar.setCursor(Qt.CursorShape.PointingHandCursor)
                    item_layout.addWidget(botao_editar)
                else:
                    # Avaliar
                    if reserva.get_data_fim() < date.today():
                        botao_avaliar = QPushButton("Avaliar")
                        botao_avaliar.clicked.connect(lambda _, r=reserva: self.avaliar_reserva(r))
                        botao_avaliar.setCursor(Qt.CursorShape.PointingHandCursor)
                        item_layout.addWidget(botao_avaliar)

            else:
                if reserva.get_status() == "pendente":
                    # Confirmar
                    botao_confirmar = QPushButton("Confirmar")
                    botao_confirmar.clicked.connect(lambda _, r=reserva: self.confirmar_reserva(r))
                    botao_confirmar.setCursor(Qt.CursorShape.PointingHandCursor)
                    item_layout.addWidget(botao_confirmar)

            if reserva.get_status() == "pendente":
                # Cancelar/Remover
                botao_remover = QPushButton("Cancelar" if self.tipo == "Locatário" else "Remover")
                botao_remover.clicked.connect(lambda _, r=reserva: self.cancelar_reserva(r))
                botao_remover.setCursor(Qt.CursorShape.PointingHandCursor)
                item_layout.addWidget(botao_remover)

            layout_secundario.addLayout(item_layout)
        
        # Adiciona ao stacked widget
        self.stacked_widgets.addWidget(self._widget_primario)
        self.stacked_widgets.addWidget(self._widget_secundario)
        
        # Mostra o primeiro widget por padrão
        self.mostrar_widget(0)

    def mostrar_widget(self, indice):
        """Alterna entre os widgets principais
        Args:
            indice: 0 para primário, 1 para secundário
        """
        if 0 <= indice < self.stacked_widgets.count():
            self.stacked_widgets.setCurrentIndex(indice)

    def reload_ui(self):
        """Recarrega completamente a interface"""
        # Salva o estado atual
        indice_atual = self.stacked_widgets.currentIndex()
        
        # Limpa tudo
        for i in reversed(range(self.stacked_widgets.count())):
            widget = self.stacked_widgets.widget(i)
            self.stacked_widgets.removeWidget(widget)
            widget.deleteLater()
        
        # Recria os widgets
        self.carregar_widgets()
        
        # Restaura o estado
        if 0 <= indice_atual < self.stacked_widgets.count():
            self.mostrar_widget(indice_atual)

    def editarObjeto(self, imovel:Imovel|None = None, reserva:Reserva|None = None):
        try:
            if self._db.get_usuario().get_tipo() == "Locador":
                tipo_objeto = "Imovel"
            else:
                tipo_objeto = "Reserva"
            modal = ModalEditar(imovel, reserva, tipo_objeto, self)
            if modal.exec() == QDialog.DialogCode.Accepted:
                if tipo_objeto == "Imovel":
                    if imovel:
                        titulo, descricao, endereco, valor_diaria = modal.get_dados_editados()

                        self._db.editar_imovel(imovel.get_id(), 
                                            titulo, 
                                            descricao, 
                                            endereco, 
                                            valor_diaria)
                    else:
                        titulo, descricao, endereco, valor_diaria = modal.get_dados_editados()
                        self._db.cadastrar_imovel(titulo, 
                                                descricao, 
                                                endereco, 
                                                valor_diaria)
                else:
                    if reserva:
                        data_inicio, data_fim, valor_total = modal.get_dados_editados()
                        data_inicio = self._db.str_pra_date(data_inicio)
                        data_fim = self._db.str_pra_date(data_fim)
                        self._db.editar_reserva(reserva.get_id(), 
                                            data_inicio, 
                                            data_fim, 
                                            valor_total, 
                                            imovel.get_id())
                    else:
                        data_inicio, data_fim, valor_total = modal.get_dados_editados()
                        data_inicio = self._db.str_pra_date(data_inicio)
                        data_fim = self._db.str_pra_date(data_fim)
                        self._db.cadastrar_reserva(data_inicio, 
                                                data_fim, 
                                                valor_total, 
                                                imovel.get_id(), 
                                                self._db.get_usuario().get_id())
        except ValueError as e:
            QMessageBox.critical(self, "Erro", str(e))
            return
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            return
        self.recarregar_ui.emit()

    def avaliar_reserva(self, reserva:Reserva):
        try:
            modal = QDialog()
            modal.setWindowTitle("Avaliar Reserva")
            layout = QVBoxLayout(modal)
            form = QFormLayout()

            nota = QLineEdit()
            nota.setPlaceholderText("Nota (0 a 5)")
            comentario = QLineEdit()
            comentario.setPlaceholderText("Comentário")
            form.addRow("Nota:", nota)
            form.addRow("Comentário:", comentario)
            layout.addLayout(form)

            botao_ok = QPushButton("OK")
            botao_ok.clicked.connect(modal.accept)
            botao_cancelar = QPushButton("Cancelar")
            botao_cancelar.clicked.connect(modal.reject)
            layout.addWidget(botao_ok)
            layout.addWidget(botao_cancelar)

            if modal.exec() == QDialog.DialogCode.Accepted:
                avaliacao = Avaliacao(None, int(nota.text()), comentario.text(), reserva.get_imovel_id())
                self._db.cadastrar_avaliacao(avaliacao)
                self._db.remover_reserva(reserva.get_id())
                self.recarregar_ui.emit()

        except ValueError as e:
            QMessageBox.critical(self, "Erro", str(e))
            return
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def cancelar_reserva(self, reserva:Reserva):
        id = reserva.get_id()
        self._db.remover_reserva(id)
        self.recarregar_ui.emit()

    def remover_imovel(self, imovel:Imovel):
        id = imovel.get_id()
        self._db.remover_imovel(id)
        self.recarregar_ui.emit()
    
    def confirmar_reserva(self, reserva:Reserva):
        id = reserva.get_id()
        self._db.confirmar_reserva(id)
        self.recarregar_ui.emit()

    def mostrar_avaliacoes(self, imovel:Imovel):
        try:
            modal = QDialog()
            modal.setWindowTitle("Avaliações")
            layout = QVBoxLayout(modal)
            avaliacoes = self._db.listar_avaliacoes_imovel(imovel.get_id())
            nota_media = sum([a.get_nota() for a in avaliacoes]) / len(avaliacoes) if avaliacoes else "Sem avaliações"
            nota_media_label = QLabel(f"Média: {nota_media}")
            layout.addWidget(nota_media_label)
            # Lista de avaliações
            for avaliacao in avaliacoes:
                texto = f"Nota: {avaliacao.get_nota()}\n\
Comentario: {avaliacao.get_comentario()}"
                label = QLabel(texto)
                layout.addWidget(label)
            modal.setLayout(layout)
            modal.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
            return
        self.recarregar_ui.emit()