class Token:

    def __init__(self,tipoToken,val,fila,colum) -> None:
        self.tipoToken=tipoToken
        self.val=val
        self.fila=fila
        self.colum=colum
    
    def getTipo(self):
        return self.tipoToken
        
    def getVal(self):
        return self.val
    
    def getFil(self):
        return self.fila
        
    def getCol(self):
        return self.colum
        




        