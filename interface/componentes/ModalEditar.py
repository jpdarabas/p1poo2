from PyQt6.QtWidgets import *
from models import *
from datetime import date
from database import GerenciaBanco

class ModalEditar(QDialog):
    def __init__(self, imovel:Imovel|None, reserva:Reserva|None,tipo_objeto:str, parent = None):
        super().__init__(parent)
        self.imovel = imovel
        self.reserva = reserva
        self.tipo_objeto = tipo_objeto
        self._db = GerenciaBanco()

        layout = QVBoxLayout(self)
        form = QFormLayout()
        if tipo_objeto == "Reserva":
            if reserva:
                self.setWindowTitle(f"Editar {tipo_objeto}")
                data_inicio, data_fim = reserva.get_data_inicio(), reserva.get_data_fim()
            else:
                self.setWindowTitle(f"Adicionar {tipo_objeto}")
                data_inicio, data_fim = date.today(), date.today()
            
            data_inicio, data_fim = self._db.date_pra_str(data_inicio), self._db.date_pra_str(data_fim)

            self.titulo = QLabel(imovel.get_titulo())
            self.valor_diaria = QLabel(f"R$ {imovel.get_valor_diaria()}")
            self.data_inicio_edit = QLineEdit(data_inicio)
            self.data_inicio_edit.textChanged.connect(self.calcula_valor_total)
            self.data_fim_edit = QLineEdit(data_fim)
            self.data_fim_edit.textChanged.connect(self.calcula_valor_total)
            self.valor_total_label = QLabel()
            self.calcula_valor_total()


            form.addRow("Imóvel:", self.titulo)
            form.addRow("Valor diária:", self.valor_diaria)
            form.addRow("Início aluguel (dd/mm/yyyy):", self.data_inicio_edit)
            form.addRow("Fim do aluguel (dd/mm/yyyy):", self.data_fim_edit)
            form.addRow("Valor total:", self.valor_total_label)
        else:
            if imovel:
                self.setWindowTitle(f"Editar {tipo_objeto}")
                titulo, descricao, endereco, valor_diaria = imovel.get_titulo(), imovel.get_descricao(), imovel.get_endereco(), imovel.get_valor_diaria()
            else:
                self.setWindowTitle(f"Adicionar {tipo_objeto}")
                titulo, descricao, endereco, valor_diaria = "", "", "", 0.0
            
            self.titulo_edit = QLineEdit(titulo)
            self.descricao_edit = QLineEdit(descricao)
            self.endereco_edit = QLineEdit(endereco)
            self.valor_edit = QLineEdit(str(valor_diaria))

            form.addRow("Título:", self.titulo_edit)
            form.addRow("Descrição:", self.descricao_edit)
            form.addRow("Endereço:", self.endereco_edit)
            form.addRow("Valor diária:", self.valor_edit)

        layout.addLayout(form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def get_dados_editados(self):
        if self.tipo_objeto == "Reserva":
            return self.data_inicio_edit.text(), self.data_fim_edit.text(), self.calcula_valor_total()
        else:
            return self.titulo_edit.text(), self.descricao_edit.text(), self.endereco_edit.text(), float(self.valor_edit.text())
    
    def calcula_valor_total(self):
        try:
            data_inicio = self._db.str_pra_date(self.data_inicio_edit.text())
            data_fim = self._db.str_pra_date(self.data_fim_edit.text())
            dias = (data_fim - data_inicio).days + 1
            valor_total = dias * self.imovel.get_valor_diaria()

        except Exception as e:
            valor_total = 0.0

        self.valor_total_label.setText(f"R$ {valor_total:.2f}")
        return valor_total
