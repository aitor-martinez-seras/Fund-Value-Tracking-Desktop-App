from utils import *
from plots import *
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkcalendar import DateEntry


class Fund():
    """
    Base class where all the GUI is going to be implemented
    """
    DB = DATABASE_PATH
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
        deposit_frame.pack(pady=10, padx=10)
        #deposit_frame.grid(row=0, column=0, rowspan=3,columnspan=self.COLUMNSPAN, padx=self.FRAME_PADX, pady=self.FRAME_PADY, sticky=W+E)
        # Add deposit button
        self.add_deposit_button = ttk.Button(deposit_frame,text='Añadir aporte', style='my.TButton', command=self.add_deposit_window)
        self.add_deposit_button.grid(row=0, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=20)
        # Edit deposit button
        self.edit_deposit_button = ttk.Button(deposit_frame, text='Editar/eliminar aportes realizados',
                                              style='my.TButton', command=self.edit_deposit_window)
        self.edit_deposit_button.grid(row=1, column=0, columnspan=self.COLUMNSPAN, sticky=W + E, padx=20, ipadx=20)
        # Delete deposit button

        # Frame for operating with the 'Visualizations'
        visu_frame = LabelFrame(self.main_window, text='Opciones de visualizacion', font=self.LABEL_FONT, labelanchor=N)
        visu_frame.pack(pady=10)
        # Add deposit button
        self.profits_button = ttk.Button(visu_frame, text='Rentabilidad por aporte', style='my.TButton',
                                         command=self.profits_per_deposit_window)
        self.profits_button.grid(row=0, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=25)
        # Edit deposit button
        self.profits_per_fund_button = ttk.Button(visu_frame, text='Rentabilidad total por fondo', style='my.TButton',
                                                  command=self.profits_per_fund_window)
        self.profits_per_fund_button.grid(row=1, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=25)

        # Frame for operating with 'Funds'
        fund_frame = LabelFrame(self.main_window, text='Operaciones con los fondos', font=self.LABEL_FONT, labelanchor=N)
        fund_frame.pack(pady=10)
        # Add fund button
        self.add_fund_button = ttk.Button(fund_frame, text='Añadir nuevo fondo', style='my.TButton',
                                          command=self.add_fund_window)
        self.add_fund_button.grid(row=0, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20, ipadx=25)
        # Edit fund button
        self.edit_fund_button = ttk.Button(fund_frame, text='Editar nombre del fondo', style='my.TButton',
                                           command=self.edit_fund_window)
        self.edit_fund_button.grid(row=1, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20)
        # Delete fund button
        self.del_fund_button = ttk.Button(fund_frame, text='Eliminar fondo', style='my.TButton',
                                          command=self.delete_fund_window)
        self.del_fund_button.grid(row=2, column=0, columnspan=self.COLUMNSPAN, sticky=W+E, padx=20)

    # Functions of the deposit frame #

    # Functions of each window
    def add_deposit_window(self):
        """
        Creates the window to add a deposit to the fund
        """
        window = self.new_window('Añadir aporte a fondo')
        # Date entry
        date_label = Label(window, text='Introduzca la fecha: ', font=self.LABEL_FONT)
        date_label.grid(row=0, column=0, sticky=W, padx=self.ENTRY_PADX)
        date_entry = DateEntry(window, selectmode='day', date_pattern='yyyy-mm-dd', state='readonly',
                               width=self.DATE_WIDTH)
        date_entry.grid(row=0, column=1, sticky=W, padx=self.ENTRY_PADX)
        # Dropdown menu
        drop_label = Label(window, text='Seleccione el fondo al que ingresar: ', font=self.LABEL_FONT)
        drop_label.grid(row=1, column=0, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        fund_entry = self.dropdown_menu(window)
        fund_entry.grid(row=1, column=1, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        # Desposit entry
        deposit_label = Label(window, text='Introduzca la cantidad ingresada: ', font=self.LABEL_FONT)
        deposit_label.grid(row=2, column=0, padx=self.ENTRY_PADX, sticky=W)
        deposit_entry = Entry(window, width=self.ENTRY_WIDTH)
        deposit_entry.grid(row=2, column=1, padx=self.ENTRY_PADX, sticky=W)
        # Number of shares entry
        shares_label = Label(window, text='Introduzca el nº de participaciones: ', font=self.LABEL_FONT)
        shares_label.grid(row=3, column=0, padx=self.ENTRY_PADX, sticky=W)
        shares_entry = Entry(window, width=self.ENTRY_WIDTH)
        shares_entry.grid(row=3, column=1, padx=self.ENTRY_PADX, sticky=W)
        # Save button
        create_button = ttk.Button(window, text='Añadir aporte', style='my.TButton',
                                   command=lambda: self.add_deposit(window, date_entry, fund_entry, deposit_entry,shares_entry))
        create_button.grid(row=4, columnspan=2, ipadx=50, pady=20)

    def add_deposit(self,window,date_entry, fund_entry, deposit_entry, shares_entry):
        mensaje = Label(window,text='')
        mensaje.grid(row=5, columnspan=2, sticky=W + E)
        # To handle the float conversion error
        try:
            date, fund, deposit, shares = date_entry.get(), fund_entry.get(), float(deposit_entry.get()), float(shares_entry.get())
            date = parse_date_to_datetime(date)
        except ValueError:
            mensaje['fg'] = 'red'
            mensaje['text'] = 'Datos introducidos incorrectos, el aporte no ha sido creado'
            deposit_entry.delete(0, END)
            shares_entry.delete(0, END)
            return
        # To check whether the inputs can be inserted into the database
        if validate_date(date) and validate_name(fund) and validate_number(deposit) and validate_number(shares):
            create_deposit(self.DB, {'date': date, 'fund': fund, 'deposit':deposit, 'shares':shares})
            mensaje['fg'] = 'green'
            mensaje['text'] = 'Aporte creado correctamente, la ventana se va a cerrar automaticamente'
            window.after(3000, window.destroy)
        else:
            mensaje['fg'] = 'red'
            mensaje['text'] = 'Datos introducidos incorrectos, el aporte no ha sido creado'
            deposit_entry.delete(0, END)
            shares_entry.delete(0, END)

    def edit_deposit_window(self):
        window = self.new_window('Editar aporte a fondo')
        window.geometry('650x450')
        # Frame to select the fund and refresh the view
        fund_frame = Frame(window)
        #fund_frame.grid(row=0, column=0, columnspan=2,padx=5, pady=5)
        fund_frame.pack(pady=5)
        # Dropdown menu to select the fund to be visualized
        drop_label = Label(fund_frame, text='Seleccione el fondo al que ingresar: ', font=self.LABEL_FONT)
        drop_label.grid(row=0, column=0, padx=self.ENTRY_PADX, sticky=W)
        fund_entry = self.dropdown_menu(fund_frame)
        fund_entry.grid(row=0, column=1, padx=self.ENTRY_PADX, sticky=W)

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
        share_l = Label(boxes_frame, text=DB_COLUMNS[3])
        share_l.grid(row=0, column=3)
        value_l = Label(boxes_frame, text=DB_COLUMNS[4])
        value_l.grid(row=0, column=4)
        # Boxes
        id_string = StringVar()
        id_box = Entry(boxes_frame,  textvariable=id_string, state=DISABLED)
        id_box.grid(row=1, column=0)
        date_box = DateEntry(boxes_frame, selectmode='day', date_pattern='yyyy-mm-dd',
                             width=self.DATE_WIDTH)
        date_box.grid(row=1, column=1)
        self.clear_boxes(date_box)
        deposit_box = Entry(boxes_frame)
        deposit_box.grid(row=1, column=2)
        share_box = Entry(boxes_frame)
        share_box.grid(row=1, column=3)
        value_box = Entry(boxes_frame)
        value_box.grid(row=1, column=4)

        # Buttons section
        buttons_frame = Frame(window)
        buttons_frame.pack(pady=5)

        update_button = ttk.Button(
            buttons_frame, text='Actualizar datos', style='my.TButton',
            command= lambda: self.update_record(window, fund_entry.get(), table_list,
                                                id_string, date_box, deposit_box, share_box, value_box, message)
        )
        update_button.grid(row=0, column=0, padx=20)

        clear_button = ttk.Button(
            buttons_frame, text='Limpiar campos', style='my.TButton',
            command=lambda: self.clear_boxes(id_string, date_box, deposit_box, share_box, value_box)
        )
        clear_button.grid(row=0, column=1, padx=20)
        
        delete_button = ttk.Button(
            buttons_frame, text='Borrar registro seleccionado', style='my.TButton',
            command=lambda: self.delete_record(window, fund_entry.get(), table_list,
                                                id_string, date_box, deposit_box, share_box, value_box, message)
        )
        delete_button.grid(row=0, column=2, padx=20)
        # Message
        message_frame = Frame(window)
        message_frame.pack(pady=10)
        message = Label(message_frame, text='')
        message.grid(row=0, column=0, pady=5)

        # Binds
        # Bind the dropdown menu to refresh the table everytime its value changes
        fund_entry.bind(
            "<<ComboboxSelected>>",
            lambda event, args=(fund_entry, table_list): self.on_combo_click(event, args)
        )
        # Bind the double click to the select record function
        table_list.bind('<Double-1>',
                        lambda event, args=(table_list, id_string, date_box,
                                            deposit_box, share_box, value_box):
                        self.select_record(event, args))

    def select_record(self, event, args):
        """
        Grabs the info from the double-clicked register of the table and puts it in the corresponding boxes of the
        edit/delete window
        """
        table, id_string, date_box, deposit_box, share_box, value_box = args
        # Clear boxes
        self.clear_boxes(id_string, date_box, deposit_box, share_box, value_box)
        # Grab record number
        self.selected = table.selection()
        # Grab record values
        values = table.item(self.selected, 'values')
        id_string.set(values[0])
        date_box.set_date(values[1])
        deposit_box.insert(0, values[2])
        share_box.insert(0, values[3])
        value_box.insert(0, values[4])

    def on_combo_click(self, event, args):
        """
        When selecting the fund from the ComboBox, this function prints the table with the fund info
        """
        fund_entry, table_frame = args
        # Call the function that prints the deposits of the selected fund
        self.visualize_table(fund_entry.get(),table_frame)

    def update_record(self, window: Toplevel, fund, table: ttk.Treeview, id_string, date_box,
                      deposit_box, share_box, value_box, message):
        """

        :param message:
        :param table:
        :param id_box:
        :param date_box:
        :param deposit_box:
        :param share_box:
        :param value_box:
        :return:
        """
        # Ensure data is in the correct format
        try:
            id, date, deposit, shares, value = id_string.get(), date_box.get(), float(deposit_box.get()), \
                                                       float(share_box.get()), float(value_box.get())
            date = parse_date_to_datetime(date)
        except ValueError:
            message['fg'] = 'red'
            message['text'] = 'Datos introducidos incorrectos, el aporte no ha sido editado'
            # Clear the message after 1 second
            window.after(2000, self.delete_message, message)
            return
        # To check whether the inputs can be inserted into the database
        if validate_date(date) and validate_name(fund) and validate_number(deposit) and validate_number(shares):
            edit_deposit(self.DB, {'fund': fund, 'id': id, 'date': date,
                                   'deposit': deposit, 'shares': shares, 'value': value})
            message['fg'] = 'green'
            message['text'] = 'Aporte editado correctamente'
            correct_data = True # Flag to know if the data was correctly inserted in the database
        else:
            message['fg'] = 'red'
            message['text'] = 'Datos introducidos incorrectos, el aporte no ha sido editado'
            correct_data = False # If data is not validated correctly, this flag makes the data not update in the table

        # Clear the message after 1 second
        window.after(2000, self.delete_message, message)

        # Write new items to the table if they were correctly updated. For performance reasons, instead of consulting
        # the data on the database after the update of the register and printing all the table again, we simply update
        # the data on the table, using the flag
        if correct_data:
            table.item(self.selected, text='', values=(id, date, deposit, shares, value))

        # Clear the boxes after 1 second
        window.after(1000, self.clear_boxes, id_string, date_box, deposit_box, share_box, value_box)

    def delete_record(self, window: Toplevel, fund, table: ttk.Treeview, id_string: StringVar, date_box,
                      deposit_box, share_box, value_box, message):
        try:
            # Assert id is not empty
            assert len(id_string.get()) != 0
            # Delete the record from the DB
            record_deleted = delete_record_from_db(self.DB, fund, id_string.get())
            self.visualize_table(fund, table)
        except AssertionError:
            record_deleted = False
        # Clear all the boxes after a delay
        self.clear_boxes(id_string, date_box, deposit_box, share_box, value_box)
        if record_deleted:
            message['fg'] = 'green'
            message['text'] = 'Aporte eliminado correctamente'
        else:
            message['fg'] = 'red'
            message['text'] = 'Datos introducidos incorrectos, el aporte no ha sido eliminado'

    def visualize_table(self, fund_name, table_list: ttk.Treeview, dates=None):
        """
        Function that prints the values of a fund in the table
        """
        # Delete previous entries
        self.clear_table(table_list)
        # Add the values to the table
        deposits = get_deposits_of_a_fund(self.DB, fund_name, dates='All')
        for index, deposit in enumerate(deposits):
            table_list.insert(parent='', index='end', iid=index,
                              values=self.round_numbers_to_n_decimals(deposit, 3))

    @staticmethod
    def round_numbers_to_n_decimals(deposit_tuple, n):
        deposit = list(deposit_tuple)
        deposit[2:] = [round(float(item), n) for item in deposit[2:]]
        return deposit

    def initialize_table(self, table: ttk.Treeview):
        """
        Fills the table with the Columns and headers
        """
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

    @staticmethod
    def delete_message(message):
        message['text'] = ''

    @staticmethod
    def clear_boxes(*args):
        for item in args:
            try:
                item.delete(0, END)
            except AttributeError:
                item.set('')

    @staticmethod
    def clear_table(table: ttk.Treeview):
        for item in table.get_children():
            table.delete(item)

    # Functions of the visualize frame #

    def profits_per_deposit_window(self):
        # Create the window
        window = self.new_window('Visualización de rentabilidades')
        # Frame for the options of the visualization
        options_frame = Frame(window)
        options_frame.pack(padx=20, pady=5)
        # Fund selection
        fund_label = Label(options_frame, text='Seleccione el fondo:', font=self.LABEL_FONT)
        fund_label.grid(row=0, column=0, padx=5, sticky=E)
        # The last argument of the call is to offer the option to visualize the overall profits
        fund_entry = self.dropdown_menu(options_frame)
        fund_entry.grid(row=0, column=1, padx=self.ENTRY_PADX, sticky=W)
        funds = get_available_funds(self.DB)

        # Init date
        init_date_label = Label(options_frame, text='Fecha inicial:', font=self.LABEL_FONT)
        init_date_label.grid(row=1, column=0, padx=5, sticky=E)
        init_date_entry = DateEntry(options_frame, selectmode='day', date_pattern='yyyy-mm-dd', state='readonly',
                               width=self.DATE_WIDTH)
        init_date_entry.grid(row=1, column=1, sticky=W, padx=self.ENTRY_PADX)
        # End date
        end_date_label = Label(options_frame, text='Fecha final:', font=self.LABEL_FONT)
        end_date_label.grid(row=2, column=0, padx=5, sticky=E)
        end_date_entry = DateEntry(options_frame, selectmode='day', date_pattern='yyyy-mm-dd', state='readonly',
                                    width=self.DATE_WIDTH)
        end_date_entry.grid(row=2, column=1, sticky=W, padx=self.ENTRY_PADX)

        # Options for the plots
        # Percent
        percent_label = Label(options_frame, text='Forma de representación:', font=self.LABEL_FONT)
        percent_label.grid(row=0, column=2, padx=5, sticky=E)
        percent_entry = ttk.Combobox(options_frame, values=OPTIONS_FOR_PERCENT, state='readonly', style='my.TCombobox')
        percent_entry.grid(row=0, column=3, padx=5, ipadx=12, sticky=E)
        percent_entry.current(0)
        # Spacing
        spacing_label = Label(options_frame, text='Espaciado:', font=self.LABEL_FONT)
        spacing_label.grid(row=1, column=2, padx=5, sticky=E)
        spacing_entry = ttk.Combobox(options_frame, values=OPTIONS_FOR_SPACING, state='readonly', style='my.TCombobox')
        spacing_entry.grid(row=1, column=3, padx=5, ipadx=12, sticky=E)
        spacing_entry.current(0)

        # Frame for the message
        message_frame = Frame(window)
        message_frame.pack(pady=2)
        message = Label(message_frame, text='')
        message.grid(row=0, column=0)

        # Frame for plotting
        plot_frame = Frame(window)
        plot_frame.pack(padx=20, pady=5)
        # Figure, axes and toolbar objects creation for plotting
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.
        toolbar = NavigationToolbar2Tk(canvas, plot_frame, pack_toolbar=False)

        # Update plot button
        plot_button = ttk.Button(options_frame, text='Visualizar', style='my.TButton',
                                   command=lambda: self.plot_figure(
                                                   fig, ax, canvas, toolbar,
                                                   fund_entry.get(),
                                                   dates={'from': init_date_entry.get(),
                                                          'to': end_date_entry.get()},
                                                   message=message,
                                                   option='Per deposit',
                                                   visualization_options ={'percentage': percent_entry.get(),
                                                                           'spacing': spacing_entry.get()}
                                                   )
                                 )
        plot_button.grid(row=3, columnspan=4, ipadx=80, pady=5)

    def plot_figure(self, fig: plt.Figure, ax, canvas: FigureCanvasTkAgg, toolbar: NavigationToolbar2Tk,
                    fund_name: str or list, dates: dict, message: Label, option: str, visualization_options: dict):
        """
        Implements the logic to decide the figure that must be plot in each case and to prevent plotting anything when
        there is no data for the plot. If True obtained from the functions responsible for the plots, sends the canvas
        and the toolbar to a function that shows it in the corresponding window. If a False or a list is returned from
        these functions, means that plot could not be completed
        """
        # Plotted variable will contain True if the plot can be done, False otherwise
        if fund_name == "":
            message['fg'] = 'red'
            message['text'] = 'No se ha seleccionado un fondo existente'
            return
        else:
            message['text'] = ""
        # Check the type of plot to paint
        if option == 'Per deposit':
            plotted = plot_profits_per_deposit(self.DB, fig, ax, fund_name, dates, visualization_options)
        elif option == 'Fund_value':
            plotted = plot_profits_per_fund(self.DB, fig, ax, fund_name, dates, visualization_options)
        else:
            message['fg'] = 'red'
            message['text'] = 'No se ha seleccionado una opción de visualización existente'
            plotted = False

        if plotted is True:
            create_plot(canvas, toolbar)
        elif isinstance(plotted, list) and len(plotted) != 0:
            create_plot(canvas, toolbar)
            message['fg'] = 'orange'
            message['text'] = f'No existen datos para las fechas seleccionadas de los siguientes fondos: ' \
                              f' {list_to_string(plotted)}'
        else:
            message['fg'] = 'red'
            message['text'] = f'No existen datos para las fechas seleccionadas de los siguientes fondos: ' \
                              f' {list_to_string(plotted)}'

    def profits_per_fund_window(self):
        # Create the window
        window = self.new_window('Visualización de rentabilidad de cada fondo')
        # Frame for the options of the visualization
        options_frame = Frame(window)
        options_frame.pack(padx=20, pady=5)
        # Fund selection
        fund_label = Label(options_frame, text='Seleccione los fondos que quiere visualizar:', font=self.LABEL_FONT)
        fund_label.grid(row=0, column=0, padx=5, sticky=E)
        # The last argument of the call is to offer the option to visualize the overall profits
        self.funds_to_plot = []
        fund_selection_button = ttk.Button(options_frame, text='Selección de fondos', style='my.TButton',
                                           command=lambda: self.fund_selection(message))
        fund_selection_button.grid(row=0, column=1, padx=self.ENTRY_PADX, sticky=W)

        # Options for the plots
        # Percent
        percent_label = Label(options_frame, text='Forma de representación:', font=self.LABEL_FONT)
        percent_label.grid(row=1, column=0, padx=5, sticky=E)
        percent_entry = ttk.Combobox(options_frame, values=OPTIONS_FOR_PERCENT, state='readonly', style='my.TCombobox')
        percent_entry.grid(row=1, column=1, padx=self.ENTRY_PADX, sticky=W)
        percent_entry.current(0)

        # Init date
        init_date_label = Label(options_frame, text='Fecha inicial:', font=self.LABEL_FONT)
        init_date_label.grid(row=2, column=0, padx=5, sticky=E)
        init_date_entry = DateEntry(options_frame, selectmode='day', date_pattern='yyyy-mm-dd', state='readonly',
                               width=self.DATE_WIDTH)
        init_date_entry.grid(row=2, column=1, sticky=W, padx=self.ENTRY_PADX)
        # End date
        end_date_label = Label(options_frame, text='Fecha final:', font=self.LABEL_FONT)
        end_date_label.grid(row=3, column=0, padx=5, sticky=E)
        end_date_entry = DateEntry(options_frame, selectmode='day', date_pattern='yyyy-mm-dd', state='readonly',
                                    width=self.DATE_WIDTH)
        end_date_entry.grid(row=3, column=1, sticky=W, padx=self.ENTRY_PADX)

        # Frame for the message
        message_frame = Frame(window)
        message_frame.pack(pady=2)
        message = Label(message_frame, text='')
        message.grid(row=0, column=0)

        # Frame for plotting
        plot_frame = Frame(window)
        plot_frame.pack(padx=20, pady=5)
        # Figure, axes and toolbar objects creation for plotting
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)  # A tk.DrawingArea.
        toolbar = NavigationToolbar2Tk(canvas, plot_frame, pack_toolbar=False)

        # Update plot button
        plot_button = ttk.Button(options_frame, text='Visualizar', style='my.TButton',
                                 command=lambda: self.plot_figure(
                                                   fig, ax, canvas, toolbar,
                                                   self.funds_to_plot,
                                                   dates={'from': init_date_entry.get(),
                                                          'to': end_date_entry.get()},
                                                   message=message,
                                                   option='Fund_value',
                                                   visualization_options ={'percentage': percent_entry.get()}
                                                   )
                                 )
        plot_button.grid(row=4, columnspan=2, ipadx=80, pady=5)

    def fund_selection(self, message):
        # Create new window
        window = self.new_window('Seleccione fondos a visualizar')
        # Initialize list that will move info between functions
        list_of_checkbuttons = []
        list_of_vars = []
        # Frame for the checkbuttons
        frame_checkbuttons = Frame(window)
        frame_checkbuttons.grid(row=0, column=0, columnspan=2, sticky='WE', padx=20, pady=15)
        # Creation of the checkbuttons
        self.create_checkbuttons_from_list(frame_checkbuttons, get_available_funds(self.DB),
                                           list_of_checkbuttons, list_of_vars)
        # Frame for the save options button
        frame_save_button = Frame(window)
        frame_save_button.grid(row=1, column=0, columnspan=2, sticky='WE', padx=20, pady=15)
        save_button = ttk.Button(frame_save_button, text='Guardar selección', style='my.TButton',
                                 command=lambda : self.save_fund_selection_options(list_of_checkbuttons,
                                                                                   list_of_vars,
                                                                                   window,
                                                                                   message)
                                 )
        save_button.pack(anchor='center')

    def create_checkbuttons_from_list(self, frame: Frame, fund_list: list,
                                      list_of_checkbuttons: list, list_of_vars: list):
        for index, item in enumerate(fund_list):
            var = tkinter.IntVar()
            var.set(1)
            list_of_checkbuttons.append(ttk.Checkbutton(frame, text=item, variable=var))
            list_of_checkbuttons[-1].grid(row=index // 2, column=index % 2, padx=5, pady=5, ipadx=15, sticky='WE')
            list_of_vars.append(var)

    def save_fund_selection_options(self, list_of_checkbuttons: list, list_of_vars: list, window: Toplevel,
                                    message: Label):
        """
        Save the funds selection to an attribute of the object to make it available to the other
        widows (the other functions)
        """
        self.funds_to_plot = []
        for index, intvar in enumerate(list_of_vars):
            if intvar.get() == 1:
                self.funds_to_plot.append(list_of_checkbuttons[index].cget('text'))
        print(self.funds_to_plot)
        window.destroy()
        message['fg'] = 'black'
        message['text'] = f'Fondos seleccionados: {list_to_string(self.funds_to_plot)}'


    # Functions of the fund frame #

    def add_fund_window(self):
        """
        Creates the window for adding a Fund to the database
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
        window = self.new_window('Editar nombre a fondo')
        # Dropdown menu
        drop_label = Label(window, text='Seleccione el fondo: ', font=self.LABEL_FONT)
        drop_label.grid(row=0, column=0, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        fund_entry = self.dropdown_menu(window)
        fund_entry.grid(row=0, column=1, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        # New name entry
        name_label = Label(window, text='Introduzca el nuevo nombre: ', font=self.LABEL_FONT)
        name_label.grid(row=2, column=0, padx=self.ENTRY_PADX, sticky=W)
        name_entry = Entry(window, width=self.ENTRY_WIDTH)
        name_entry.grid(row=2, column=1, padx=self.ENTRY_PADX, sticky=W)
        # Save button
        create_button = ttk.Button(window, text='Validar nuevo nombre', style='my.TButton',
                                   command=lambda: self.edit_fund(window, fund_entry, name_entry))
        create_button.grid(row=3, columnspan=2, ipadx=50, pady=20)

    def edit_fund(self, window, fund_entry: ttk.Combobox, name_entry: Entry):
        '''
        Wraps the logic of the edit fund window
        '''
        mensaje = Label(window, text='')
        mensaje.grid(row=5, columnspan=2, sticky=W + E)
        old_name, new_name = fund_entry.get(), name_entry.get()
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
        fund_entry = self.dropdown_menu(window)
        fund_entry.grid(row=0, column=1, columnspan=2, padx=self.ENTRY_PADX, sticky=W)
        # Save button
        create_button = ttk.Button(window, text='Validar nuevo nombre', style='my.TButton',
                                   command=lambda: self.delete_fund(window, fund_entry))
        create_button.grid(row=2, columnspan=2, ipadx=80, pady=20, padx=50, sticky=W+E)

    def delete_fund(self, window, fund_entry: ttk.Combobox):
        mensaje = Label(window, text='')
        mensaje.grid(row=3, columnspan=2, sticky=W + E)
        fund_name = fund_entry.get()
        delete_fund_from_db(self.DB, fund_name)
        mensaje['fg'] = 'green'
        mensaje['text'] = 'Fondo eliminado correctamente, la ventana se va a cerrar automaticamente'
        window.after(3000, window.destroy)

    # Auxiliary functions #

    def new_window(self, title='') -> Toplevel:
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

    def dropdown_menu(self, window, *args) -> ttk.Combobox:
        '''
        Creates the dropdown menu with the name of the funds
        :param window: Tk or TopLevel instance
        :return: dropdown menu
        '''
        drop = ttk.Combobox(window, postcommand=lambda: self.set_combobox_values_as_funds(drop, args),
                            values=[], state='readonly', style='my.TCombobox')
        return drop

    def set_combobox_values_as_funds(self, combobox: ttk.Combobox, args):
        """
        Sets the passed Combobox values to the funds
        :param args: str or list of strings with values that we want to add to the ComboBox dropdown menu
        """
        combobox['values'] = list(args) + get_available_funds(self.DB)


if __name__ == '__main__':
    # Creates the .db file in case it does not exist in the DATABASE_PATH of the constants.py file
    create_db_file()
    root = Tk()
    app = Fund(root)
    root.mainloop()
