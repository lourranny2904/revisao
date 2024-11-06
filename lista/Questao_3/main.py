from database import create_db, get_connection, save
from produto.produto import Produto
from cliente.cliente import Cliente


if __name__ == '__main__':
    # a função create db invoca o acesso a conexão via get_connection
    create_db('banco.db', 'sqlite.sql')    
   

nome_produto = input('Digite o nome do produto:')
quantidade_produto = int(input('Digite a quantidade que deseja:'))

produto1 = Produto(nome=nome_produto, preco=29.99, quantidade=quantidade_produto)
save(produto1, 'banco.db')


print(produto1)
print(f"Valor total: R${produto1.valor_total():.2f}")

nome_cliente = input("Digite o nome do cliente: ")
email_cliente = input("Digite o email do cliente: ")


cliente1 = Cliente(nome=nome_cliente, email=email_cliente)
save(cliente1, 'banco.db')

print(cliente1)