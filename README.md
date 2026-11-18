Sistema de Gestão Comercial
Aplicação desktop em desenvolvimento para organizar o cadastro de produtos de um pequeno comércio.

Ideia
Centralizar informações de produtos — como código de barras, preços e estoque — em uma interface simples, com base para incluir vendas e movimentações de estoque futuramente.

O que já funciona
Cadastrar, listar e editar produtos.
Inativar e reativar produtos sem apagá-los.
Validar informações básicas, como código de barras único e preço de venda maior que zero.
Armazenar os dados localmente em SQLite.
Pontos fortes
Simples e local: interface desktop e banco SQLite, sem depender de um servidor.
Dados protegidos por regras básicas: por exemplo, código de barras único e estoque atual não negativo.
Estrutura modular: interface, funções de produtos e banco ficam separados.
Pronto para evoluir: o banco já prevê vendas e movimentações de estoque; esses fluxos ainda estão em desenvolvimento.
Tecnologias
Python · PySide6 · SQLite

Como iniciar
Instale o PySide6 e execute primeiro Gestao.py para criar o banco; depois, execute main.py para abrir a interface. Os nomes pressupõem a organização dos módulos descrita no código.

Uso de inteligência artificial
Claude foi usado como apoio para acelerar o desenvolvimento. O assistente do Replit ajudou a analisar os trechos de código e organizar esta documentação.
