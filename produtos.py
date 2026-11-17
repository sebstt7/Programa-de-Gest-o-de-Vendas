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

def buscar_produto_por_id(produti_id):
    conc = conectar()
    cur = conc.cursor()
    cur.execute("""
    SELECT id, codigo_barras, nome, preco_venda, preco_custo, estoque_atual, estoque_minimo 
    FROM produtos
    WHERE id = ?""", (produti_id,))
    
    produto = cur.fetchone()
    conc.close()
    return produto

def atualizar_produto(produto_id, codigo_barras, nome, preco_venda, preco_custo, estoque_atual, estoque_minimo):
    conc = conectar()
    cur = conc.cursor()
    cur.execute("""
    UPDATE produtos
    SET codigo_barras = ?, nome = ?, preco_venda = ?, preco_custo = ?, estoque_atual = ?, estoque_minimo = ?
    WHERE id = ?""", (codigo_barras, nome, preco_venda, preco_custo, estoque_atual, estoque_minimo, produto_id))
    
    conc.commit()
    conc.close()

def inativar_produto(produto_id):
    conc = conectar()
    cur = conc.cursor()
    cur.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (produto_id,))
    conc.commit()
    conc.close()


def listar_produtos_inativos():
    conc = conectar()
    cur = conc.cursor()
    cur.execute("""
        SELECT id, codigo_barras, nome, preco_venda,
               estoque_atual, estoque_minimo
        FROM produtos
        WHERE ativo = 0
        ORDER BY nome""")
    produtos = cur.fetchall()
    conc.close()
    return produtos


def reativar_produto(produto_id):
    conc = conectar()
    cur = conc.cursor()
    cur.execute("UPDATE produtos SET ativo = 1 WHERE id = ?", (produto_id,))
    conc.commit()
    conc.close()