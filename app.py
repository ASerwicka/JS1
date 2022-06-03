from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data

EDUCATION = 'Wszystkie'
DEPENDENCY = 'Ogółem'


class Gui(Tk):
    def __init__(self):
        super().__init__()
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
        self.geometry("900x500")
        self.upper_frame = LabelFrame(self, height=250, width=900)
        self.upper_frame.pack(fill=BOTH, expand=YES, side=TOP)
        self.upper_frame.pack_propagate(False)

        self.up_left_frame = LabelFrame(self.upper_frame, height=400, width=250)
        self.up_left_frame.pack(fill=BOTH, side=LEFT)
        self.up_left_frame.pack_propagate(False)

        self.up_right_frame = LabelFrame(self.upper_frame, height=400, width=650)
        self.up_right_frame.pack(fill=BOTH, expand=YES, side=RIGHT)
        self.up_right_frame.pack_propagate(False)

        self.bottom_frame = LabelFrame(self, height=100, width=900)
        self.bottom_frame.pack(fill=BOTH, expand=YES, side=BOTTOM)
        self.bottom_frame.pack_propagate(False)

    def retrieve(self):
        self.chosen_education = self.combo_edu.get()
        self.chosen_dependency = self.combo_dep.get()

    def create_combobox_education(self):
        temp = self.labels[1:]
        temp.append('Wszystkie',)
        self.combo_edu = ttk.Combobox(self.up_left_frame, values=temp)
        self.combo_edu.set("Pick an education")
        self.combo_edu.pack(fill=X)

        self.combo_dep = ttk.Combobox(self.up_left_frame, values=('Wiek', 'Ogółem'))
        self.combo_dep.set("Pick a dependency")
        self.combo_dep.pack(fill=X)

        button = Button(self.up_left_frame, text="Submit", command=self.retrieve)
        button.pack(fill=X)

    def get_data_to_display(self):
        if self.chosen_dependency is None and self.chosen_education is None:
            self.view_data(None)
        elif self.chosen_dependency.__eq__('Ogółem') and self.chosen_education.__eq__('Wszystkie'):
            self.view_data(self.Data.get_general_data())
        elif self.chosen_dependency.__eq__('Wiek'):
            if self.chosen_education.__eq__('Ogółem'):
                #TODO
                self.view_data(None)
            elif self.chosen_education.__eq__('Podstawowe'):
                # TODO
                self.view_data(None)
            elif self.chosen_education.__eq__('Średnie'):
                # TODO
                self.view_data(None)
            elif self.chosen_education.__eq__('Policealne'):
                # TODO
                self.view_data(None)
            elif self.chosen_education.__eq__('Zasadnicze zawodowe'):
                # TODO
                self.view_data(None)
            elif self.chosen_education.__eq__('Gimnazjalne'):
                # TODO
                self.view_data(None)
            elif self.chosen_education.__eq__('Wyższe'):
                # TODO
                self.view_data(None)

    # require pandas dataframe
    def view_data(self, dataframe):
        if dataframe is not None:
            self.local_labels = dataframe.columns.tolist()
            self.local_data = dataframe.values.tolist()
        else:
            self.local_labels = self.labels
            self.local_data = self.data
        tree = ttk.Treeview(self.bottom_frame, columns=self.local_labels, show='headings', selectmode='browse')
        scrollbar = ttk.Scrollbar(self.bottom_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)

        count = 0
        for label in self.local_labels:
            tree.column(count, anchor=CENTER, width=110)
            tree.heading(count, text=label)
            count = count + 1

        for line in self.local_data:
            tree.insert('', 'end', values=line)

        tree.pack(expand=True, fill=BOTH)

    def view_graph(self):
        picture_frame = LabelFrame(self.up_right_frame, bg="blue", height=250, width=250)
        picture_frame.pack(side=TOP, expand=False)

        sizegrip = ttk.Sizegrip(picture_frame)
        sizegrip.pack(side="right", anchor=SW)

        figure, ax = self.Data.education_general_diagram()
        canvas = FigureCanvasTkAgg(figure, picture_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


if __name__ == '__main__':
    app = Gui()
    app.get_data_to_display()
    app.create_combobox_education()
    app.mainloop()
