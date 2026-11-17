import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QDoubleSpinBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)

from produtos import salvar_produto, listar_produtos


class TelaCadastro(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Protudos")
        self.resize(800, 450)

        self.campo_codigo = QLineEdit()
        self.campo_nome = QLineEdit()

        self.campo_preco_venda = QDoubleSpinBox()
        self.campo_preco_venda.setDecimals(2)
        self.campo_preco_venda.setMaximum(99999)
        self.campo_preco_venda.setPrefix("R$ ")

        self.campo_preco_custo = QDoubleSpinBox()
        self.campo_preco_custo.setDecimals(2)
        self.campo_preco_custo.setMaximum(99999)
        self.campo_preco_custo.setPrefix("R$ ")

        self.campo_estoque = QSpinBox()
        self.campo_estoque.setMaximum(99999)

        formulario = QFormLayout()
        formulario.addRow("Código de barras:", self.campo_codigo),
        formulario.addRow("Nome:", self.campo_nome),
        formulario.addRow("Preço de venda:", self.campo_preco_venda),
        formulario.addRow("Preço de custo:", self.campo_preco_custo),
        formulario.addRow("Estoque Atual:", self.campo_estoque),
        formulario.addRow("Estoque mínimo:", self.campo_minimo)

        self.botao_salvar = QPushButton ("Salvar")
        self.botao_salvar.clicked.connect(self.salvar)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Código", "Produto", "Preço", "Estoque", "Mínimo"]
        )
        

