#
# programa de auiditoria para Ferreteria basico
# version 10.0 
# fecha: Junio 2020
# javieralo013@gmail.com
# 



import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3

class SearchFrame(ttk.Frame):
    db_name = "database.db"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #atributes
        bgfontcolor= None
        
        #frame 1
        frame1 = ttk.LabelFrame(self, text = 'Buscar productos')
        frame1.grid(row=0,column=0,pady=20,padx=20,sticky=W)
        
       #name input
        Label(frame1, text='Nombre: ',bg=bgfontcolor).grid(row=2, column=0)
        self.name = Entry(frame1)
        self.name.focus()
        self.name.grid(row=2, column=1)
        self.name.bind('<Key-Return>',self.search_product)

        #sku input
        Label(frame1, text='Codigo: ',bg=bgfontcolor).grid(row=1,column=0)
        self.sku = Entry(frame1)
        self.sku.grid(row=1, column=1)
        self.sku.bind('<Key-Return>',self.search_product)        

        #button search product
        ttk.Button(frame1, text = 'Buscar producto', command = \
                    self.search_product).grid(row = 3, columnspan = 2, sticky = W + E) 
        
        # Output Messages
        self.message = Label(frame1, text = '', fg = 'red', bg=bgfontcolor,font=16)
        self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W + E  )

        # ---- Creating a frame2 container ----
        frame2 = Frame(self, bg="light goldenrod yellow" )
        frame2.grid(row=1,column=0,pady=(0,20),padx=20)  

        # title tables
        Label(frame2, text='Resultado de busqueda ',bg="light goldenrod yellow").grid(row=0, column=0)
        
        #   view Table in windowTk
        self.tree = ttk.Treeview(frame2,height = 15, columns = ("name","price","qty"))
        self.tree.grid(row = 2, column = 0,columnspan=2)
        self.tree.heading('#0', text='Codigo', anchor=CENTER)
        self.tree.column("#0", minwidth=80, width=80, stretch=False)
        self.tree.heading('name', text='Nombre', anchor=CENTER)
        self.tree.column("name", minwidth=200, width=200, stretch=False)
        self.tree.heading('price', text='Precio', anchor=CENTER)
        self.tree.column("price", minwidth=100, width=100, stretch=False)
        self.tree.heading('qty', text='Cantidad', anchor=CENTER)
        self.tree.column("qty", minwidth=60, width=60, stretch=False)
        
        
        # BUTTON view all database
        self.statusdb = Label(frame2, text = 'status', fg = 'gray', bg="light goldenrod yellow")
        self.statusdb.grid(row = 3, column = 0, sticky = W+E)
        ttk.Button(frame2,text = 'Mostrar todo', command = self.get_allproducts).grid(row = 3, 
                    column = 1, sticky = W+E)
        
        self.get_allproducts()


    def search_product(self, event=()):
        entry_name = self.name.get()
        entry_sku = self.sku.get()
        countrow = 0
        if len(entry_name) != 0 :
            query = "SELECT * FROM products WHERE name LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%"+entry_name+"%")
            db_rows= self.run_query(query,(parameters,))
            for row in db_rows:
                countrow += 1
                self.tree.insert('', 0, text=row[0], values=(row[1],row[2],row[3]) )
            self.message['text'] = 'Resultados de : {}'.format(entry_name)
            self.name.delete(0, END)
            self.statusdb["text"] = "Articulos: "+str(countrow)
        elif len(entry_sku) != 0 :
            query = "SELECT * FROM products WHERE sku LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%"+entry_sku+"%")
            db_rows= self.run_query(query,(parameters,))
            for row in db_rows:
                countrow += 1
                self.tree.insert('', 0, text=row[0], values=(row[1],row[2],row[3]) )
            self.message['text'] = 'Resultados de : {}'.format(entry_sku)
            self.sku.delete(0, END)
            self.statusdb["text"] = "Articulos: "+str(countrow)
        else:
            self.message['text'] = 'codigo o nombre requerido'        
        
    '''
    def addedit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        sku = self.tree.item(self.tree.selection())['text']
        name = self.tree.item(self.tree.selection())['values'][0]
        print(sku,name)
    '''
        
        
    def get_allproducts(self):
        records = self.tree.get_children()
        countrow = 0
        query = "SELECT * FROM products ORDER BY name COLLATE NOCASE DESC"
        # clean the cells of tree
        for element in records:
            self.tree.delete(element)
        # fill the cells of products database
        db_rows= self.run_query(query)
        for row in db_rows:
            countrow += 1
            self.tree.insert('', 0, text=row[0], values=(row[1],row[2],row[3]) )
        self.statusdb["text"] = "Articulos: "+str(countrow)

    def run_query(self, inquery, inparameters = ()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(inquery, inparameters)
                conn.commit()
            return result
        except sqlite3.OperationalError as e:
                self.message['text'] = 'Error en Base de Datos'
                print("Error in database.db, sqlite3.OperationalError: ",e)
                return


class AddEditFrame(ttk.Frame):
    db_name = "database.db"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #atributes
        bgfontcolor= None
        self.old_name = StringVar()
        
        #frame 1
        frame1 = ttk.LabelFrame(self, text = 'Agregar Productos')
        frame1.grid(row=0,column=0,pady=20,padx=20,sticky=W)

        # sku input
        Label(frame1, text='Codigo: ',bg=bgfontcolor).grid(row=1, column=0)
        self.sku = Entry(frame1)
        self.sku.focus()
        self.sku.grid(row=1, column=1) 
        
        # name input
        Label(frame1, text='Nombre: ',bg=bgfontcolor).grid(row=2, column=0)
        self.name = Entry(frame1)
        self.name.grid(row=2, column=1)

        # price input
        Label(frame1, text='Precio: ',bg=bgfontcolor).grid(row=3, column=0)
        self.price = Entry(frame1)
        self.price.grid(row=3, column=1)  

        # qty input
        Label(frame1, text='Cantidad: ',bg=bgfontcolor).grid(row=4, column=0)
        self.qty = Entry(frame1)
        self.qty.grid(row=4, column=1)
        self.qty.bind('<Key-Return>',self.add_product) 
        
        #add button 
        ttk.Button(frame1, text = 'Añadir Producto', command = \
                    self.add_product).grid(row = 5, columnspan = 2, sticky = W + E)
        
        #button search product
        ttk.Button(frame1, text = 'Buscar producto', command = \
                    self.search_product).grid(row = 6, sticky = W + E )  
                    
        # Output Messages
        self.message = Label(frame1, text = '', fg = 'green', bg=bgfontcolor,font=16)
        self.message.grid(row = 7, column = 0, columnspan = 2, sticky = W + E  )


        # ---- Creating a frame2 container ----
        self.frame2 = Frame(self, bg="white" )
        self.frame2.grid(row=1,column=0,pady=(0,20),padx=20)  

        # title tables
        Label(self.frame2, text='Elimiar ',bg="light goldenrod yellow").grid(row=0, column=0)
        
                    
        #  view Table in windowTk
        self.tree = ttk.Treeview(self.frame2,height = 7, columns = ("name","price","qty"))
        self.tree.grid(row = 1, column = 0,columnspan=2)
        self.tree.heading('#0', text='Codigo', anchor=CENTER)
        self.tree.column("#0", minwidth=80, width=80, stretch=False)
        self.tree.heading('name', text='Nombre', anchor=CENTER)
        self.tree.column("name", minwidth=200, width=200, stretch=False)
        self.tree.heading('price', text='Precio', anchor=CENTER)
        self.tree.column("price", minwidth=100, width=100, stretch=False)
        self.tree.heading('qty', text='Cantidad', anchor=CENTER)
        self.tree.column("qty", minwidth=60, width=60, stretch=False)
        self.tree.bind('<Double-1>', self.set_cell_value)
        
        #button delete
        self.delete_button = ttk.Button(self.frame2,text = 'Eliminar', command = \
                            self.delete_product).grid(row = 3, column = 0, sticky = W + E)

        #button Edit
        self.edit_button = ttk.Button(self.frame2,text = 'Editar', command = \
                            self.edit_product).grid(row = 3, column = 1, sticky = W + E)
        
        # edit products  
        
    def set_cell_value(self, event,position=()):
        try:
            sku_select = self.tree.item(self.tree.selection())['text']
            values_sku = self.tree.item(self.tree.selection())['values']
            self.tree.item(self.tree.selection())['values'][0]
            # sku_select: 120012 <class 'int'>
            # values_sku: ['Arena por metro2', '40.0', 900] <class 'list'>
        except IndexError as e:
            self.message['text'] = 'Seleccionar producto'
            return
        except tk.TclError as e :
            print("ups : ",e)
            return
        
        #StringVar         
        
        
        new_sku = StringVar(value = str(sku_select))
        new_name = StringVar(value = str(values_sku[0]))
        new_price = StringVar(value = str(values_sku[1]))
        new_qty = StringVar(value = str(values_sku[2]))
        
        def  okeEdit():
            edit_wind.grab_release()
            self.tree.grid(row = 1, column = 0,columnspan=2)
            edit_wind.grid_remove()
            new_date = (new_sku.get(),new_name.get() ,new_price.get() , new_qty.get() )
            old_date = (sku_select, values_sku[0], values_sku[1],values_sku[2] )
            self.edit_records(new_date, old_date )
            
        def cancelEdit():
            edit_wind.grab_release()
            self.tree.grid(row = 1, column = 0,columnspan=2)
            edit_wind.grid_remove()
            
        #remove widget self.tree       
        self.tree.grid_remove()

        #create top leve for edit products
        
        edit_wind = Frame(self.frame2, bg="white" )
        edit_wind.grid(row = 2, column = 0,columnspan=2,pady=(0,50))
        edit_wind.grab_set()

        #set old-new sku 
        Label(edit_wind, text='Codigo').grid(row=0,column=0)
        Entry(edit_wind, textvariable = new_sku ).grid(row = 1, column = 0)
 
        
        #set old-new name 
        Label(edit_wind, text='Nombre').grid(row=0,column=1)
        Entry(edit_wind, textvariable = new_name ).grid(row = 1, column = 1)

        
        #set old-new price 
        Label(edit_wind, text='Precio').grid(row=0,column=2)
        Entry(edit_wind, textvariable = new_price ).grid(row = 1, column = 2)
                
        #set old qty 
        Label(edit_wind, text='Cantidad').grid(row=0,column=3)
        Entry(edit_wind, textvariable = new_qty ).grid(row = 1, column = 3)
        
        ttk.Button(edit_wind,text = 'OK', command = \
                    okeEdit).grid(row = 2, column = 0, sticky = W + E)
                    
        ttk.Button(edit_wind,text = 'Cancel', command = \
                    cancelEdit).grid(row = 2, column = 1, sticky = W + E)
        
        



    def edit_records(self, innew_date, inold_date ):
        new_date = innew_date
        old_date = inold_date
        #print(new_date) # ('12', 'Martillo madera', '20.0', '8')
        #print(old_date) # (12, 'Martillo madera', '20.0', 8)
        
        #validar datos de entrada
        #dbtype:     "sku"	INTEGER NOT NULL,
                    #"name"	TEXT NOT NULL,
                    #"price"	REAL NOT NULL,
                    #"qty"	INTEGER,
        new_sku = 0
        new_price = 0.0
        new_qty = 0
        #old_sku = 0
        old_price = 0.0
        #old_qty = 0
        try:
            new_sku = int(new_date[0])
            new_price = float(new_date[2])
            new_qty = int(new_date[3])
            #old_sku = old_date[0]
            old_price = float(old_date[2])
            #old_qty = old_date[3]
        except ValueError:
            self.message['text'] = 'Datos invalidos'
        else:
            ## self.message['text'] = 'Añadiendo producto...'
            ## query = 'INSERT INTO products VALUES(?, ?, ?, ?)'
            ## parameters = (int_sku, entry_name, float_price,int_qty )
            ## self.run_query(query, parameters)
            ## self.message['text'] = 'Añadido producto : {} , {}'.format(entry_sku,entry_name)
            ## ## add update in database
            query = 'UPDATE products SET sku = ?, name = ?, price = ?, qty = ? WHERE sku = ? AND name = ?'
            parameters = (new_sku, new_date[1], new_price, new_qty, old_date[0],old_date[1] )
            self.run_query(query, parameters)
            #self.edit_wind.destroy()
            self.message['text'] = 'Producto {} actualizado'.format(new_date[1])
            self.search_product()
            
        
        
    def delete_product(self):        
        self.message['text'] = ''
        sku_select = self.tree.item(self.tree.selection())['text']
        #print("sku:",sku_select,"Type",type(sku_select) , isinstance(sku_select,int))
        if isinstance(sku_select,int):
            #print("Se eliminara:",sku_select )
            query = 'DELETE FROM products WHERE sku = ?'
            self.run_query(query, (sku_select,))
            self.message['text'] = 'Producto {} Eliminado'.format(sku_select)
            self.search_product()
        else:
            self.message['text'] = 'Producto no seleccionado'
            
    def edit_product(self):
        pass
        

    def add_product(self, event=()):
        entry_sku = self.sku.get()
        entry_name = self.name.get()
        entry_price = self.price.get()
        entry_qty = self.qty.get()
        #flag_validation= len(entry_sku) != 0 and len(entry_name) != 0 \
        #                and len(entry_price) != 0 and len(entry_qty) != 0
        
        #validar datos de entrada
        #dbtype:     "sku"	INTEGER NOT NULL,
                    #"name"	TEXT NOT NULL,
                    #"price"	REAL NOT NULL,
                    #"qty"	INTEGER,
        int_sku = 0
        float_price = 0.0
        int_qty = 0
        try:
            int_sku = int(entry_sku)
            float_price = float(entry_price)
            int_qty = int(entry_qty)
        except ValueError:
            self.message['text'] = 'Datos invalidos'
        else:
            self.message['text'] = 'Añadiendo producto...'
            query = 'INSERT INTO products VALUES(?, ?, ?, ?)'
            parameters = (int_sku, entry_name, float_price,int_qty )
            self.run_query(query, parameters)
            self.message['text'] = 'Añadido producto : {} , {}'.format(entry_sku,entry_name)
            self.sku.delete(0, END)
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.qty.delete(0, END)



    def search_product(self, event=()):
        entry_name = self.name.get()
        entry_sku = self.sku.get()
        if len(entry_name) != 0 :
            query = "SELECT * FROM products WHERE name LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%"+entry_name+"%")
            db_rows= self.run_query(query,(parameters,))
            for row in db_rows:
                self.tree.insert('', 0, text=row[0], values=(row[1],row[2],row[3]) )
            self.message['text'] = 'Resultados de : {}'.format(entry_name)
            #self.name.delete(0, END)
        elif len(entry_sku) != 0 :
            query = "SELECT * FROM products WHERE sku LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%"+entry_sku+"%")
            db_rows= self.run_query(query,(parameters,))
            for row in db_rows:
                self.tree.insert('', 0, text=row[0], values=(row[1],row[2],row[3]) )
            self.message['text'] = 'Resultados de : {}'.format(entry_sku)
            #self.sku.delete(0, END)
        else:
            self.message['text'] = 'codigo o nombre requerido'

        
    def run_query(self, inquery, inparameters = ()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(inquery, inparameters)
                conn.commit()
            return result
        except sqlite3.OperationalError as e:
                self.message['text'] = 'Error en Base de Datos'
                print("Error in database.db, sqlite3.OperationalError: ",e)
                return
        



class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        #design root
        main_window.title('Control de productos')
        main_window.iconbitmap("files/volcano.ico")
        x = int( ( main_window.winfo_screenwidth() - main_window.winfo_reqwidth() ) / 4)
        main_window.geometry( "+{}+50".format(x) )
        main_window.config(bg = "floral white")
 
        #create widget notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        
        self.search_frame = SearchFrame(self.notebook)
        self.notebook.add(
            self.search_frame, text="Busqueda", underline=0, padding=10)
        
        self.addedit_frame = AddEditFrame(self.notebook)
        self.notebook.add(
            self.addedit_frame, text="Editar/Agregar", underline=0, padding=10)
        
        self.notebook.pack(padx=10, pady=10)
        self.pack()
        
if __name__ == '__main__':
    main_window = tk.Tk()
    app = Application(main_window)
    app.mainloop()
    print("BYE")


# 