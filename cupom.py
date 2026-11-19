from datetime import datetime

from PySide6.QtGui import QFont, QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

import config

def reais (centavos):
    return f"R$ {centavos/ 100:.2f}".replace(".", ",")

def montar_cupom(venda_id, itens, total, forma_pagamento, recebido=None, troco=None):
    L = config.largura_cupom
    linhas = []

    def centro(texto):
        linhas.append(texto.center(L))

    def separador():
        linhas.append("-" * L)

    centro(config.loja_nome)
    if config.loja_endereço:
        centro(config.loja_endereço)
    if config.loja_telefone:
        centro(config.loja_telefone)
    if config.loja_cnpj:
        centro(f"CNPJ: {config.loja_cnpj}")

    separador()
    centro("COMPROVANTE NAO FISCAL")
    separador()
    linhas.append(f"venda: {venda_id}")
    linhas.append(datetime.now().strftime("Data: %d/%m/%y %H:%M"))

    for item in itens:
        linhas.append(item["nome"][:L])
        detalhe = f"{item["quantidade"]} X {reais(item["preco"])}"
        subtotal = reais(item["preco"] * item["quantidade"])
        linhas.append(detalhe + subtotal.rjust(L - len(detalhe)))

    separador()
    total_txt = reais(total)
    linhas.append("TOTAL".ljust(L - len(total_txt)) + total_txt)
    linhas.append(f"Pagamento: {forma_pagamento}")
    if recebido if not None:
        recebido_txt = reais(recebido)
        troco_txt = reais(troco)
        linhas.append("Recebido".ljust(L - len(recebido.txt)) + recebido_txt)
        linhas.append("Troco".ljust(L - len(troco_txt)) + troco_txt)
    separador()
    centro("Obrigado pela preferencia")
    centro("Este comprovante nao tem valor fiscal")

    return "\n".join(linhas)

def imprimir_cupom(texto, parent=None):
    impressora = QPrinter()
    dialogo = QPrintDialog(impressora, parent)
    if dialogo.exec() != QPrintDialog.DialogCode.Accepted:
        return False

    documento = QTextDocument()
    fonte = QFont("Consolas", 8) #fonte de largura fixa
    documento.setDefaultFont(fonte)
    documento.setPlainText(texto)
    documento.print_(impressora)
    return True