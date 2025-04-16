from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QFormLayout, QComboBox)
from PyQt6.QtCore import Qt
from database import GerenciaBanco

class TelaCadastro(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.setup_ui()
        self.db = GerenciaBanco()
        
    def setup_ui(self):
        self.setWindowTitle("Cadastro")
        self.setFixedSize(400, 400)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Nome
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Seu nome completo")
        
        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email")
        
        # Tipo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Locador", "Locatário"])
        
        # Senha
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Crie uma senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password) 
        
        # Botões
        self.cadastrar_btn = QPushButton("Cadastrar")
        self.cadastrar_btn.clicked.connect(self.fazer_cadastro)
        
        self.voltar_btn = QPushButton("Cancelar")
        self.voltar_btn.clicked.connect(self.navigator.go_back)
        
        # Adicionando ao layout
        form_layout.addRow("Nome:", self.nome_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Tipo:", self.tipo_combo)
        form_layout.addRow("Senha:", self.senha_input)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.cadastrar_btn)
        layout.addWidget(self.voltar_btn)
        
        self.setLayout(layout)
    
    def fazer_cadastro(self):
        nome = self.nome_input.text()
        email = self.email_input.text()
        tipo = self.tipo_combo.currentText()
        senha = self.senha_input.text()
        
        if not all([nome, email, senha]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        
        try:
            self.db.cadastrar_usuario(email, nome, tipo, senha)
            QMessageBox.information(self, "Sucesso", "Cadastro realizado com sucesso!")
            self.navigator.navigate_to('TelaLogin')  # Navega para a tela de login
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"{e}")
        return