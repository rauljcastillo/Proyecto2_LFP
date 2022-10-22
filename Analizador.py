from Token import Token
from errores import Errores

class Analizador:
    palabras_reservadas={
        "Etiqueta": "tEtiqueta",
        "Boton": "tBtn",
        "Check": "tCheck",
        "RadioBoton": "tRadBtn",
        "Texto": "tTexto",
        "AreaTexto": "tAreaTxt",
        "Clave": "tClave",
        "Contenedor": "tConten",
        "Controles":"tControles",
        "setAncho": "tAncho",
        "setAlto":"tAlto",
        "setColorFondo": "tColFon",
        "setColorLetra": "tColLet",
        "setAlineacion": "tAlineac",
        "setMarcada": "tMarcada",
        "setTexto": "tsetTexto",
        "add": "tAdd",
        "propiedades": "tProp",
        "Colocacion": "tColoc",
        "setPosicion": "tsetPos",
        "this": "tkID",
        "add": "tAdd",
        "True": "tbool",
        "False": "tbool"

    }

    simbolos={
        "+": "MAS",
        '"': "ComillasD",
        "'": "ComillaS",
        "<": "ANG_A",
        ">": "ANG_C",
        "-": "MENOS",
        ".": "PUNTO",
        ",": "COMA",
        "*": "MULTI",
        "!": "EXCLAM",
        ";": "PUNTCOM",
        "(": "PAREN_A",
        ")": "PAREN_C",
}
    variable1=["tEtiqueta","tBtn","tCheck","tRadBtn","tTexto","tAreaTxt","tClave","tConten","tThis"]
    variable2=["tAncho","tAlto","tColFon","tColLet","tAlineac","tMarcada","tsetTexto"]
    numeros=["ENTERO","REAL"]
    coloc=["tAdd","tsetPos"]

    def __init__(self) -> None:
        self.Salida:list=[]
        self.estado:int=0
        self.auxLex:str=""
        self.fila=1
        self.col=1
        self.errores=[]
        self.cont=0

    #--Empieza analizador léxico--
    def Escanear(self,entrada:str):
        entrada=entrada+"#"
        self.auxLex=""
        contador=0
        c:str
        while contador<=len(entrada)-1:
            c=entrada[contador]        
            if self.estado==0:
                if c.isdigit():
                    self.estado=1
                    self.auxLex=c
                    self.col+=1
                elif c.isalpha():
                    self.estado=5
                    self.col+=1
                    self.auxLex+=c
                elif c in self.simbolos:
                    self.auxLex=c
                    self.col+=1
                    self.agregarToken(self.simbolos[c])
                
                elif c=="/":
                    if entrada[contador+1]=="/":
                        self.auxLex="//"
                        contador+=2
                        self.col+=1
                        self.estado=4
                        continue
                    elif entrada[contador+1]=="*":
                        self.auxLex="/*"
                        contador+=2
                        self.estado=6
                        continue
                    self.auxLex+=c
                    self.col+=1
                    self.agregarToken("SIGNO_DIV")
            
                elif c=="\n":
                    self.fila+=1
                    self.col=1
                    self.auxLex=""
                elif c==" ":
                    self.col+=1

                else:
                    self.col+=1
                    if c=="#" and contador==len(entrada)-1:
                        print("Hemos concluido el análisis")
                    else:
                        self.errores.append(Errores("Lexico",c,self.fila,self.col))
                        self.estado=0
            elif self.estado==1:
                if c.isdigit():
                    self.estado=1
                    self.col+=1
                    self.auxLex+=c
                elif c==".":
                    self.estado=2
                    self.col+=1
                    self.auxLex+=c
                else:
                    self.agregarToken("NUM")
                    contador-=1
            elif self.estado==2:
                if c.isdigit():
                    self.estado=3
                    self.col+=1
                    self.auxLex+=c
                else:
                    self.col+=1
                    self.errores.append(Errores("Lexico",c,self.fila,self.col))
                    self.estado=0
            elif self.estado==3:  #Este estado detecta los numeros despues del punto decimal
                if c.isdigit():
                    self.estado=3
                    self.col+=1
                    self.auxLex+=c
                else:
                    self.col+=1
                    self.agregarToken("NUM")
                    contador-=1
            
            elif self.estado==4:  #Este estado detecta los comentarios de //
                if c=="\n":
                    self.fila+=1
                    self.col=1
                    self.estado=0
                elif c.isascii():
                    self.col+=1
            elif self.estado==5:  #Este estado detecta las cadenas del alfabeto
                if c.isalpha():
                    self.auxLex+=c
                    self.col+=1
                else:
                    if self.auxLex in self.palabras_reservadas:
                        self.agregarToken(self.palabras_reservadas[self.auxLex])
                        contador-=1
                    elif c=="." or c==";" or c==")" or c=="(" or c==" " or c=="\n":
                        self.agregarToken("tkID")
                        contador-=1
                    elif c=="'" or c=='"':
                        self.agregarToken("tCadena")
                        contador-=1
                    else:
                        self.col+=1
                        self.errores.append(Errores("Lexico",c,self.fila,self.col))
                        self.estado=0
            elif self.estado==6:   #Detecta los comentarios multilinea
                if c=="\n":
                    self.fila+=1
                    self.col=1
                elif c=="*":
                    self.col+=1
                    if entrada[contador+1]=="/":
                        self.estado=0
                        contador+=1
                elif c.isascii():
                    self.col+=1

            contador+=1
        return self.Salida
    
    def agregarToken(self,tipo):
        self.Salida.append(Token(tipo,self.auxLex,self.fila,self.col))
        self.auxLex=""
        self.estado=0
    
    def imprimir(self,lista:list):
        for elem in lista:
            print(elem.getTipo(),"-->",elem.getVal())
    
    def listaErr(self):
        return self.errores

