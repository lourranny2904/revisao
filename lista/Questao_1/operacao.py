def soma (a: int, b: int) -> int:
    return a + b 

def multiplicacao (a: int, b: int) -> int:
    return a * b 

def subtracao (a: int, b: int) -> int:
    return a - b 

def divisao (a: int, b: int) -> int:
    return a / b 

def resto (a: int, b: int) -> int:
    if b == 0:
        return('número não pode ser dividido por 0') 
    else:
        return a/b