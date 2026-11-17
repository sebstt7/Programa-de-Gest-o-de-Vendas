from datetime import datetime
from Gestao import conectar

def buscar_produto_por_codigo(codigo):
    conc = conectar()
    cur = conc.cursor()
    cur.execute("""
SELECT id, codigo_barras, nome, preco_venda, estoque_atual
FROM produtos
WHERE codigo_barras = ? AND ativo = 1""", (codigo))
    produto = cur.fetchone()
    conc.close()
    return produto

def finalizar_venda(itens, forma_pagamento):
    total = sum(i["preco"] * i["quantidade"] for i in itens)
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conc = conectar()
    try:
        cur = conc.cursor()
        cur.execute(
            "INSERT INTO vendas (data_hora, total, forma_pagamento) VALUES (?, ?, ?)",
            (agora, total, forma_pagamento))
        venda_id = cur.lastrowid

        for i in itens:
            cur.execute("""
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)""",
                (venda_id, i["id"], i["quantidade"], i["preco"]))

            cur.execute("""
                UPDATE produtos
                SET estoque_atual = estoque_atual - ?
                WHERE id = ? AND estoque_atual >= ?""",
                (i["quantidade"], i["id"], i["quantidade"]))
            if cur.rowcount == 0:
                    raise ValueError(f"Estoque insuficiente para o produto {i['nome']}.")
            cur.execute("""
                INSERT INTO movimentacoes_estoque (produto_id, tipo, quantidade, data_hora)
                VALUES (?, 'SAIDA', ?, ?)""",
                (i["produto_id"], i["quantidade"], agora))

        conc.commit()
        return venda_id, total
    except Exception:
        conc.rollback()
        raise
    finally:
        conc.close()
