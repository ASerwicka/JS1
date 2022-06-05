import datetime
from tkinter import ttk, simpledialog, messagebox
from tkinter import *

import pandas as pd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data

EDUCATION = 'Wszystkie'
DEPENDENCY = 'Ogółem'


# TODO menu 6
# TODO ładne gui 9
# TODO dokumentacja 10


class Gui:

    def __init__(self):
        self.root = Tk()
        try:
            config_tmp = open('config.txt')
            config_tmp = config_tmp.readline().split(", ")
            x = int(config_tmp[0])
            y = int(config_tmp[1])
        except:
            y = 0
            x = 0

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.file_logs = open("logs.txt", "a", encoding="utf-8")
        self.menubar = None
        self.filemenu = None
        self.statusbar = tk.Label()
        self.button = Button()
        self.canvas = FigureCanvasTkAgg()
        self.picture_frame = LabelFrame()
        self.Var = None
        self.check_button = None
        self.sex = 0
        self.scrollbar = ttk.Scrollbar()
        self.tree = ttk.Treeview()
        self.Data = data.Data()
        # data from csv file
        self.data = self.Data.get_file()
        self.local_data = self.data
        # labels from csv file
        self.labels = self.Data.get_labels()
        self.local_labels = self.labels
        self.chosen_dependency = None
        self.chosen_education = None
        self.combo_dep = None
        self.combo_edu = None
        self.combo_sort = ttk.Combobox()
        self.root.geometry("900x500+%d+%d" % (x, y))
        self.upper_frame = LabelFrame(self.root, height=250, width=900)
        self.upper_frame.pack(fill=BOTH, expand=YES, side=TOP)
        self.upper_frame.pack_propagate(False)

        self.up_left_frame = LabelFrame(self.upper_frame, height=400, width=250)
        self.up_left_frame.pack(fill=BOTH, side=LEFT)
        self.up_left_frame.pack_propagate(False)

        self.up_right_frame = LabelFrame(self.upper_frame, height=400, width=650)
        self.up_right_frame.pack(fill=BOTH, expand=YES, side=RIGHT)
        self.up_right_frame.pack_propagate(False)

        self.bottom_frame = LabelFrame(self.root, height=100, width=900)
        self.bottom_frame.pack(fill=BOTH, expand=YES, side=BOTTOM)
        self.bottom_frame.pack_propagate(False)

        button = Button(self.up_left_frame, text="Reset", command=self.reset_action)
        button.pack(fill=X, side=BOTTOM)

        self.get_data_to_display()
        self.create_options()
        self.create_status()
        self.create_menu()

    def on_close(self):
        with open('config.txt', 'w') as configfile:
            configfile.write(str(self.root.winfo_rootx()) + ", " + str(self.root.winfo_rooty()))
        self.root.destroy()
        print("L")
        quit()

    def reset_action(self):
        self.view_data(None)
        self.picture_frame.destroy()

    def retrieve(self):
        self.chosen_education = self.combo_edu.get()
        self.chosen_dependency = self.combo_dep.get()
        self.sex = self.Var.get()
        self.get_data_to_display()

    def save_data(self):
        file = simpledialog.askstring("Input", "Podaj nazwę pliku", parent=self)
        df = pd.DataFrame(self.local_data, columns=self.local_labels)
        df.to_csv(file + '.csv', index=False)

    def choose_file_to_logs(self):
        file = simpledialog.askstring("Input", "Podaj nazwę pliku", parent=self)
        self.file_logs = file + '.txt'

    def write_logs(self, df):
        self.file_logs.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')
        if self.chosen_dependency is not None and self.chosen_education is not None:
            self.file_logs.write(str(self.chosen_education) + ", " + str(self.chosen_dependency) + ", podział na płeć: "
                                 + str(self.sex) + '\n')
            self.file_logs.write(pd.DataFrame(df).to_string() + '\n')

    def create_menu(self):
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Save selected data to file", command=self.save_data)
        self.filemenu.add_command(label="Choose file to save logs to...", command=self.choose_file_to_logs)

        self.filemenu.add_separator()

        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="Options", menu=self.filemenu)

        self.root['menu'] = self.menubar

    def create_status(self):
        self.statusbar = tk.Label(self.bottom_frame, text="Gotów...", anchor=W)
        self.statusbar.pack(fill=X, side=BOTTOM)

    def set_status(self, txt):
        self.statusbar["text"] = txt

    def create_options(self):
        temp = self.labels[1:]
        temp.append('Wszystkie', )
        self.combo_edu = ttk.Combobox(self.up_left_frame, values=temp)
        self.combo_edu.set("Pick an education")
        self.combo_edu.pack(fill=X, side=TOP)

        self.combo_dep = ttk.Combobox(self.up_left_frame, values=('Wiek', 'Ogółem'))
        self.combo_dep.set("Pick a dependency")
        self.combo_dep.pack(fill=X, side=TOP)

        self.Var = IntVar()

        self.check_button = Checkbutton(self.up_left_frame, text="Z podziałem na płeć", variable=self.Var)
        self.check_button.pack(fill=X, side=TOP)

        button = Button(self.up_left_frame, text="Submit", command=self.retrieve)
        button.pack(fill=X, side=TOP)

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

    def sort(self):
        sort_temp = self.combo_sort.get()
        try:
            self.view_data(pd.DataFrame(self.local_data, columns=self.local_labels).sort_values(str(sort_temp)))
        except:
            messagebox.showinfo(title=None, message="Proszę wybrać tryb sortowania")

    # require pandas dataframe
    def view_data(self, dataframe):
        self.set_status("Wykonano.")

        if dataframe is not None:
            self.local_labels = dataframe.columns.tolist()
            self.local_data = dataframe.values.tolist()
        else:
            self.local_labels = self.labels
            self.local_data = self.data

        self.tree.destroy()
        self.scrollbar.destroy()
        self.combo_sort.destroy()
        self.button.destroy()

        self.button = Button(self.up_left_frame, text="Submit", command=self.sort)
        self.button.pack(fill=X, side=BOTTOM)

        self.combo_sort = ttk.Combobox(self.up_left_frame, values=self.local_labels)
        self.combo_sort.set("Pick sorting")
        self.combo_sort.pack(fill=X, side=BOTTOM)

        self.tree = ttk.Treeview(self.bottom_frame, columns=self.local_labels, show='headings', selectmode='browse')
        self.scrollbar = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        count = 0
        for label in self.local_labels:
            if label.__eq__("Zasadnicze zawodowe"):
                self.tree.column(count, anchor=CENTER, width=110)
            else:
                self.tree.column(count, anchor=CENTER, width=80)
            self.tree.heading(count, text=label)
            count = count + 1

        for line in self.local_data:
            self.tree.insert('', 'end', values=line)

        self.tree.pack(expand=True, fill=BOTH, side=TOP)

        if dataframe is None:
            self.write_logs(pd.DataFrame(self.local_data, columns=self.local_labels))
        else:
            self.write_logs(dataframe)

    def view_graph(self, figure):
        self.picture_frame = LabelFrame(self.up_right_frame, height=250, width=250)
        self.picture_frame.pack(side=TOP)

        # TODO check if it possible to change size of one frame despite other frames
        # sizegrip = ttk.Sizegrip(self.picture_frame)
        # sizegrip.pack(side="right", anchor=SW)

        self.canvas = FigureCanvasTkAgg(figure, self.picture_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


if __name__ == '__main__':
    app = Gui()
    app.root.mainloop()
