import tkinter

from utils import *
from tkinter import *
from tkinter import ttk
import time
from tkcalendar import DateEntry
from collections import abc

class Fund():
    """
    Clase base para crear la vetana principal
    """
    DB = 'database/FundStatus.db'
    COLUMNSPAN = 2
    MAIN_FONT = 'Malgun Gothic Semilight'
    LABEL_FONT = 'Calibri'
    FRAME_PADY = 15
    FRAME_PADX = 25
    ENTRY_PADX = 15
    ENTRY_PADY = 20
    DATE_WIDTH = 15
    ENTRY_WIDTH = 20

    # In the init function the main window is defined, then in each function the new popping window and its actions
    # are defined. Auxiliary functions are defined in Utils.py
    def __init__(self, root):
        self.main_window = root
        self.main_window.title('App de gestion de fondos de inversion')
        self.main_window.resizable(1,1)
        self.main_window.wm_iconbitmap('resources/banco.ico')

        # Variables that are needed for the edit_deposit function
        self.selected = ()

        # Styles
        sButton = ttk.Style()
        sButton.configure('my.TButton', font=(self.MAIN_FONT, 12))
        sDrop = ttk.Style()
        sDrop.configure('my.TCombobox', font=(self.MAIN_FONT, 12))

        # Frame for operating with the 'Deposits'
        deposit_frame = LabelFrame(self.main_window, text='Operaciones con los aportes a fondos', font=self.LABEL_FONT, labelanchor=N)
        deposit_frame.grid(row=0, column=0, rowspan=3,columnspan=self.COLUMNSPAN, padx=self.FRAME_PADX, pady=self.FRAME_PADY, sticky=W+E)
        # Add deposit button
        self.add_deposit_button = ttk.Button(deposit_frame,text='Añadir aporte a fondo', style='my.TButton', command=self.add_deposit_window)
        self.add_deposit_button.grid(row=0, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=20)
        # Edit deposit button
        self.edit_deposit_button = ttk.Button(deposit_frame, text='Editar aportes realizados a fondo',
                                              style='my.TButton', command=self.edit_deposit_window)
        self.edit_deposit_button.grid(row=1, column=0, columnspan=self.COLUMNSPAN, sticky=W + E, padx=20, ipadx=20)
        # Delete deposit button
        self.del_deposit_button = ttk.Button(deposit_frame, text='Eliminar aporte realizado a fondo', style='my.TButton')
        self.del_deposit_button.grid(row=2, column=0, columnspan=self.COLUMNSPAN, sticky=W + E, padx=20)

        # Frame for operating with the 'Visualizations'
        visu_frame = LabelFrame(self.main_window, text='Opciones de visualizacion', font=self.LABEL_FONT, labelanchor=N)
        visu_frame.grid(row=4, column=0, rowspan=2, columnspan=self.COLUMNSPAN, padx=self.FRAME_PADX, pady=self.FRAME_PADY, sticky=W+E)
        # Add deposit button
        self.profits_button = ttk.Button(visu_frame, text='Rentabilidad total', style='my.TButton')
        self.profits_button.grid(row=4, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=25)
        # Edit deposit button
        self.profits_per_deposit_button = ttk.Button(visu_frame, text='Rentabilidad por aportacion', style='my.TButton')
        self.profits_per_deposit_button.grid(row=5, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=25)

        # Frame for operating with 'Funds'
        fund_frame = LabelFrame(self.main_window, text='Operaciones con los fondos', font=self.LABEL_FONT, labelanchor=N)
        fund_frame.grid(row=6, column=0, rowspan=3, columnspan=self.COLUMNSPAN, padx=self.FRAME_PADX,
                        pady=self.FRAME_PADY,sticky=W+E)
        # Add fund button
        self.add_fund_button = ttk.Button(fund_frame, text='Añadir nuevo fondo', style='my.TButton',
                                          command=self.add_fund_window)
        self.add_fund_button.grid(row=7, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=25)
        # Edit fund button
        self.edit_fund_button = ttk.Button(fund_frame, text='Editar tabla del fondo', style='my.TButton',
                                           command=self.edit_fund_window)
        self.edit_fund_button.grid(row=8, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20)
        # Delete fund button
        self.del_fund_button = ttk.Button(fund_frame, text='Eliminar fondo', style='my.TButton',
                                          command=self.delete_fund_window)
        self.del_fund_button.grid(row=9, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20)

    # Functions of each window
    def add_deposit_window(self):
        '''
        Creates the window to add a deposit to the fund
        '''
        window = self.new_window('Añadir aporte a fondo')
        # Date entry
        date_label = Label(window, text='Introduzca la fecha: ', font=self.LABEL_FONT)
        date_label.grid(row=0, column=0, sticky=W, padx=self.ENTRY_PADX)
        date_entry = DateEntry(window, selectmode='day', date_pattern='yyyy-mm-dd', state='readonly', width=self.DATE_WIDTH)
        date_entry.grid(row=0, column=1, sticky=W, padx=self.ENTRY_PADX)
        # Dropdown menu
        drop_label = Label(window, text='Seleccione el fondo al que ingresar: ', font=self.LABEL_FONT)
        drop_label.grid(row=1, column=0, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        drop_entry = self.dropdown_menu(window)
        drop_entry.grid(row=1, column=1, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        # Desposit entry
        deposit_label = Label(window, text='Introduzca la cantidad ingresada: ', font=self.LABEL_FONT)
        deposit_label.grid(row=2, column=0, padx=self.ENTRY_PADX, sticky=W)
        deposit_entry = Entry(window, width=self.ENTRY_WIDTH)
        deposit_entry.grid(row=2, column=1, padx=self.ENTRY_PADX, sticky=W)
        # Number of participations entry
        participations_label = Label(window, text='Introduzca el nº de participaciones: ', font=self.LABEL_FONT)
        participations_label.grid(row=3, column=0, padx=self.ENTRY_PADX, sticky=W)
        participations_entry = Entry(window, width=self.ENTRY_WIDTH)
        participations_entry.grid(row=3, column=1, padx=self.ENTRY_PADX, sticky=W)
        # Save button
        create_button = ttk.Button(window, text='Añadir aporte', style='my.TButton',
                                   command=lambda: self.add_deposit(window, date_entry, drop_entry, deposit_entry,participations_entry))
        create_button.grid(row=4, columnspan=2, ipadx=50, pady=20)

    def add_deposit(self,window,date_entry, drop_entry, deposit_entry, participations_entry):
        mensaje = Label(window,text='')
        mensaje.grid(row=5, columnspan=2, sticky=W + E)
        # To handle the float conversion error
        try:
            date, fund, deposit, participations = date_entry.get(), drop_entry.get(), float(deposit_entry.get()), float(participations_entry.get())
        except ValueError:
            mensaje['fg'] = 'red'
            mensaje['text'] = 'Datos introducidos incorrectos, el aporte no ha sido creado'
            deposit_entry.delete(0,END)
            participations_entry.delete(0,END)
            return
        # To check whether the inputs can be inserted into the database
        if validate_date(date) and validate_name(fund) and validate_number(deposit) and validate_number(participations):
            create_deposit(self.DB, {'date': date, 'fund': fund, 'deposit':deposit, 'participations':participations})
            mensaje['fg'] = 'green'
            mensaje['text'] = 'Aporte creado correctamente, la ventana se va a cerrar automaticamente'
            window.after(3000, window.destroy)
        else:
            mensaje['fg'] = 'red'
            mensaje['text'] = 'Datos introducidos incorrectos, el aporte no ha sido creado'
            deposit_entry.delete(0, END)
            participations_entry.delete(0, END)

    def edit_deposit_window(self):
        """

        :return:
        """
        window = self.new_window('Editar aporte a fondo')
        window.geometry('650x450')
        # Frame to select the fund and refresh the view
        fund_frame = Frame(window)
        #fund_frame.grid(row=0, column=0, columnspan=2,padx=5, pady=5)
        fund_frame.pack(pady=5)
        # Dropdown menu to select the fund to be visualized
        drop_label = Label(fund_frame, text='Seleccione el fondo al que ingresar: ', font=self.LABEL_FONT)
        drop_label.grid(row=0, column=0, padx=self.ENTRY_PADX, sticky=W)
        drop_entry = self.dropdown_menu(fund_frame)
        drop_entry.grid(row=0, column=1, padx=self.ENTRY_PADX, sticky=W)

        # Create the frame for the visualizations
        table_frame = Frame(window)
        #table_frame.grid(row=1, column=0, rowspan=10,columnspan=2, padx=5, pady=5)
        table_frame.pack()
        # Scrollbar
        vscroll = Scrollbar(table_frame, orient=tkinter.VERTICAL)
        vscroll.grid(row=0, rowspan=10, column=5, sticky=N + S)
        # Create the table object that represents the deposits of the selected fund
        table_list = ttk.Treeview(table_frame, yscrollcommand=vscroll.set)
        table_list.grid(row=1, column=0, columnspan=5, padx=5)
        # Config the scrolls
        vscroll.config(command=table_list.yview)
        # Initialize columns
        self.initialize_table(table_list)

        # Create the entries where the text is going to be edited
        boxes_frame = Frame(window)
        boxes_frame.pack(padx=20,pady=20)
        # Labels
        id_l = Label(boxes_frame, text=DB_COLUMNS[0])
        id_l.grid(row=0, column=0)
        date_l = Label(boxes_frame, text=DB_COLUMNS[1])
        date_l.grid(row=0, column=1)
        deposit_l = Label(boxes_frame, text=DB_COLUMNS[2])
        deposit_l.grid(row=0, column=2)
        participation_l = Label(boxes_frame, text=DB_COLUMNS[3])
        participation_l.grid(row=0, column=3)
        value_l = Label(boxes_frame, text=DB_COLUMNS[4])
        value_l.grid(row=0, column=4)
        # Boxes
        id_box = Entry(boxes_frame)
        id_box.grid(row=1, column=0)
        date_box = Entry(boxes_frame)
        date_box.grid(row=1, column=1)
        deposit_box = Entry(boxes_frame)
        deposit_box.grid(row=1, column=2)
        participation_box = Entry(boxes_frame)
        participation_box.grid(row=1, column=3)
        value_box = Entry(boxes_frame)
        value_box.grid(row=1, column=4)

        # Buttons section
        buttons_frame = Frame(window)
        buttons_frame.pack(pady=5)

        update_button = ttk.Button(
            buttons_frame, text='Actualizar datos', style='my.TButton',
            command= lambda: self.update_record(window, drop_entry.get(), table_list,
                                                id_box, date_box, deposit_box, participation_box, value_box, message)
        )
        update_button.grid(row=0, column=0, padx=20)

        clear_button = ttk.Button(
            buttons_frame, text='Limpiar registros', style='my.TButton',
            command=lambda: self.clear_entries(id_box, date_box, deposit_box, participation_box, value_box)
        )
        clear_button.grid(row=0, column=1, padx=20)

        # Message
        message_frame = Frame(window)
        message_frame.pack(pady=10)
        message = Label(message_frame, text='')
        message.grid(row=0, column=0, pady=5)

        # Binds
        # Bind the dropdown menu to refresh the table everytime its value changes
        drop_entry.bind(
            "<<ComboboxSelected>>",
            lambda event, args=(drop_entry, table_list): self.on_combo_click(event, args)
        )
        # Bind the double click to the select record function
        table_list.bind('<Double-1>',
                        lambda event, args=(table_list, id_box, date_box,
                                            deposit_box, participation_box, value_box):
                        self.select_record(event, args))

    def update_record(self, window: Toplevel, fund, table: ttk.Treeview, id_box, date_box,
                      deposit_box, participation_box, value_box, message):
        """

        :param message:
        :param table:
        :param id_box:
        :param date_box:
        :param deposit_box:
        :param participation_box:
        :param value_box:
        :return:
        """
        try:
            id, date, deposit, participations, value = id_box.get(), date_box.get(), float(deposit_box.get()), \
                                                       float(participation_box.get()), float(value_box.get())
        except ValueError:
            message['fg'] = 'red'
            message['text'] = 'Datos introducidos incorrectos, el aporte no ha sido editado'
            # Clear the message after 1 second
            window.after(2000, self.delete_message, message)
            return
        # To check whether the inputs can be inserted into the database
        if validate_date(date) and validate_name(fund) and validate_number(deposit) and validate_number(participations):
            #edit_deposit(self.DB, {'fund': fund, 'id': id, 'date': date, 'deposit': deposit, 'participations': participations, 'value': value})
            message['fg'] = 'green'
            message['text'] = 'Aporte editado correctamente'
        else:
            message['fg'] = 'red'
            message['text'] = 'Datos introducidos incorrectos, el aporte no ha sido editado'

        # Clear the message after 1 second
        window.after(2000, self.delete_message, message)

        # Write new items to the table
        table.item(self.selected, text='',
                   values=(id, date, deposit, participations, value)
                   )

        # Clear the boxes after 1 second
        window.after(1000, self.clear_boxes, id_box, date_box, deposit_box, participation_box, value_box)

    @staticmethod
    def delete_message(message):
        message['text'] = ''

    @staticmethod
    def clear_boxes(*args):
        for item in args:
            item.delete(0, END)

    def select_record(self, event, args):
        table, id_box, date_box, deposit_box, participation_box, value_box = args

        # Clear boxes
        self.clear_boxes(id_box, date_box, deposit_box, participation_box, value_box)

        # Grab record number
        self.selected = table.selection()

        # Grab record values
        values = table.item(self.selected, 'values')
        id_box.insert(0, values[0])
        date_box.insert(0, values[1])
        deposit_box.insert(0, values[2])
        participation_box.insert(0, values[3])
        value_box.insert(0, values[4])

    def on_combo_click(self, event, args):
        drop_entry, table_frame = args
        # Call the function that prints the deposits of the selected fund
        self.visualize_table(drop_entry.get(),table_frame)

    def clear_entries(self, id_box, date_box, deposit_box, participation_box, value_box):
        # Clear previous selection
        id_box.delete(0, END)
        date_box.delete(0, END)
        deposit_box.delete(0, END)
        participation_box.delete(0, END)
        value_box.delete(0, END)

    def clear_table(self, table: ttk.Treeview):
        for item in table.get_children():
            table.delete(item)

    def visualize_table(self, fund_name, table_list: ttk.Treeview, dates=None):
        """
        Function that prints the values of a fund in the table
        :return:
        """
        # Delete previous entries
        self.clear_table(table_list)
        # Add the values to the table
        deposits = get_deposits_of_a_fund(self.DB, fund_name)
        #columns = [x for x in deposits.keys()]
        for index, deposit in enumerate(deposits):
            table_list.insert(parent='', index='end', iid=index, values=deposit)

    def initialize_table(self, table):
        # Format columns
        table['columns'] = DB_COLUMNS
        table.column("#0", width=0, stretch=NO)
        table.column(DB_COLUMNS[0], anchor=CENTER, width=40)
        table.column(DB_COLUMNS[1], anchor=CENTER, width=85)
        table.column(DB_COLUMNS[2], anchor=CENTER, width=100)
        table.column(DB_COLUMNS[3], anchor=CENTER, width=100)
        table.column(DB_COLUMNS[4], anchor=CENTER, width=120)
        # Headings of the columns
        table.heading("#0", text='', anchor=W)
        table.heading(DB_COLUMNS[0], text=DB_COLUMNS[0], anchor=CENTER)
        table.heading(DB_COLUMNS[1], text=DB_COLUMNS[1], anchor=CENTER)
        table.heading(DB_COLUMNS[2], text=DB_COLUMNS[2], anchor=CENTER)
        table.heading(DB_COLUMNS[3], text=DB_COLUMNS[3], anchor=CENTER)
        table.heading(DB_COLUMNS[4], text=DB_COLUMNS[4], anchor=CENTER)
        table.tag_configure('oddrow', background='white')
        table.tag_configure('evenrow', background='cyan')

    def add_fund_window(self):
        """
        Creates the window for adding a Fund to the database
        :return:
        """
        window = self.new_window('Añadir aporte a fondo')
        # Label and entry to write the name
        name_label = Label(window, text='Introduzca el nombre del fondo: ',font=self.LABEL_FONT)
        name_label.grid(row=0, column=0, padx=5)
        name_entry = Entry(window)
        name_entry.focus()
        name_entry.grid(row=0, column=1, pady=self.ENTRY_PADY ,padx=self.ENTRY_PADX, ipadx=50)
        # Button to save the changes and check if the name is correct
        create_button = ttk.Button(window, text='Crear fondo', style='my.TButton', command=lambda: self.add_fund(window,name_entry))
        create_button.grid(row=1, columnspan=2, ipadx=self.ENTRY_PADX, pady=5)


    def add_fund(self, window, name_entry):
        mensaje = Label(window,text='')
        mensaje.grid(row=3, columnspan=2, sticky=W + E)
        fund_name = name_entry.get()
        if validate_name(fund_name):
            create_fund_db(self.DB, fund_name)
            mensaje['fg'] ='green'
            mensaje['text'] = 'Fondo creado correctamente, la ventana se va a cerrar automaticamente'
            window.after(3000, window.destroy)
        else:
            mensaje['fg'] = 'red'
            mensaje['text'] = 'Datos introducidos incorrectos, el fondo no ha sido creado'
            name_entry.delete(0, END)

    def edit_fund_window(self):
        '''
        Creates the window to add a deposit to the fund
        '''
        window = self.new_window('Editar nombre a fondo')
        # Dropdown menu
        drop_label = Label(window, text='Seleccione el fondo: ', font=self.LABEL_FONT)
        drop_label.grid(row=0, column=0, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        drop_entry = self.dropdown_menu(window)
        drop_entry.grid(row=0, column=1, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        # New name entry
        name_label = Label(window, text='Introduzca el nuevo nombre: ', font=self.LABEL_FONT)
        name_label.grid(row=2, column=0, padx=self.ENTRY_PADX, sticky=W)
        name_entry = Entry(window, width=self.ENTRY_WIDTH)
        name_entry.grid(row=2, column=1, padx=self.ENTRY_PADX, sticky=W)
        # Save button
        create_button = ttk.Button(window, text='Validar nuevo nombre', style='my.TButton',
                                   command=lambda: self.edit_fund(window, drop_entry, name_entry))
        create_button.grid(row=3, columnspan=2, ipadx=50, pady=20)

    def edit_fund(self, window, drop_entry: ttk.Combobox, name_entry: Entry):
        '''
        Wraps the logic of the edit fund window
        :param window:
        :param drop_entry:
        :param name_entry:
        :return:
        '''
        mensaje = Label(window, text='')
        mensaje.grid(row=5, columnspan=2, sticky=W + E)
        old_name, new_name = drop_entry.get(), name_entry.get()
        # To check whether the inputs can be inserted into the database
        if validate_name(old_name) and validate_name(new_name):
            edit_fund(self.DB, old_name, new_name)
            mensaje['fg'] = 'green'
            mensaje['text'] = 'Fondo editado correctamente, la ventana se va a cerrar automaticamente'
            window.after(3000, window.destroy)
        else:
            mensaje['fg'] = 'red'
            mensaje['text'] = 'Datos introducidos incorrectos, el aporte no ha sido creado'
            name_entry.delete(0, END)

    def delete_fund_window(self):
        '''
        Creates the window to delete a deposit to the fund
        '''
        window = self.new_window('Eliminar fondo')
        # Dropdown menu
        drop_label = Label(window, text='Seleccione el fondo a eliminar: ', font=self.LABEL_FONT)
        drop_label.grid(row=0, column=0, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        drop_entry = self.dropdown_menu(window)
        drop_entry.grid(row=0, column=1, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        # Save button
        create_button = ttk.Button(window, text='Validar nuevo nombre', style='my.TButton',
                                   command=lambda: self.delete_fund(window, drop_entry))
        create_button.grid(row=2, columnspan=2, ipadx=80, pady=20, padx=50, sticky=W+E)

    def delete_fund(self, window, drop_entry: ttk.Combobox):
        """

        :param window:
        :param drop_entry:
        :return:
        """
        mensaje = Label(window, text='')
        mensaje.grid(row=3, columnspan=2, sticky=W + E)
        fund_name = drop_entry.get()
        delete_fund_from_db(self.DB, fund_name)
        mensaje['fg'] = 'green'
        mensaje['text'] = 'Fondo eliminado correctamente, la ventana se va a cerrar automaticamente'
        window.after(3000, window.destroy)


    # Auxiliary functions
    def new_window(self,title=''):
        """
        Creates a new window with the title, resizeable and icon
        :param title: String
        :return: TopLevel item with title and resizeable defined
        """
        new_w = Toplevel()
        new_w.title(title)
        new_w.wm_iconbitmap('resources/banco.ico')
        new_w.resizable(1, 1)
        return new_w

    def dropdown_menu(self, window):
        '''
        Creates the dropdown menu with the name of the funds
        :param window: Tk or TopLevel instance
        :return: dropdown menu
        '''
        drop = ttk.Combobox(window, postcommand=lambda: self.set_combobox_values(drop),
                            values=[], state='readonly', style='my.TCombobox')
        return drop

    def set_combobox_values(self,combobox):
        """
        Sets the passed Combobox values to the funds
        :param combobox: ttk.Combobox object
        :return:
        """
        combobox['values'] = get_available_funds(self.DB)


if __name__ == '__main__':
    root = Tk()
    app = Fund(root)
    root.mainloop()

    '''
    def dropdown_menu(self, window):
        Creates the dropdown menu with the name of the funds
        :param window: Tk or TopLevel instance
        :return: dropdown menu
        clicked = StringVar()
        clicked.set('Selecciona un fondo de la lista')
        options = get_available_funds(self.DB)
        print(options)
        drop = OptionMenu(window, clicked, 'Hello')
        return drop
    '''