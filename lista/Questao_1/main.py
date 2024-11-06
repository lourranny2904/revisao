import Questão_1.operacao as operacao 
from Questão_1.operacao import *

if __name__ == '__main__':
    a = int(input('Digite o primeiro número:'))
    b = int(input('Digite o outro número:'))
# so para melhor detalhamento sobre 
    print (f"Soma:{operacao.soma(a,b)}")
    print (f"Multiplicação:{operacao.multiplicacao(a,b)}")
    print (f"Subtração:{operacao.subtracao(a,b)}")
    print (f"Divisão{operacao.divisao(a,b)}")

print (operacao.multiplicacao(a,b))
print (resto(a,b))