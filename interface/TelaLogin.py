from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from database import GerenciaBanco

class TelaLogin(QWidget):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.setup_ui()
        self.db = GerenciaBanco()
        
    def setup_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Campos de entrada
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email")
        
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Digite sua senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)  # Corrigido para PyQt6
        
        # Botões
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.fazer_login)
        
        self.cadastrar_btn = QPushButton("Cadastrar")
        self.cadastrar_btn.clicked.connect(self.ir_para_cadastro)
        
        # Adicionando ao layout
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Senha:", self.senha_input)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.cadastrar_btn)
        
        self.setLayout(layout)
    
    def fazer_login(self):
        email = self.email_input.text()
        senha = self.senha_input.text()
        
        if not email or not senha:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
         
        sucesso_login = self.db.login(email, senha)
        if sucesso_login:
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
            self.navigator.navigate_to('TelaPrincipal', refresh=True)
        else:
            QMessageBox.warning(self, "Erro", "Email ou senha incorretos!")
            return
    
    def ir_para_cadastro(self):
        self.navigator.navigate_to('TelaCadastro')