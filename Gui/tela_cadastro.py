import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QDoubleSpinBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView
)

from produtos import (
    salvar_produto, listar_produtos, buscar_produto_por_id,
    atualizar_produto, inativar_produto
)


class TelaCadastro(QWidget):
    def __init__(self):
        super().__init__()
        self.produto_em_edicao = None
        self.setWindowTitle("Cadastro de Produtos")
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

        self.campo_minimo = QSpinBox()
        self.campo_minimo.setMaximum(99999)

        formulario = QFormLayout()
        formulario.addRow("Código de barras:", self.campo_codigo)
        formulario.addRow("Nome:", self.campo_nome)
        formulario.addRow("Preço de venda:", self.campo_preco_venda)
        formulario.addRow("Preço de custo:", self.campo_preco_custo)
        formulario.addRow("Estoque atual:", self.campo_estoque)
        formulario.addRow("Estoque mínimo:", self.campo_minimo)

        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar.clicked.connect(self.salvar)
        self.botao_novo = QPushButton("Novo")
        self.botao_novo.clicked.connect(self.limpar_campos)
        self.botao_inativar = QPushButton("Inativar")
        self.botao_inativar.clicked.connect(self.inativar)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Código", "Produto", "Preço", "Estoque", "Mínimo"]
        )
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela.cellDoubleClicked.connect(self.carregar_produto_para_edicao)

        esquerda = QVBoxLayout()
        esquerda.addLayout(formulario)
        esquerda.addWidget(self.botao_salvar)
        esquerda.addWidget(self.botao_novo)
        esquerda.addWidget(self.botao_inativar)
        esquerda.addStretch()

        principal = QHBoxLayout(self)
        principal.addLayout(esquerda, 1)
        principal.addWidget(self.tabela, 2)

        self.campo_codigo.setFocus()
        self.carregar_tabela()

    def salvar(self):
        codigo = self.campo_codigo.text().strip()
        nome = self.campo_nome.text().strip()
        preco_venda = round(self.campo_preco_venda.value() * 100)
        preco_custo = round(self.campo_preco_custo.value() * 100)

        if not codigo or not nome:
            QMessageBox.warning(self, "Atenção", "Código e nome são obrigatórios.")
            return
        if preco_venda <= 0:
            QMessageBox.warning(self, "Atenção", "O preço de venda deve ser maior que zero.")
            return

        try:
            if self.produto_em_edicao is None:
                salvar_produto(codigo, nome, preco_venda, preco_custo,
                               self.campo_estoque.value(), self.campo_minimo.value())
            else:
                atualizar_produto(self.produto_em_edicao, codigo, nome, preco_venda,
                                  preco_custo, self.campo_estoque.value(),
                                  self.campo_minimo.value())
        except Exception as erro:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar produto: {erro}")
            return

        self.limpar_campos()
        self.carregar_tabela()

    def limpar_campos(self):
        self.produto_em_edicao = None
        self.botao_salvar.setText("Salvar")
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
        for linha, (id_, codigo, nome, preco, estoque, minimo) in enumerate(produtos):
            valores = [id_, codigo, nome,
                       f"R$ {preco / 100:.2f}".replace(".", ","),
                       estoque, minimo]
            for coluna, valor in enumerate(valores):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carregar_produto_para_edicao(self, linha, coluna):
        produto_id = int(self.tabela.item(linha, 0).text())
        produto = buscar_produto_por_id(produto_id)
        if produto is None:
            return

        (id_, codigo, nome, preco_venda, preco_custo,
         estoque_atual, estoque_minimo) = produto

        self.produto_em_edicao = id_
        self.campo_codigo.setText(codigo)
        self.campo_nome.setText(nome)
        self.campo_preco_venda.setValue(preco_venda / 100)
        self.campo_preco_custo.setValue(preco_custo / 100)
        self.campo_estoque.setValue(estoque_atual)
        self.campo_minimo.setValue(estoque_minimo)
        self.botao_salvar.setText("Salvar alterações")

    def inativar(self):
        if self.produto_em_edicao is None:
            QMessageBox.warning(self, "Atenção", "Selecione um produto para inativar.")
            return

        resposta = QMessageBox.question(
            self, "Confirmação", "Deseja realmente inativar este produto?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if resposta == QMessageBox.StandardButton.Yes:
            try:
                inativar_produto(self.produto_em_edicao)
            except Exception as erro:
                QMessageBox.critical(self, "Erro", f"Falha ao inativar produto: {erro}")
                return
            self.limpar_campos()
            self.carregar_tabela()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaCadastro()
    janela.show()
    sys.exit(app.exec())