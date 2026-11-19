import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView,
    QLabel, QComboBox
)
from PySide6.QtGui import QShortcut, QKeySequence

from vendas import buscar_produto_por_codigo, finalizar_venda


def formatar_reais(centavos):
    return f"R$ {centavos / 100:.2f}".replace(".", ",")


class TelaPDV(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDV - Venda")
        self.resize(900, 550)
        self.itens = []

        self.campo_codigo = QLineEdit()
        self.campo_codigo.setPlaceholderText("Bipe o produto ou digite o código de barras e pressione Enter")
        self.campo_codigo.returnPressed.connect(self.adicionar_produto)

        self.label_aviso = QLabel("")
        self.label_aviso.setStyleSheet("color: #e74c3c;")

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["Código", "Produto", "Qtd", "Preço unit.", "Subtotal"]
        )
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela.horizontalHeader().setStretchLastSection(True)

        self.label_total = QLabel("TOTAL: R$ 0,00")
        self.label_total.setStyleSheet("font-size: 25px; font-weight: bold;")

        self.combo_pagamento = QComboBox()
        self.combo_pagamento.addItems(["Dinheiro", "Pix", "Cartão de débito", "Cartão de crédito"])

        self.botao_remover = QPushButton("Remover item")
        self.botao_remover.clicked.connect(self.remover_item)
        self.botao_cancelar = QPushButton("Cancelar venda")
        self.botao_cancelar.clicked.connect(self.cancelar_venda)
        self.botao_finalizar = QPushButton("Finalizar venda (F2)")
        self.botao_finalizar.clicked.connect(self.finalizar)

        QShortcut(QKeySequence("F2"), self, activated=self.finalizar)

        rodape = QHBoxLayout()
        rodape.addWidget(self.botao_remover)
        rodape.addWidget(self.botao_cancelar)
        rodape.addStretch()
        rodape.addWidget(QLabel("Pagamento:"))
        rodape.addWidget(self.combo_pagamento)
        rodape.addWidget(self.botao_finalizar)

        layout = QVBoxLayout(self)
        layout.addWidget(self.campo_codigo)
        layout.addWidget(self.label_aviso)
        layout.addWidget(self.tabela)
        layout.addWidget(self.label_total)
        layout.addLayout(rodape)

        self.campo_codigo.setFocus()

    def adicionar_produto(self):
        codigo = self.campo_codigo.text().strip()
        self.campo_codigo.clear()
        self.label_aviso.setText("")
        if not codigo:
            return

        produto = buscar_produto_por_codigo(codigo)
        if produto is None:
            self.label_aviso.setText(f"Produto não encontrado: {codigo}")
            return

        produto_id, codigo_barras, nome, preco, estoque = produto

        for item in self.itens:
            if item["produto_id"] == produto_id:
                if item["quantidade"] + 1 > estoque:
                    self.label_aviso.setText(
                        f"Estoque insuficiente de {nome} (disponível: {estoque})")
                    return
                item["quantidade"] += 1
                break
        else:
            if estoque < 1:
                self.label_aviso.setText(f"{nome} está sem estoque.")
                return
            self.itens.append({
                "produto_id": produto_id,
                "codigo": codigo_barras,
                "nome": nome,
                "preco": preco,
                "quantidade": 1,
            })

        self.atualizar_tela()

    def atualizar_tela(self):
        self.tabela.setRowCount(len(self.itens))
        total = 0
        for linha, item in enumerate(self.itens):
            subtotal = item["preco"] * item["quantidade"]
            total += subtotal
            valores = [item["codigo"], item["nome"], item["quantidade"],
                       formatar_reais(item["preco"]), formatar_reais(subtotal)]
            for coluna, valor in enumerate(valores):
                self.tabela.setItem(linha, coluna, QTableWidgetItem(str(valor)))
        self.label_total.setText(f"TOTAL: {formatar_reais(total)}")
        self.tabela.scrollToBottom()

    def remover_item(self):
        linha = self.tabela.currentRow()
        if linha < 0:
            self.label_aviso.setText("Clique em um item da lista para remover.")
        else:
            del self.itens[linha]
            self.atualizar_tela()
        self.campo_codigo.setFocus()

    def cancelar_venda(self):
        if self.itens:
            resposta = QMessageBox.question(
                self, "Confirmação", "Cancelar a venda inteira?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if resposta != QMessageBox.StandardButton.Yes:
                self.campo_codigo.setFocus()
                return
        self.nova_venda()

    def finalizar(self):
        if not self.itens:
            self.label_aviso.setText("Nenhum item na venda.")
            self.campo_codigo.setFocus()
            return

        try:
            venda_id, total = finalizar_venda(
                self.itens, self.combo_pagamento.currentText()
            )
        except Exception as erro:
            QMessageBox.critical(self, "Erro", f"Não foi possível finalizar a venda:\n{erro}")
            self.campo_codigo.setFocus()
            return

        QMessageBox.information(
            self, "Venda concluída",
            f"Venda nº {venda_id}\nTotal: {formatar_reais(total)}"
        )
        self.nova_venda()

    def nova_venda(self):
        self.itens = []
        self.label_aviso.setText("")
        self.atualizar_tela()
        self.campo_codigo.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPDV()
    janela.show()
    sys.exit(app.exec())