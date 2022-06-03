import pandas as pd
import matplotlib.pyplot as plt

#data = pd.read_csv('Dane_2011_ogólne.csv', sep=';')
#del data['Policealne']
# labels
#labels = data.columns.tolist()



def format_number(data_value, indx):
    if data_value >= 1000000:
        formatter = '{:1.1f}M'.format(data_value * 0.000001)
    else:
        formatter = '{:1.0f}K'.format(data_value * 0.001)
    return formatter


class Data:
    def __init__(self):
        # for displaying
        self.file = open("Dane_2011_ogólne.csv", encoding='utf8')
        self.labels = self.file.readline()
        self.labels = self.labels.split(';')
        temp_file = []
        for line in self.file:
            temp_file.append(line.split(';'))
        self.file = temp_file

        # for calculating
        self.data = pd.read_csv('Dane_2011_ogólne.csv', sep=';')
        self.data_labels = self.data.columns.tolist()
        del self.data_labels[0]
        del self.data_labels[0]
        for label in self.data_labels:
            self.data[label] = self.data[label].astype(int)

    def get_labels(self):
        return self.labels

    def get_file(self):
        return self.file

    def get_general_data(self):
        general_data = self.data.iloc[[0]]
        del general_data[general_data.columns[0]]
        del general_data[general_data.columns[0]]
        general_data.values[0].tolist()
        general_data_as_table = pd.DataFrame(list(zip(general_data.columns, general_data.values[0])),
                                             columns=['Wykształcenie', 'Liczba'])
        return general_data_as_table

    def education_general_diagram(self):
        general_data_as_table = self.get_general_data()
        values = general_data_as_table['Liczba'].to_numpy()

        fig, ax = plt.subplots(figsize=(9, 6))

        plt.bar(self.data_labels, values, color='purple', )
        ax.yaxis.set_major_formatter(format_number)

        plt.title('Ogólne wykształcenie')
        plt.show()
        return fig, ax
