from Analizador import Analizador
file=open("./texto.txt","r")
entrada=file.read()
file.close()
ob1=Analizador()
lista=ob1.Escanear(entrada)
ob1.imprimir(lista)
ob1.listaErr()