class Errores:
    def __init__(self,tipo,lexema,fila,col) -> None:
        self.tipo=tipo
        self.lexema=lexema
        self.fila=fila
        self.col=col

    def getTipo(self):
        return self.tipo
    def getLexema(self):
        return self.lexema
    def getFila(self):
        return self.fila
    def getCol(self):
        return self.col