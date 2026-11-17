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

        esquerda = QVBoxLayout()
        esquerda.addLayout(formulario)
        esquerda.addWidget(self.botao_salvar)
        esquerda.addStretch()

        principal = QHBoxLayout(self)
        principal.addLayout(esquerda, 1)
        principal.addWidget(self.tabela, 2)

        self.campo_codigo.setFocus()
        self.carregar_tabela()

def salvar(self):
    codigo = self.campo_codigo.txt().strip()
    nome = self.campo_nome.txt().strip()
    preco_venda = round(self.campo_preco_venda.values() * 100)
    preco_custo = round(self.campo_preco_custo.value() * 100)

    if not codigo or not nome:
        QMessageBox.warning(self, "Atenção", "Código e nome são obrigatórios.")
        return
    if preco_venda <= 0:
        QMessageBox.warning(self, "Atenção", "O preço de venda deve ser maior que zero.")
        return
    
    try:
        salvar_produto(codigo, nome, preco_venda, preco_custo, self.campo_estoque.value(), self.campo_minimo.value())
    except Exception as erro:
        QMessageBox.critical(self, "Erro", f"Falha ao salvar produto: {erro}")
        return

    self.limpar_campos()
    self.carregar_tabela()

    def limpar_campos(self):
        self.campo_codigo.clear()
        self.campo_nome.clear()
        self.campo_preco_venda.setValue(0)
        self.campo_preco_custo.setValue(0)
        self.campo_estoque.setValue(0)
        self.campo_minimo.setValue(0)
        self.campo_codigo.setFocus()

    def carregar_tabela(self):
        produtos = listar_produtos()
        self.tabela.setRowCount(len(produtos))



