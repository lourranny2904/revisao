from produto.produto import Produto
from cliente.cliente import Cliente


nome_produto = input('Digite o nome do produto:')
quantidade_produto = int(input('Digite a quantidade que deseja:'))

produto1 = Produto(nome=nome_produto, preco=29.99, quantidade=quantidade_produto)


print(produto1)
print(f"Valor total: R${produto1.valor_total():.2f}")

nome_cliente = input("Digite o nome do cliente: ")
email_cliente = input("Digite o email do cliente: ")


cliente1 = Cliente(nome=nome_cliente, email=email_cliente)

print(cliente1)