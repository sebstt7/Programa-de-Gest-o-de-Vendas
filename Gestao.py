import sqlite3

def conectar():
    conc = sqlite3.connect("comercio.db")
    conc.execute("PRAGMA foreign_keys = ON")
    return conc

def criar_tabelas():
    conc = conectar()
    cur = conc.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_barras TEXT NOT NULL UNIQUE,
        nome TEXT NOT NULL,
        preco_venda INTEGER NOT NULL,
        preco_custo INTEGER DEFAULT 0,
        estoque_atual INTEGER DEFAULT 0 CHECK (estoque_atual >= 0),
        estoque_minimo INTEGER DEFAULT 0,
        ativo INTEGER DEFAULT 1,
        ncm TEXT,
        cfop TEXT,
        origem TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora TEXT NOT NULL,
        total INTEGER NOT NULL,
        forma_pagamento TEXT
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL CHECK (quantidade > 0),
        preco_unitario INTEGER NOT NULL,
        FOREIGN KEY (venda_id) REFERENCES vendas(id),
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
        quantidade INTEGER NOT NULL CHECK (quantidade > 0),
        observacao TEXT,
        data_hora TEXT NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )""")

    conc.commit()
    conc.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco criado com sucesso!")