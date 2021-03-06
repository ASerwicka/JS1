import datetime
from tkinter import ttk, simpledialog, messagebox
from tkinter import *

import pandas as pd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data


class Gui:
    def __init__(self):
        self.root = Tk()
        # odczytanie pliku z danymi o poprzednim położeniu okna
        try:
            config_tmp = open('config.txt')
            config_tmp = config_tmp.readline().split(", ")
            x = int(config_tmp[0])
            y = int(config_tmp[1])
        except:
            y = 0
            x = 0

        # wywołanie zapisania danych o położeniu okna po kliknięciu przycisku wyjścia
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # otwarcie pliku z logami
        self.file_logs = open("logs.txt", "a", encoding="utf-8")

        self.scrollbar = ttk.Scrollbar()
        self.tree = ttk.Treeview()
        self.Data = data.Data()
        self.statusbar = tk.Label()
        self.button = Button()
        self.canvas = FigureCanvasTkAgg()
        self.picture_frame = LabelFrame()
        self.combo_sort = ttk.Combobox()
        self.menubar = None
        self.filemenu = None
        self.Var = None
        self.check_button = None
        self.chosen_dependency = None
        self.chosen_education = None
        self.combo_dep = None
        self.combo_edu = None
        self.sex = 0

        # dane z odczytanego pliku z klasy Data
        self.data = self.Data.get_file()
        # dane na których będzie pracować funkcja wyświetlająca dane
        self.local_data = self.data
        # labele z odczytanego pliku z klasy Data
        self.labels = self.Data.get_labels()
        # labele na których pracować będzie funkcja wyświetlająca dane
        self.local_labels = self.labels

        # ustawienie położenia okna
        self.root.geometry("900x500+%d+%d" % (x, y))

        # tworzenie frame'ów
        self.upper_frame = LabelFrame(self.root, height=250, width=900, background='#2E2E2E', relief=FLAT)
        self.upper_frame.pack(fill=BOTH, expand=YES, side=TOP)
        self.upper_frame.pack_propagate(False)

        self.up_left_frame = LabelFrame(self.upper_frame, height=400, width=250, background='#2E2E2E', relief=FLAT)
        self.up_left_frame.pack(fill=BOTH, side=LEFT)
        self.up_left_frame.pack_propagate(False)

        self.up_right_frame = LabelFrame(self.upper_frame, height=400, width=650, background='white', relief=FLAT)
        self.up_right_frame.pack(fill=BOTH, expand=YES, side=RIGHT)
        self.up_right_frame.pack_propagate(False)

        self.bottom_frame = LabelFrame(self.root, height=100, width=900, background='#2E2E2E', relief=FLAT)
        self.bottom_frame.pack(fill=BOTH, expand=YES, side=BOTTOM)
        self.bottom_frame.pack_propagate(False)

        # przycisk do przywrócenia początkowych danych w oknie z danymi (dane bezpośrednio z pliku)
        button = Button(self.up_left_frame, text="Reset", command=self.reset_action, background='#585858',
                        activebackground='#2E2E2E', activeforeground="#E6E6E6", bd=0, fg="#E6E6E6", height=2)
        button.pack(fill=X, side=BOTTOM, pady=5)

        self.get_data_to_display()
        self.create_options()
        self.create_status()
        self.create_menu()

    # funkcja zapisująca położenie okna
    def on_close(self):
        with open('config.txt', 'w') as configfile:
            configfile.write(str(self.root.winfo_rootx()) + ", " + str(self.root.winfo_rooty()))
        self.root.destroy()
        print("L")
        quit()

    # funkcja wywołująca przywrówenie początkowych danych w oknie z danymi
    def reset_action(self):
        self.view_data(None)
        self.picture_frame.destroy()

    # funkcja która dane nam info o wybranych przez użytkownika wartościach
    def retrieve(self):
        self.chosen_education = self.combo_edu.get()
        self.chosen_dependency = self.combo_dep.get()
        self.sex = self.Var.get()
        self.get_data_to_display()

    # funkcja która zapisuje aktualnie wyświetlone dane do podanego pliku
    def save_data(self):
        file = simpledialog.askstring("Input", "Podaj nazwę pliku", parent=self.root)
        if file is not None and self.input_fine(file):
            df = pd.DataFrame(self.local_data, columns=self.local_labels)
            df.to_csv(file + '.csv', index=False)
        elif file is not None:
            messagebox.showinfo(title=None, message="Niepoprawna nazwa pliku")

    # funkcja która podmienia plik do zapisu logów na podany przez użytkownika
    def choose_file_to_logs(self):
        file = simpledialog.askstring("Input", "Podaj nazwę pliku", parent=self.root)
        if file is not None and self.input_fine(file):
            self.file_logs = open(file + '.txt', "a", encoding="utf-8")
        elif file is not None:
            messagebox.showinfo(title=None, message="Niepoprawna nazwa pliku")

    def input_fine(self, input):
        if str(input).isspace():
            return False
        else:
            for letter in input:
                if letter == " ":
                    return False
        return True

    # funkcja zapisująca logi do pliku
    def write_logs(self, df):
        self.file_logs.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')
        if self.chosen_dependency is not None and self.chosen_education is not None:
            self.file_logs.write(str(self.chosen_education) + ", " + str(self.chosen_dependency) + ", podział na płeć: "
                                 + str(self.sex) + '\n')
            self.file_logs.write(pd.DataFrame(df).to_string() + '\n')

    # funkcja tworząca menu
    def create_menu(self):
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0, background="#848484", relief=FLAT, activebackground="#848484")
        self.filemenu.add_command(label="Zapisz dane do pliku", command=self.save_data)
        self.filemenu.add_command(label="Wybierz plik do którego zapisywać logi...", command=self.choose_file_to_logs)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Wyjście", command=self.root.quit)
        self.menubar.add_cascade(label="Opcje", menu=self.filemenu)

        self.root['menu'] = self.menubar

    # funkcja tworząca status bar
    def create_status(self):
        self.statusbar = tk.Label(self.bottom_frame, text="Gotów...", anchor=W)
        self.statusbar.pack(fill=X, side=BOTTOM)

    # funkcja ustawiająca status bar
    def set_status(self, txt):
        self.statusbar["text"] = txt

    # funkcja tworząca opcje wyboru dla użytkownika
    def create_options(self):
        temp = self.labels[1:]
        temp.append('Wszystkie', )

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox',
                        background="#585858",
                        fieldbackground="#585858",
                        foreground="#E6E6E6",
                        darkcolor="#585858",
                        selectbackground="#585858",
                        lightcolor="#585858"
                        )
        self.combo_edu = ttk.Combobox(self.up_left_frame, values=temp, foreground="#E6E6E6", )
        self.combo_edu.set("Wybierz edukacje")
        self.combo_edu.pack(fill=X, side=TOP, pady=10)

        self.combo_dep = ttk.Combobox(self.up_left_frame, values=('Wiek', 'Ogółem'), foreground="#E6E6E6")
        self.combo_dep.set("Wybierz zależność")
        self.combo_dep.pack(fill=X, side=TOP, pady=10)

        self.Var = IntVar()

        self.check_button = Checkbutton(self.up_left_frame, text="Z podziałem na płeć", variable=self.Var,
                                        background="#2E2E2E", activebackground="#2E2E2E", activeforeground="#E6E6E6",
                                        fg="#E6E6E6", selectcolor="#585858")
        self.check_button.pack(fill=X, side=TOP, pady=5)

        button = Button(self.up_left_frame, text="Zatwierdź", command=self.retrieve, background='#585858',
                        activebackground='#2E2E2E', activeforeground="#E6E6E6", bd=0, fg="#E6E6E6")
        button.pack(fill=X, side=TOP, pady=5)

    # funkcja która pobiera dane z klasy Data na podstawie wyboru użytkownika i przesyła je dalej do wyświetlenia
    def get_data_to_display(self):
        self.picture_frame.destroy()

        if self.chosen_dependency is None and self.chosen_education is None:
            self.view_data(None)

        elif self.sex.__eq__(0):
            if self.chosen_dependency.__eq__('Ogółem'):
                self.view_data(self.Data.get_general_data_arg(self.chosen_education))
                if self.Data.get_general_diagram_arg(self.chosen_education) is not None:
                    self.view_graph(self.Data.get_general_diagram_arg(self.chosen_education))

            elif self.chosen_dependency.__eq__('Wiek'):
                self.view_data(self.Data.get_age_data_arg(self.chosen_education))
                self.view_graph(self.Data.get_age_diagram_arg(self.chosen_education))
        else:
            if self.chosen_dependency.__eq__('Ogółem'):
                self.view_data(self.Data.get_general_data_sex_arg(self.chosen_education))
                if self.Data.get_general_sex_diagram_arg(self.chosen_education) is not None:
                    self.view_graph(self.Data.get_general_sex_diagram_arg(self.chosen_education))

            elif self.chosen_dependency.__eq__('Wiek'):
                self.view_data(self.Data.get_age_data_sex_arg(self.chosen_education))
                if self.Data.get_age_sex_diagram_arg(self.chosen_education) is not None:
                    self.view_graph(self.Data.get_age_sex_diagram_arg(self.chosen_education))

    # funkcja sortująca wyświetlone dane
    def sort(self):
        sort_temp = self.combo_sort.get()
        try:
            self.view_data(pd.DataFrame(self.local_data, columns=self.local_labels).sort_values(str(sort_temp)))
        except:
            messagebox.showinfo(title=None, message="Proszę wybrać tryb sortowania")

    # funkcja wyświetlająca dane w oknie, przyjmuje DataFrame w argumencie
    def view_data(self, dataframe):
        self.set_status("Wykonano.")

        # jeśli do funkcji nie został podany DataFrame to funkcja przyjmuje defaultowe dane
        if dataframe is not None:
            self.local_labels = dataframe.columns.tolist()
            self.local_data = dataframe.values.tolist()
        else:
            self.local_labels = self.labels
            self.local_data = self.data

        # zniszczenie poprzednich danych
        self.tree.destroy()
        self.scrollbar.destroy()
        self.combo_sort.destroy()
        self.button.destroy()

        # stworzenie pola wyboru oraz przycisku zatwierdzenia do sortowania danych
        self.button = Button(self.up_left_frame, text="Zatwierdź", command=self.sort, background='#585858',
                             activebackground='#2E2E2E', activeforeground="#E6E6E6", bd=0, fg="#E6E6E6")
        self.button.pack(fill=X, side=BOTTOM, pady=5)

        self.combo_sort = ttk.Combobox(self.up_left_frame, values=self.local_labels, background='#585858')
        self.combo_sort.set("Wybierz sortowanie")
        self.combo_sort.pack(fill=X, side=BOTTOM, pady=5)

        # stworzenie pola do wyświetlenia danych
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview", background="#A4A4A4",
                        fieldbackground="#A4A4A4", foreground="#151515")

        self.tree = ttk.Treeview(self.bottom_frame, columns=self.local_labels, show='headings', selectmode='browse')
        self.scrollbar = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # stworzenie kolumn
        count = 0
        for label in self.local_labels:
            if label.__eq__("Zasadnicze zawodowe"):
                self.tree.column(count, anchor=CENTER, width=110)
            else:
                self.tree.column(count, anchor=CENTER, width=80)
            self.tree.heading(count, text=label)
            count = count + 1

        # dodanie danych
        for line in self.local_data:
            self.tree.insert('', 'end', values=line)

        self.tree.pack(expand=True, fill=BOTH, side=TOP)

        # zapisanie wyświetlonych danych do logów
        if dataframe is None:
            self.write_logs(pd.DataFrame(self.local_data, columns=self.local_labels))
        else:
            self.write_logs(dataframe)

    # funkcja wyświetlająca graf, dostaje w argumencie figure
    def view_graph(self, figure):
        self.picture_frame = LabelFrame(self.up_right_frame, height=250, width=250)
        self.picture_frame.pack(side=TOP)

        self.canvas = FigureCanvasTkAgg(figure, self.picture_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


if __name__ == '__main__':
    app = Gui()
    app.root.mainloop()
