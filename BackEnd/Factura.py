import re

class Factura(object):
    def __init__(self,fecha,referencia,nemisor,nreceptor,valor,iva,total):
        self.fecha = fecha
        self.referencia = referencia
        self.nemisor = nemisor
        self.nreceptor = nreceptor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.codaprobacion = ''

    def imprimir(self):
        print('-----------------------------------------------------------')
        print(self.fecha)
        print(self.referencia)
        print(self.nemisor)
        print(self.nreceptor)
        print(self.valor)
        print(self.iva)
        print(self.total)



def encontrarFecha(texto):
    fecha = re.findall('\d\d\/\d\d\/\d\d\d\d',texto)
    return fecha[0]
