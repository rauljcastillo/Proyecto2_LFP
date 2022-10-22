from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Treeview
from Analizador import Analizador

class Anal:

    def __init__(self,tk:Tk) -> None:
        self.ventana=tk
        self.ob=Analizador()

    def callback(self,event):
        a,b=self.txt.index("insert").split(".")
        self.var.set(f"Lin. {a}, Col. {int(b)+1}")

    def llamar(self):
        self.ob.limpiar()
        self.cadena=self.txt.get("1.0","end")
        self.cadena=self.cadena.replace("\t","    ")
        lista=self.ob.Escanear(self.cadena)
        self.ob.imprimir(lista)
        self.ob.analisisSintactico()
        errores=self.ob.listaErr()
        for element in errores:
            self.tabla.insert("",END,values=(element.getTipo(),element.getFila(),element.getCol(),f"No se reconoce: {element.getLexema()}"))


    def principal(self):
        menu=Menu(self.ventana)
        self.ventana.resizable(0,0)
        self.ventana.config(menu=menu)
        self.ventana.geometry("930x600")
        self.txt=Text(self.ventana,height=24,width=90)
        self.txt.place(x=20,y=20)
        btn1=Button(self.ventana,text="Analizar",command=self.llamar)
        btn1.place(x=760,y=90,width=130,height=40)
        btn5=Button(self.ventana,text="Limpiar",command=self.limpiar)
        btn5.place(x=760,y=140,width=130,height=40)
        File=Menu(menu,tearoff=0)
        Ayuda=Menu(menu,tearoff=0)

        menu.add_cascade(label= "Archivo", menu=File)
        menu.add_cascade(label= "Ayuda",menu=Ayuda)
        File.add_command(label="Abrir",command=self.abrir)
        File.add_command(label="Guardar",command=self.guardar)
        File.add_command(label="Guardar como",command=self.guardarComo)
        File.add_separator()
        File.add_command(label="Salir",command=self.ventana.quit)
        Ayuda.add_command(label="Manual de usuario")
        Ayuda.add_command(label="Manual técnico")
        Ayuda.add_command(label="Ayuda")

        self.var=StringVar()
        self.var.set("Lin. 1, Col. 1")
        self.lbl=Label(self.ventana,textvariable=self.var,font=("Arial",12,"bold"))
        self.lbl.place(x=600,y=410)
        self.txt.bind("<KeyRelease>",self.callback)
        self.txt.bind("<ButtonRelease-1>",self.callback)

        self.tabla=Treeview(self.ventana,show="headings",columns=("col1","col2","col3","col4"),height=20)
        self.tabla.place(y=440,relheight=0.2,relwidth=1)
        self.tabla.heading("col1",text="Tipo de Error",anchor=CENTER)
        self.tabla.heading("col2",text="Linea",anchor=CENTER)
        self.tabla.heading("col3",text="Columna",anchor=CENTER)
        self.tabla.heading("col4",text="Descripción",anchor=CENTER)

        self.tabla.column("col1", anchor=CENTER, width=15)
        self.tabla.column("col2", anchor=CENTER, width=15)
        self.tabla.column("col3", anchor=CENTER,width=15)
        self.tabla.column("col4", anchor=CENTER)
        style=ttk.Style()
        style.theme_use('clam')
        
        style.configure(
        'Treeview',
        foreground="black",
        font=("Arial ",10,"bold"),
        rowheight=25)

        style.configure(
        'Treeview.Heading',
        font=("Arial",10,"bold"),
        rowheight=15,
        background="gray78") 
        scroll=Scrollbar(self.tabla,orient=VERTICAL,command=self.tabla.yview)
        scroll.pack(side=RIGHT,fill='y')
        self.tabla.configure(yscrollcommand=scroll.set)


        self.ventana.mainloop()

    def abrir(self):
        file=filedialog.askopenfile()
        if file:
            self.ruta=file.name
            try:
                archivo=open(self.ruta,"r")
                lectura=archivo.read()
                messagebox.showinfo(title="Exito",message="Archivo cargado con éxito")
                self.txt.delete("1.0","end")
                self.txt.insert(INSERT,lectura)
                archivo.close()
            except:
                messagebox.showerror(title="Error",message="Error al leer el archivo")
    def guardar(self):
        self.cadena=self.txt.get("1.0","end")
        try:
            file=open(self.ruta,"w")
            file.write(self.cadena)
            file.close()
            messagebox.showinfo(title="Archivo guardado",message="Archivo guardado")
        except:
            messagebox.showerror("Error",message="Error al guardar")
    
    def guardarComo(self):
        self.cadena=self.txt.get("1.0","end")
        archivos = filedialog.asksaveasfilename(filetypes=[("Archivos",".txt")],defaultextension=".txt")
        if archivos:
            ar=open(archivos,"w")
            ar.write(self.cadena)
            ar.close()
        
    def limpiar(self):
        self.txt.delete("1.0","end")
        self.ob.limpiar()
ob=Anal(Tk())
ob.principal()