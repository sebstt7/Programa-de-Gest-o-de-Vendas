from Gestao import conectar

def salvar_produto (codigo_barras, nome, preco_venda, preco_custo, estoque_atual, estoque_minimo):
    conc = conectar()
    cur = conc.cursor()
    cur.execute(
        """INSERT INTO produtos (codigo_barras, nome, preco_venda, preco_custo, estoque_atual, estoque_minimo)
        VALUES (?, ?, ?, ?, ?, ?)""", (codigo_barras, nome, preco_venda, preco_custo, estoque_atual, estoque_minimo))
    conc.commit()
    conc.close()

def listar_produtos():
    conc = conectar()
    cur = conc.cursor()
    cur.execute("""
    SELECT id, codigo_barras, nome, preco_venda, estoque_atual, estoque_minimo 
    FROM produtos
    WHERE ativo = 1
    ORDER BY nome""")

    produtos = cur.fetchall()
    conc.close()
    return produtos