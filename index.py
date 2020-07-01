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


def validateDecimal(text):
    return text.isdecimal()


class SearchFrame(ttk.Frame):
    db_name = "database.db"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # attributes
        bgfontcolor = None

        # frame 1
        frame1 = ttk.LabelFrame(self, text='Buscar productos')
        frame1.grid(row=0, column=0, pady=20, padx=20, sticky=W)

        # name input
        Label(frame1, text='Nombre: ', bg=bgfontcolor).grid(row=2, column=0)
        self.name = Entry(frame1, width="45")
        self.name.focus()
        self.name.grid(row=2, column=1)
        self.name.bind('<Key-Return>', self.search_product)

        # sku input
        Label(frame1, text='Codigo: ', bg=bgfontcolor).grid(row=1, column=0)
        self.sku = Entry(frame1, width="45")
        self.sku.grid(row=1, column=1)
        self.sku.bind('<Key-Return>', self.search_product)

        # button search product
        ttk.Button(frame1, text='Buscar producto', command= \
            self.search_product).grid(row=3, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(frame1, text='', fg='red', bg=bgfontcolor, font=16)
        self.message.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # ---- Creating a frame2 container ----
        self.frame2 = Frame(self, bg="light goldenrod yellow")
        self.frame2.grid(row=1, column=0, pady=(0, 20), padx=20)

        # title tables
        Label(self.frame2, text='Resultado de busqueda ', bg="light goldenrod yellow").grid(row=0, column=0)

        # view Table in windowTk
        self.tree = ttk.Treeview(self.frame2, height=15, columns=("name", "price", "qty"))
        self.tree.grid(row=2, column=0, columnspan=2)
        self.tree.heading('#0', text='Codigo', anchor=CENTER)
        self.tree.column("#0", minwidth=80, width=80, stretch=False)
        self.tree.heading('name', text='Nombre', anchor=CENTER)
        self.tree.column("name", minwidth=200, width=200, stretch=False)
        self.tree.heading('price', text='Precio', anchor=CENTER)
        self.tree.column("price", minwidth=100, width=100, stretch=False)
        self.tree.heading('qty', text='Cantidad', anchor=CENTER)
        self.tree.column("qty", minwidth=60, width=60, stretch=False)

        # BUTTON view all database
        self.statusdb = Label(self.frame2, text='status', fg='gray', bg="light goldenrod yellow")
        self.statusdb.grid(row=3, column=0, sticky=W + E)
        ttk.Button(self.frame2, text='Mostrar todo', command=self.get_allproducts).grid(row=3,
                                                                                        column=1, sticky=W + E)

        self.get_allproducts()

    def search_product(self, event=()):
        entry_name = self.name.get()
        entry_sku = self.sku.get()
        countrow = 0
        if len(entry_name) != 0:
            query = "SELECT * FROM products WHERE name LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%" + entry_name + "%")
            db_rows = self.run_query(query, (parameters,))
            for row in db_rows:
                countrow += 1
                self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))
            self.message['text'] = 'Resultados de : {}'.format(entry_name)
            self.name.delete(0, END)
            self.statusdb["text"] = "Articulos: " + str(countrow)
        elif len(entry_sku) != 0:
            query = "SELECT * FROM products WHERE sku LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%" + entry_sku + "%")
            db_rows = self.run_query(query, (parameters,))
            for row in db_rows:
                countrow += 1
                self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))
            self.message['text'] = 'Resultados de : {}'.format(entry_sku)
            self.sku.delete(0, END)
            self.statusdb["text"] = "Articulos: " + str(countrow)
        else:
            self.message['text'] = 'codigo o nombre requerido'

    def get_allproducts(self):
        records = self.tree.get_children()
        countrow = 0
        query = "SELECT * FROM products ORDER BY name COLLATE NOCASE DESC"
        # clean the cells of tree
        for element in records:
            self.tree.delete(element)
        # fill the cells of products database
        db_rows = self.run_query(query)
        for row in db_rows:
            countrow += 1
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))
        self.statusdb["text"] = "Articulos: " + str(countrow)

    def run_query(self, inquery, inparameters=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(inquery, inparameters)
                conn.commit()
            return result
        except sqlite3.OperationalError as e:
            self.message['text'] = 'Error en Base de Datos'
            print("Error in database.db, sqlite3.OperationalError: ", e)
            return


class AddEditFrame(Frame):
    db_name = "database.db"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # attributes
        bgfontcolor = None
        self.old_name = StringVar()

        # frame 1
        frame1 = ttk.LabelFrame(self, text='Agregar Productos')
        frame1.grid(row=0, column=0, pady=20, padx=20, sticky=W)

        # sku input
        Label(frame1, text='Codigo: ', bg=bgfontcolor).grid(row=1, column=0)
        self.sku = Entry(frame1)
        self.sku.focus()
        self.sku.grid(row=1, column=1)

        # name input
        Label(frame1, text='Nombre: ', bg=bgfontcolor).grid(row=2, column=0)
        self.name = Entry(frame1)
        self.name.grid(row=2, column=1)

        # price input
        Label(frame1, text='Precio: ', bg=bgfontcolor).grid(row=3, column=0)
        self.price = Entry(frame1)
        self.price.grid(row=3, column=1)

        # qty input
        Label(frame1, text='Cantidad: ', bg=bgfontcolor).grid(row=4, column=0)
        self.qty = Entry(frame1)
        self.qty.grid(row=4, column=1)
        self.qty.bind('<Key-Return>', self.add_product)

        # add button
        ttk.Button(frame1, text='Añadir Producto', command= \
            self.add_product).grid(row=5, columnspan=2, sticky=W + E)

        # button search product
        ttk.Button(frame1, text='Buscar producto', command= \
            self.search_product).grid(row=6, sticky=W + E)

        # Output Messages
        self.message = Label(frame1, text='', fg='green', bg=bgfontcolor, font=16)
        self.message.grid(row=7, column=0, columnspan=2, sticky=W + E)

        # ---- Creating a frame2 container ----
        self.frame2 = Frame(self, bg="white")
        self.frame2.grid(row=1, column=0, pady=(0, 20), padx=20)

        # title tables
        Label(self.frame2, text='Elimiar ', bg="light goldenrod yellow").grid(row=0, column=0)

        # view Table in window
        self.tree = ttk.Treeview(self.frame2, height=7, columns=("name", "price", "qty"))
        self.tree.grid(row=1, column=0, columnspan=2)
        self.tree.heading('#0', text='Codigo', anchor=CENTER)
        self.tree.column("#0", minwidth=80, width=80, stretch=False)
        self.tree.heading('name', text='Nombre', anchor=CENTER)
        self.tree.column("name", minwidth=200, width=200, stretch=False)
        self.tree.heading('price', text='Precio', anchor=CENTER)
        self.tree.column("price", minwidth=100, width=100, stretch=False)
        self.tree.heading('qty', text='Cantidad', anchor=CENTER)
        self.tree.column("qty", minwidth=60, width=60, stretch=False)
        self.tree.bind('<Double-1>', self.set_cell_value)

        # button delete
        self.delete_button = ttk.Button(self.frame2, text='Eliminar', command= \
            self.delete_product).grid(row=3, column=0, sticky=W + E)

        # button Edit
        self.edit_button = ttk.Button(self.frame2, text='Editar', command= \
            self.set_cell_value).grid(row=3, column=1, sticky=W + E)

        # edit products  

    def set_cell_value(self, event=()):
        try:
            sku_select = self.tree.item(self.tree.selection())['text']
            values_sku = self.tree.item(self.tree.selection())['values']
            a = self.tree.item(self.tree.selection())['values'][0]
            # sku_select: 120012 <class 'int'>
            # values_sku: ['Arena por metro2', '40.0', 900] <class 'list'>
        except IndexError:
            self.message['text'] = 'Seleccionar producto'
            return
        except tk.TclError as e:
            print("ups : ", e)
            return

        # StringVar

        new_sku = StringVar(value=str(sku_select))
        new_name = StringVar(value=str(values_sku[0]))
        new_price = StringVar(value=str(values_sku[1]))
        new_qty = StringVar(value=str(values_sku[2]))

        def okeEdit():
            edit_wind.grab_release()
            #self.tree.grid(row=1, column=0, columnspan=2)
            edit_wind.grid_remove()
            new_date = (new_sku.get(), new_name.get(), new_price.get(), new_qty.get())
            old_date = (sku_select, values_sku[0], values_sku[1], values_sku[2])
            self.edit_records(new_date, old_date)

        def cancelEdit():
            edit_wind.grab_release()
            # self.tree.grid(row=1, column=0, columnspan=2)
            edit_wind.grid_remove()

        # remove widget self.tree
        # self.tree.grid_remove()

        # create top leve for edit products

        edit_wind = Frame(self.frame2, bg="white")
        edit_wind.grid(row=1, column=2, pady=(0, 50))
        edit_wind.grab_set()

        # s et old-new sku
        Label(edit_wind, text='Codigo').grid(row=0, column=0)
        Entry(edit_wind, textvariable=new_sku, width = 10).grid(row=1, column=0)

        # set old-new name
        Label(edit_wind, text='Nombre').grid(row=0, column=1)
        Entry(edit_wind, textvariable=new_name, width = 25).grid(row=1, column=1)

        # set old-new price
        Label(edit_wind, text='Precio').grid(row=0, column=2)
        Entry(edit_wind, textvariable=new_price, width = 10).grid(row=1, column=2)

        # set old qty
        Label(edit_wind, text='Cantidad').grid(row=0, column=3)
        Entry(edit_wind, textvariable=new_qty, width = 10).grid(row=1, column=3)

        ttk.Button(edit_wind, text='OK', command= \
            okeEdit).grid(row=2, column=0, sticky=W + E)

        ttk.Button(edit_wind, text='Cancel', command= \
            cancelEdit).grid(row=2, column=1, sticky=W + E)

    def edit_records(self, innew_date, inold_date):
        new_date = innew_date
        old_date = inold_date

        try:
            new_sku = int(new_date[0])
            new_price = float(new_date[2])
            new_qty = int(new_date[3])
            # old_sku = old_date[0]
            # old_price = float(old_date[2])
            # old_qty = old_date[3]
        except ValueError:
            self.message['text'] = 'Datos invalidos'
        else:
            # add update in database
            query = 'UPDATE products SET sku = ?, name = ?, price = ?, qty = ? WHERE sku = ? AND name = ?'
            parameters = (new_sku, new_date[1], new_price, new_qty, old_date[0], old_date[1])
            self.run_query(query, parameters)
            # self.edit_wind.destroy()
            self.message['text'] = 'Producto {} actualizado'.format(new_date[1])
            self.search_product()

    def delete_product(self):
        self.message['text'] = ''
        sku_select = self.tree.item(self.tree.selection())['text']
        # print("sku:",sku_select,"Type",type(sku_select) , isinstance(sku_select,int))
        if isinstance(sku_select, int):
            # print("Se eliminara:",sku_select )
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

        try:
            int_sku = int(entry_sku)
            float_price = float(entry_price)
            int_qty = int(entry_qty)
        except ValueError:
            self.message['text'] = 'Datos invalidos'
        else:
            self.message['text'] = 'Añadiendo producto...'
            query = 'INSERT INTO products VALUES(?, ?, ?, ?)'
            parameters = (int_sku, entry_name, float_price, int_qty)
            self.run_query(query, parameters)
            self.message['text'] = 'Añadido producto : {} , {}'.format(entry_sku, entry_name)
            self.sku.delete(0, END)
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.qty.delete(0, END)

    def search_product(self, event=()):
        entry_name = self.name.get()
        entry_sku = self.sku.get()
        if len(entry_name) != 0:
            query = "SELECT * FROM products WHERE name LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%" + entry_name + "%")
            db_rows = self.run_query(query, (parameters,))
            for row in db_rows:
                self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))
            self.message['text'] = 'Resultados de : {}'.format(entry_name)
            # self.name.delete(0, END)
        elif len(entry_sku) != 0:
            query = "SELECT * FROM products WHERE sku LIKE ? "
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            # fill the cells of products database
            parameters = ("%" + entry_sku + "%")
            db_rows = self.run_query(query, (parameters,))
            for row in db_rows:
                self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3]))
            self.message['text'] = 'Resultados de : {}'.format(entry_sku)
            # self.sku.delete(0, END)
        else:
            # clean the cells of tree
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)
            self.message['text'] = 'codigo o nombre requerido'

    def run_query(self, inquery, inparameters=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(inquery, inparameters)
                conn.commit()
            return result
        except sqlite3.OperationalError as e:
            self.message['text'] = 'Error en Base de Datos'
            print("Error in database.db, sqlite3.OperationalError: ", e)
            return


class SaleFrame(Frame):
    db_name = "database.db"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sku_sale = IntVar(value=0)
        self.name_sale = StringVar(value="seleccione producto")
        self.price_sale = DoubleVar(value=0.0)
        self.qyt_sale = IntVar(value=0)
        self.subtotal_sale = DoubleVar(value=0.0)
        self.totalSaleWindow = StringVar()

        self.frame1 = Frame(self, bg="white")
        self.frame1.grid(row=1, column=0, pady=(0, 20), padx=20)

        # title tables
        Label(self.frame1, text='Punto de venta', bg="light goldenrod yellow").grid(row=0, column=0)
        self.message = Label(self.frame1, text='Titulo', fg='green', bg="white", font=16)
        self.message.grid(row=1, column=0, columnspan=2, sticky=W + E)

        column_item = ("sku", "name", "price", "qty", "subtotal")
        self.tree = ttk.Treeview(self.frame1, height=20, show="headings", columns=column_item)
        self.tree.grid(row=2, column=0, columnspan=6)
        self.tree.heading('sku', text='Codigo', anchor=CENTER)
        self.tree.column('sku', minwidth=80, width=80, stretch=False)
        self.tree.heading('name', text='Nombre', anchor=CENTER)
        self.tree.column('name', minwidth=200, width=200, stretch=False)
        self.tree.heading('price', text='Precio', anchor=CENTER)
        self.tree.column('price', minwidth=100, width=100, stretch=False)
        self.tree.heading('qty', text='Cantidad', anchor=CENTER)
        self.tree.column('qty', minwidth=60, width=60, stretch=False)
        self.tree.heading('subtotal', text='subTotal', anchor=CENTER)
        self.tree.column('subtotal', minwidth=80, width=80, stretch=False)
        self.tree.bind('<ButtonRelease-1>', self.set_cell_value)

        Label(self.frame1, textvariable=self.totalSaleWindow, bg="white", font=16).grid(\
            row=3, column=4, columnspan=2, sticky=W + E)

        Button(self.frame1, text="Borrar todo", command= self.cleanSales).grid(row= 4, column=0, sticky=W+E)

        Button(self.frame1, text="Borrar ultimo", command=self.cleanLastSales).grid(row=4, column=1, sticky=W+E)

        self.charging = StringVar(value='-')
        Button(self.frame1, text = "Venta",bg="pale green",
               command= self.funVenta).grid(row= 4, column= 2, columnspan= 4, sticky=W+E)

        self.frame2 = LabelFrame(self, text="Detalles producto")
        self.frame2.grid(row=1, column=1, pady=(0, 20), padx=(0,20))

        # sale products
        Label(self.frame2, text="codigo").grid(row=0, column = 0)
        Entry(self.frame2, textvariable= self.sku_sale, state="readonly",
              width= 30).grid(row=0, column = 1, padx= 20)

        Label(self.frame2, text="producto").grid(row=1, column=0)
        Entry(self.frame2, textvariable=self.name_sale, state="readonly", width= 30).grid(row=1, column=1)

        Label(self.frame2, text="precio").grid(row=2, column=0)
        Entry(self.frame2, textvariable=self.price_sale, state="readonly", width= 30).grid(row=2, column=1)

        Label(self.frame2, text="cantidad").grid(row=3, column=0)
        self.entry_qyt_sale = Entry(self.frame2, width= 30, validate="key", textvariable = self.qyt_sale,
                                    validatecommand=(self.frame2.register(validateDecimal), "%S"))
        self.entry_qyt_sale.grid(row=3, column=1)
        self.entry_qyt_sale.bind('<KeyRelease>', self.editQty)

        Label(self.frame2, text="subtotal").grid(row=4, column=0)
        Entry(self.frame2, textvariable=self.subtotal_sale, state="readonly", width= 30).grid(row=4, column=1)

    def funVenta(self):
        records = self.tree.get_children()
        self.totalsaleupdate(records)
        self.totalwindow = Toplevel()
        self.totalwindow.title = 'Edit Product'
        self.totalwindow.iconbitmap("files/volcano.ico")
        x = self.frame1.winfo_rootx()
        y = self.frame1.winfo_rooty()
        self.totalwindow.geometry("+{}+{}".format(x,y))
        self.totalwindow.grab_set()

        Label(self.totalwindow, text='Resumen de venta').grid(row=0, column=0, padx=(20,0),pady=(20,0))

        Label(self.totalwindow, textvariable=self.charging).grid(row=0, column=1, sticky='E')

        str_totalqty_item = str(len(records))
        Label(self.totalwindow, text='Cantidad de productos: {}'.format(str_totalqty_item)).grid( \
                row=1, column=1, padx=(0,20))

        total = self.totalSaleWindow.get()
        Label(self.totalwindow, text='Total: {}'.format(total)).grid( \
            row=2, column=1, padx=(0, 20))

        Button(self.totalwindow, text= "Aceptar", command= self.upSale).grid( \
            row = 4, column= 0, padx=(20,0), pady=(0,20), sticky = "WE")

        Button(self.totalwindow, text="Cancelar", command= self.totalwindow.destroy).grid( \
            row=4, column=1, padx=(0,20), pady=(0,20),sticky="WE")

    def upSale(self):
        records = self.tree.get_children()
        for item in records:
            if self.charging.get()=='--':
                self.charging.set('**')
            else: self.charging.set('--')
            # ritem : ('999', 'acha madera', '15.0', '0', '0.0')
            ritem = self.tree.item(item, 'values')
            parameters = ( int(ritem[0]), )
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute('SELECT * FROM products WHERE sku=?', parameters)
                    dbItem = cursor.fetchone()
                    # FETCHONE: (2041, 'Block 3/4 pulgadas', 1.5, 700)
                    conn.commit()
            except sqlite3.OperationalError as e:
                self.message['text'] = 'Error en Base de Datos'
                print("Error in database.db, sqlite3.OperationalError: ", e)
                return
            newqty =  dbItem[3]-int(ritem[3])

            parameters = (int(ritem[0]), ritem[1], float(ritem[2]), newqty ,
                         dbItem[0], dbItem[1])
            query = 'UPDATE products SET sku = ?, name = ?, price = ?, qty = ? WHERE sku = ? AND name = ?'
            self.run_query(query, parameters)
        self.totalwindow.destroy()

    def totalsaleupdate(self, children):
        if len(children) > 0:
            totalsale =0.0
            for item in children:
                subtotalitem= self.tree.set(item, "subtotal")
                #print( type(self.tree.set(item, "subtotal")) )
                if isinstance(subtotalitem,float) :
                    totalsale +=subtotalitem
            # print(totalsale, type(totalsale))
            self.totalSaleWindow.set("Total: "+str(totalsale))
        else:
            return

    def cleanLastSales(self):
        records = self.tree.get_children()
        if len(records) > 0:
            self.tree.delete(records[-1])
            records = self.tree.get_children()
            self.totalsaleupdate(records)

    def cleanSales(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        self.totalsaleupdate(records)

    def editQty(self, event):
        try:
            sku = self.tree.item(self.tree.selection())['values'][0]
            intQty = int(self.entry_qyt_sale.get())
            price = float(self.tree.item(self.tree.selection())['values'][2])
            records = self.tree.get_children()
        except (IndexError, ValueError):
            self.message['text'] = 'Seleccionar producto'
            return
        except tk.TclError as e:
            print("ups : ", e)
            return
        # print(self.entry_qyt_sale.get(), type(self.entry_qyt_sale.get()))
        # print(values_sku, "sku:", sku)
        if sku == int(self.sku_sale.get()):
            self.tree.set(self.tree.selection(), "qty", self.entry_qyt_sale.get())
            self.tree.set(self.tree.selection(), "subtotal", float(intQty)*price)
            self.totalsaleupdate(records)
            self.message['text'] = '=)'

    def set_cell_value(self, event):
        try:
            values_sku = self.tree.item(self.tree.selection())['values']
            qq = self.tree.item(self.tree.selection())['values'][3]
            # values_sku: [131313, 'piedrin por metro2 ', '50.0', 0, 0] <class 'list'>
        except (IndexError, ValueError):
            self.message['text'] = 'Seleccionar producto'
            return
        except tk.TclError as e:
            print("ups : ", e)
            return
        self.sku_sale.set(values_sku[0])
        self.name_sale.set(values_sku[1])
        self.price_sale.set(values_sku[2])
        self.qyt_sale.set(values_sku[3])

    def run_query(self, inquery, inparameters=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(inquery, inparameters)
                conn.commit()
            return result
        except sqlite3.OperationalError as e:
            self.message['text'] = 'Error en Base de Datos'
            print("Error in database.db, sqlite3.OperationalError: ", e)
            return


class Application(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        # design root
        main_window.title('Control de productos')
        main_window.iconbitmap("files/volcano.ico")
        x = int((main_window.winfo_screenwidth() - main_window.winfo_reqwidth()) / 4)
        main_window.geometry("+{}+30".format(x))
        main_window.config(bg="floral white")
        Button(self, text="Agregar Venta", activebackground="SkyBlue1",
               command=self.addSale).pack(side="bottom")

        # create widget notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()

        self.search_frame = SearchFrame(self.notebook)
        self.notebook.add(
            self.search_frame, text="Busqueda", underline=0, padding=10)

        self.sale_frame = SaleFrame(self.notebook)
        self.notebook.add(
            self.sale_frame, text="Venta", underline=0, padding=10)

        self.addedit_frame = AddEditFrame(self.notebook)
        self.notebook.add(
            self.addedit_frame, text="Editar/Agregar", underline=0, padding=10)

        self.notebook.pack(padx=10, pady=10)
        self.pack()

    def addSale(self):
        # tree_selection = self.search_frame.tree.selection()
        try:
            sku_select = self.search_frame.tree.item(self.search_frame.tree.selection())['text']
            values_sku = self.search_frame.tree.item(self.search_frame.tree.selection())['values']
            a = self.search_frame.tree.item(self.search_frame.tree.selection())['values'][0]
            # sku_select: 120012 <class 'int'>
            # values_sku: ['Arena por metro2', '40.0', 900] <class 'list'>
        except (IndexError, AttributeError):
            self.search_frame.message['text'] = 'Seleccionar producto para venta'
            return
        except tk.TclError as e:
            print("ups : ", e)
            return
        # print(sku_select, type(sku_select))
        # for item in values_sku:
        #     print("Item", item,"Type",type(item) )
        self.sale_frame.tree.insert('', tk.END, values=(sku_select, values_sku[0], values_sku[1], 0, 0))


if __name__ == '__main__':
    main_window = tk.Tk()
    app = Application(main_window)
    app.mainloop()
    print("BYE")

#
