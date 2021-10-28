class Factura(object):
    def __init__(self,fecha,referencia,nemisor,nreceptor,valor,iva,total):
        self.fecha = fecha
        self.referencia = referencia
        self.nemisor = nemisor
        self.nreceptor = nreceptor
        self.valor = valor
        self.iva = iva
        self.total = total