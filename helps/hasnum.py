def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

separacion = '4C-">4C'
valores = separacion.split('">')
print valores[1]
print hasNumbers(valores[1])