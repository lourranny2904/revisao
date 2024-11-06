class Produto:
     def __init__(self, nome: str, preco: float, quantidade: int):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

     def valor_total(self) -> float:
        return self.preco * self.quantidade

     def __str__(self):
        return (f"Produto(nome={self.nome}, preco={self.preco}, quantidade={self.quantidade})")