#------Inicia analizador sintáctico------

    def contiene3(self,tkn,lexema):
        for elem in self.coloc:
            if elem==tkn:
                self.cont+=1
                return 
        print("Error sintáctico, se esperaba",lexema,"linea:",self.Salida[self.cont].getFil())
        self.cont+=1

    def params(self):
        if self.Salida[self.cont-2].getTipo()=="tAncho" or self.Salida[self.cont-2].getTipo()=="tAlto":
            if self.Parea("NUM","un numero"):
                return
            elif self.Salida[self.cont].getTipo()=="PAREN_C":
                return
            else:
                self.cont+=1

        elif self.Salida[self.cont-2].getTipo()=="tsetTexto":
            a=self.Parea("ComillasD",'"')
            b=self.Parea("tCadena","una cadena")
            c=self.Parea("ComillasD",'"')
            if a and b and c:
                return
            self.cont+=1
        elif self.Salida[self.cont-2].getTipo()=="tColFon" or self.Salida[self.cont-2].getTipo()=="tColLet":
            self.Parea("NUM","un numero")
            self.Parea("COMA",",")
            self.Parea("NUM","un numero")
            self.Parea("COMA",",")
            self.Parea("NUM","un numero")
        elif self.Salida[self.cont-2].getTipo()=="tMarcada":
            if self.Parea("tbool","un booleano"):
                return 
            self.cont+=1
        elif self.Salida[self.cont-2].getTipo()=="tsetPos":
            self.Parea("NUM","un numero")
            self.Parea("COMA",",")
            self.Parea("NUM","un numero")
        elif self.Salida[self.cont-2].getTipo()=="tAdd":
            if self.Parea("tkID","un identificador"):
                return 
            self.cont+=1
            

    def contiene1(self,tkn,lexema):
        for elem in self.variable2:
            if elem==tkn:
                self.cont+=1
                return
        print("Error sintáctico, se esperaba",lexema,"linea:",self.Salida[self.cont].getFil())
        self.cont+=1
        
    def contiene(self,tkn,lexema):
        for elem in self.variable1:
            if elem==tkn:
                self.cont+=1
                return     
        print("Error sintáctico, se esperaba",lexema,"linea:",self.Salida[self.cont].getFil())
        self.cont+=1

    def gramatica_contenido(self):
        if self.Salida[self.cont].getTipo()=="tControles" or self.Salida[self.cont].getTipo()=="MENOS" or self.Salida[self.cont].getTipo()=="ANG_A":
            return None
        else:
            self.contiene(self.Salida[self.cont].getTipo(),"un elemento")
            self.Parea("tkID","un identificador")
            self.Parea("PUNTCOM",";")
            return self.gramatica_contenido()
    
    def gramaticaprop(self):
        if self.Salida[self.cont].getTipo()=="tProp" or self.Salida[self.cont].getTipo()=="MENOS" or self.Salida[self.cont].getTipo()=="ANG_A":
            return None
        else:
            self.Parea("tkID","un identificador")
            self.Parea("PUNTO",".")
            self.contiene1(self.Salida[self.cont].getTipo(),"una propiedad")
            self.Parea("PAREN_A","(")
            self.params()
            self.Parea("PAREN_C",")")
            self.Parea("PUNTCOM",";")
            return self.gramaticaprop()
    
    def gramaticaColoc(self):
        if len(self.Salida)==self.cont or self.Salida[self.cont].getTipo()=="tColoc" or self.Salida[self.cont].getTipo()=="MENOS" or self.Salida[self.cont].getTipo()=="ANG_C":
            return None
        else:
            self.Parea("tkID","un identificador")
            self.Parea("PUNTO",".")
            self.contiene3(self.Salida[self.cont].getTipo(),"una propiedad")
            self.Parea("PAREN_A","(")
            self.params()
            self.Parea("PAREN_C",')')
            self.Parea("PUNTCOM",";")
            return self.gramaticaColoc()

    def Parea(self,Tk,Lexema):
        if self.cont<len(self.Salida):
            if self.Salida[self.cont].getTipo()==Tk:
                self.cont+=1
                return True
        else:
            print("Error sintáctico, se esperaba",Lexema,"linea:",self.Salida[self.cont-1].getFil())
            return False


    def analisisSintactico(self):
        self.Parea("ANG_A","<")
        self.Parea("EXCLAM","!")
        self.Parea("MENOS","-")
        self.Parea("MENOS","-")
        self.Parea("tControles","Controles")
        self.gramatica_contenido()
        self.Parea("tControles","Controles")
        self.Parea("MENOS","-")
        self.Parea("MENOS","-")
        self.Parea("ANG_C",">")

    #Propiedades
        
        self.Parea("ANG_A","<")
        self.Parea("EXCLAM","!")
        self.Parea("MENOS","-")
        self.Parea("MENOS","-")
        self.Parea("tProp","propiedades")
        self.gramaticaprop()
        self.Parea("tProp","propiedades")
        self.Parea("MENOS","-")
        self.Parea("MENOS","-")
        self.Parea("ANG_C",">")

    #Colocacion 
        self.Parea("ANG_A","<")
        self.Parea("EXCLAM","!")
        self.Parea("MENOS","-")
        self.Parea("MENOS","-")
        self.Parea("tColoc","etiqueta Colocacion")
        self.gramaticaColoc()
        self.Parea("tColoc","etiqueta Colocacion")
        self.Parea("MENOS","-")
        self.Parea("MENOS","-")
        self.Parea("ANG_C",">")

        

    def limpiar(self):
        self.errores.clear()
        self.Salida.clear()
        self.cont=0
        self.fila=1
        self.col=1