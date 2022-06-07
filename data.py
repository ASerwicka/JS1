import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

WYZSZE = 0
POLICEALNE = 1
SREDNIE = 2
ZAWODOWE = 3
GIMNAZJALNE = 4
PODSTAWOWE = 5


# funkcja formatująca wartości na Y osi wykresów
def format_number(data_value, indx):
    if data_value >= 1000000:
        formatter = '{:1.1f}M'.format(data_value * 0.000001)
    else:
        formatter = '{:1.0f}K'.format(data_value * 0.001)
    return formatter


class Data:
    def __init__(self):
        # pobranie danych w formacie do wyświetlania w klasie Gui
        self.file = open("Dane_2011_ogólne.csv", encoding='utf8')
        self.labels = self.file.readline().replace('\n', '')
        self.labels = self.labels.split(';')
        temp_file = []
        for line in self.file:
            newline = []
            line = line.split(';')
            for sth in line:
                try:
                    sth = int(sth)
                    newline.append(sth)
                except:
                    newline.append(sth)
            temp_file.append(newline)
        self.file = temp_file

        # pobranie danych w formacie do obrabiania w klasie Data
        self.data = pd.read_csv('Dane_2011_ogólne.csv', sep=';')
        self.data_labels = self.data.columns.tolist()
        del self.data_labels[0]
        del self.data_labels[0]
        for label in self.data_labels:
            self.data[label] = self.data[label].astype(int)
        self.age_data = self.data.iloc[1:71]
        self.age_data_men = self.data.iloc[72:142]
        self.age_data_women = self.data.iloc[143:213]

    # oddaje labels w formie do wyświetlenia całego pliku
    def get_labels(self):
        return self.labels

    # oddaje wartości z całego pliku
    def get_file(self):
        return self.file

    # oddaje dane ogólne według wieku (bez podziałów)
    def get_age_data(self):
        return self.age_data

    # oddaje DataFrame złożony z informacji o wieku i odpowiadającej ilości osób z przekazanym do funkcji wykształceniem
    def get_age_data_arg(self, arg):
        if arg.__eq__('Ogółem'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data["Ogółem"])),
                                columns=['Wiek', 'Liczba wszystkich osób'])
        elif arg.__eq__('Podstawowe'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data["Podstawowe"])),
                                columns=['Wiek', 'Liczba osób z wykształceniem podstawowym'])
        elif arg.__eq__('Średnie'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data["Średnie"])),
                                columns=['Wiek', 'Liczba osób z wykształceniem średnim'])
        elif arg.__eq__('Policealne'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data["Policealne"])),
                                columns=['Wiek', 'Liczba osób z wykształceniem policealnym'])
        elif arg.__eq__('Zasadnicze zawodowe'):
            return pd.DataFrame(
                list(zip(self.age_data["Wiek"], self.age_data["Zasadnicze zawodowe"])),
                columns=['Wiek', 'Liczba osób z wykształceniem zasadniczym zawodowym'])
        elif arg.__eq__('Gimnazjalne'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data["Gimnazjalne"])),
                                columns=['Wiek', 'Liczba osób z wykształceniem gimnazjalnym'])
        elif arg.__eq__('Wyższe'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data["Wyższe"])),
                                columns=['Wiek', 'Liczba osób z wykształceniem wyższym'])
        elif arg.__eq__('Wszystkie'):
            return self.age_data

    # oddaje DataFrame złożony z informacji o wieku i odpowiadającej ilości osób z przekazanym do funkcji
    # wykształceniem podzielonych na płeć
    def get_age_data_sex_arg(self, arg):
        if arg.__eq__('Ogółem'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data_women["Ogółem"],
                                         self.age_data_men["Ogółem"])),
                                columns=['Wiek', 'Liczba wszystkich kobiet', 'Liczba wszystkich mężczyzn'])
        elif arg.__eq__('Podstawowe'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data_women["Podstawowe"],
                                         self.age_data_men["Podstawowe"])),
                                columns=['Wiek', 'Liczba kobiet z wykształceniem podstawowym',
                                         'Liczba mężczyzn z wykształceniem podstawowym'])
        elif arg.__eq__('Średnie'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data_women["Średnie"],
                                         self.age_data_men["Średnie"])),
                                columns=['Wiek', 'Liczba kobiet z wykształceniem średnim',
                                         'Liczba mężczyzn z wykształceniem średnim'])
        elif arg.__eq__('Policealne'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data_women["Policealne"],
                                         self.age_data_men["Policealne"])),
                                columns=['Wiek', 'Liczba kobiet z wykształceniem policealnym',
                                         'Liczba mężczyzn z wykształceniem policealnym'])
        elif arg.__eq__('Zasadnicze zawodowe'):
            return pd.DataFrame(
                list(zip(self.age_data["Wiek"], self.age_data_women["Zasadnicze zawodowe"],
                         self.age_data_men["Zasadnicze zawodowe"])),
                columns=['Wiek', 'Liczba kobiet z wykształceniem zasadniczym zawodowym',
                         'Liczba mężczyzn z wykształceniem zasadniczym zawodowym'])
        elif arg.__eq__('Gimnazjalne'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data_women["Gimnazjalne"],
                                         self.age_data_men["Gimnazjalne"])),
                                columns=['Wiek', 'Liczba kobiet z wykształceniem gimnazjalnym',
                                         'Liczba mężczyzn z wykształceniem gimnazjalnym'])
        elif arg.__eq__('Wyższe'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data_women["Wyższe"],
                                         self.age_data_men["Wyższe"])),
                                columns=['Wiek', 'Liczba kobiet z wykształceniem wyższym',
                                         'Liczba mężczyzn z wykształceniem wyższym'])
        elif arg.__eq__('Wszystkie'):
            return pd.DataFrame(list(zip(self.age_data["Wiek"], self.age_data_women["Ogółem"],
                                         self.age_data_men["Ogółem"], self.age_data_women["Wyższe"],
                                         self.age_data_men["Wyższe"], self.age_data_women["Policealne"],
                                         self.age_data_men["Policealne"], self.age_data_women["Średnie"],
                                         self.age_data_men["Średnie"], self.age_data_women["Zasadnicze zawodowe"],
                                         self.age_data_men["Zasadnicze zawodowe"], self.age_data_women["Gimnazjalne"],
                                         self.age_data_men["Gimnazjalne"], self.age_data_women["Podstawowe"],
                                         self.age_data_men["Podstawowe"])),
                                columns=['Wiek', 'Ogółem K', 'Ogółem M', 'Wyższe K', 'Wyższe M', 'Policealne K',
                                         'Policealne M', 'Średnie K', 'Średnie M', 'Zawodowe K', 'Zawodowe M',
                                         'Gimnazjalne K', 'Gimnazjalne M', 'Podstawowe K', 'Podstawowe M'])

    # oddaje DataFrame z informacją złożoną z wszystkich wykształceń oraz ogólnej liczbie osób które dane
    # wykształcenie posiada
    def get_general_data(self):
        general_data = self.data.iloc[[0]]
        del general_data[general_data.columns[0]]
        del general_data[general_data.columns[0]]
        general_data.values[0].tolist()
        general_data_as_table = pd.DataFrame(list(zip(general_data.columns, general_data.values[0])),
                                             columns=['Wykształcenie', 'Liczba'])
        return general_data_as_table

    # oddaje DataFrame z informacją złożoną z wszystkich wykształceń oraz liczbie mężczyzn które dane
    # wykształcenie posiada
    def get_general_data_men(self):
        general_data_men = self.data.iloc[[71]]
        del general_data_men[general_data_men.columns[0]]
        del general_data_men[general_data_men.columns[0]]
        general_data_men_as_table = pd.DataFrame(list(zip(general_data_men.columns, general_data_men.values[0])),
                                                 columns=['Wykształcenie', 'Liczba'])
        return general_data_men_as_table

    # oddaje DataFrame z informacją złożoną z wszystkich wykształceń oraz liczbie kobiet które dane
    # wykształcenie posiada
    def get_general_data_women(self):
        general_data_women = self.data.iloc[[142]]
        del general_data_women[general_data_women.columns[0]]
        del general_data_women[general_data_women.columns[0]]
        general_data_women_as_table = pd.DataFrame(list(zip(general_data_women.columns, general_data_women.values[0])),
                                                   columns=['Wykształcenie', 'Liczba'])
        return general_data_women_as_table

    # oddaje DataFrame złożony z informacji o ogólnej ilości osób z przekazanym do funkcji
    # wykształceniem podzielonych na płeć
    def get_general_data_sex_arg(self, arg):
        if arg.__eq__('Wszystkie'):
            return pd.DataFrame(list(
                zip(self.get_general_data_women()["Wykształcenie"], self.get_general_data_women()["Liczba"],
                    self.get_general_data_men()["Liczba"])),
                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

        elif arg.__eq__('Ogółem'):
            return pd.DataFrame([("Ogółem", 17027406, 15652208)],
                                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

        elif arg.__eq__('Podstawowe'):
            return pd.DataFrame([("Podstawowe", int(self.get_general_data_women().iloc[[PODSTAWOWE]]["Liczba"]),
                                  int(self.get_general_data_men().iloc[[PODSTAWOWE]]["Liczba"]))],
                                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

        elif arg.__eq__('Średnie'):
            return pd.DataFrame([("Srednie", int(self.get_general_data_women().iloc[[SREDNIE]]["Liczba"]),
                                  int(self.get_general_data_men().iloc[[SREDNIE]]["Liczba"]))],
                                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

        elif arg.__eq__('Policealne'):
            return pd.DataFrame([("Policealne", int(self.get_general_data_women().iloc[[POLICEALNE]]["Liczba"]),
                                  int(self.get_general_data_men().iloc[[POLICEALNE]]["Liczba"]))],
                                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

        elif arg.__eq__('Zasadnicze zawodowe'):
            return pd.DataFrame([("Zasadnicze zawodowe", int(self.get_general_data_women().iloc[[ZAWODOWE]]["Liczba"]),
                                  int(self.get_general_data_men().iloc[[ZAWODOWE]]["Liczba"]))],
                                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

        elif arg.__eq__('Gimnazjalne'):
            return pd.DataFrame([("Gimnazjalne", int(self.get_general_data_women().iloc[[GIMNAZJALNE]]["Liczba"]),
                                  int(self.get_general_data_men().iloc[[GIMNAZJALNE]]["Liczba"]))],
                                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

        elif arg.__eq__('Wyższe'):
            return pd.DataFrame([("Wyższe", int(self.get_general_data_women().iloc[[WYZSZE]]["Liczba"]),
                                  int(self.get_general_data_men().iloc[[WYZSZE]]["Liczba"]))],
                                columns=['Wykształcenie', 'Liczba kobiet', 'Liczba mężczyzn'])

    # oddaje DataFrame złożony z informacji o ogólnej ilości osób z przekazanym do funkcji wykształceniem
    def get_general_data_arg(self, arg):
        if arg.__eq__('Wszystkie'):
            return self.get_general_data()

        elif arg.__eq__('Ogółem'):
            return pd.DataFrame([("Ogółem", 32679614)],
                                columns=['Wykształcenie', 'Liczba'])

        elif arg.__eq__('Podstawowe'):
            return self.get_general_data().iloc[[PODSTAWOWE]]

        elif arg.__eq__('Średnie'):
            return self.get_general_data().iloc[[SREDNIE]]

        elif arg.__eq__('Policealne'):
            return self.get_general_data().iloc[[POLICEALNE]]

        elif arg.__eq__('Zasadnicze zawodowe'):
            return self.get_general_data().iloc[[ZAWODOWE]]

        elif arg.__eq__('Gimnazjalne'):
            return self.get_general_data().iloc[[GIMNAZJALNE]]

        elif arg.__eq__('Wyższe'):
            return self.get_general_data().iloc[[WYZSZE]]

    # diagram pokazujący ogólną liczbę osób według każdego z wykształceń (w tym przypadku pokazuje się tylko
    # wykres na którym są wszystkie wykształcenia, ponieważ nie ma sensu pokazywać na wykresie pojedyńczą wartość)
    def get_general_diagram_arg(self, arg):
        if arg.__eq__('Wszystkie'):
            return self.general_diagram()
        else:
            return None

    # diagram pokazujący ogólną liczbę osób według każdego z wykształceń podzieloną na płcie
    def get_general_sex_diagram_arg(self, arg):
        if arg.__eq__('Wszystkie'):
            return self.general_sex_diagram_edu()

        elif arg.__eq__('Ogółem'):
            return self.general_sex_diagram()

        elif arg.__eq__('Podstawowe'):
            return self.create_sex_diagram(PODSTAWOWE)

        elif arg.__eq__('Średnie'):
            return self.create_sex_diagram(SREDNIE)

        elif arg.__eq__('Policealne'):
            return self.create_sex_diagram(POLICEALNE)

        elif arg.__eq__('Zasadnicze zawodowe'):
            return self.create_sex_diagram(ZAWODOWE)

        elif arg.__eq__('Gimnazjalne'):
            return self.create_sex_diagram(GIMNAZJALNE)

        elif arg.__eq__('Wyższe'):
            return self.create_sex_diagram(WYZSZE)

    # diagram pokazujący liczbę osób według wieku dla wykształcenia przekazanego jako argument
    def get_age_diagram_arg(self, arg):
        if arg.__eq__('Wszystkie'):
            return self.age_general_diagram()

        elif arg.__eq__('Ogółem'):
            return self.create_age_diagram('Ogółem')

        elif arg.__eq__('Podstawowe'):
            return self.create_age_diagram('Podstawowe')

        elif arg.__eq__('Średnie'):
            return self.create_age_diagram('Średnie')

        elif arg.__eq__('Policealne'):
            return self.create_age_diagram('Policealne')

        elif arg.__eq__('Zasadnicze zawodowe'):
            return self.create_age_diagram('Zasadnicze zawodowe')

        elif arg.__eq__('Gimnazjalne'):
            return self.create_age_diagram('Gimnazjalne')

        elif arg.__eq__('Wyższe'):
            return self.create_age_diagram('Wyższe')

    # diagram pokazujący liczbę osób według wieku dla wykształcenia przekazanego jako argument podzieloną na płcie
    def get_age_sex_diagram_arg(self, arg):
        if arg.__eq__('Wszystkie'):
            return None

        elif arg.__eq__('Ogółem'):
            return self.create_age_sex_diagram('Ogółem')

        elif arg.__eq__('Podstawowe'):
            return self.create_age_sex_diagram('Podstawowe')

        elif arg.__eq__('Średnie'):
            return self.create_age_sex_diagram('Średnie')

        elif arg.__eq__('Policealne'):
            return self.create_age_sex_diagram('Policealne')

        elif arg.__eq__('Zasadnicze zawodowe'):
            return self.create_age_sex_diagram('Zasadnicze zawodowe')

        elif arg.__eq__('Gimnazjalne'):
            return self.create_age_sex_diagram('Gimnazjalne')

        elif arg.__eq__('Wyższe'):
            return self.create_age_sex_diagram('Wyższe')

    # diagram pokazujący zestawienie wszystkich wykształceń i ogólnej ilości osób które dane wykształcenie posiada
    def general_diagram(self):
        general_data_as_table = self.get_general_data()
        values = general_data_as_table['Liczba'].to_numpy()

        fig, ax = plt.subplots(figsize=(13, 6))

        plt.bar(self.data_labels, values, color='purple', )
        ax.yaxis.set_major_formatter(format_number)

        plt.title('Ogólne wykształcenie')
        plt.show()
        return fig

    # diagram pokazujący zestawienie wszystkich wykształceń i ogólnej ilości osób które dane wykształcenie posiada
    # podzielony na płcie
    def general_sex_diagram_edu(self):
        general_data_as_table_women = self.get_general_data_women()
        general_data_as_table_men = self.get_general_data_men()
        value_men = general_data_as_table_men['Liczba'].to_numpy()
        value_women = general_data_as_table_women['Liczba'].to_numpy()

        fig, ax = plt.subplots(figsize=(13, 6))
        index = np.arange(len(self.data_labels))
        width = 0.4

        plt.bar(index - width / 2, value_men, width, label='men')
        plt.bar(index + width / 2, value_women, width, label='women')
        plt.xticks(index, self.data_labels)
        ax.yaxis.set_major_formatter(format_number)
        plt.title('Wykształcenie względem płci')
        plt.legend()
        plt.show()
        return fig

    # funkcja tworzy diagram zależności wykształcenia podanego jako argument oraz ilości osób, podzielony na płcie
    def create_sex_diagram(self, arg):
        general_data_as_table_women = self.get_general_data_women()
        general_data_as_table_men = self.get_general_data_men()
        values = [int(general_data_as_table_men.iloc[[arg]]['Liczba']),
                  int(general_data_as_table_women.iloc[[arg]]['Liczba'])]

        fig, ax = plt.subplots(figsize=(13, 6))

        plt.bar(["Mężczyźni", "Kobiety"], values)
        ax.yaxis.set_major_formatter(format_number)
        plt.show()
        return fig

    # diagram pokazujący zestawienie ilości kobiet i mężczyzn od których pobrano dane
    def general_sex_diagram(self):
        values = [int(self.data.iloc[[71]]["Ogółem"]), int(self.data.iloc[[142]]["Ogółem"])]

        fig, ax = plt.subplots(figsize=(13, 6))

        plt.bar(["Mężczyźni", "Kobiety"], values)
        ax.yaxis.set_major_formatter(format_number)
        plt.show()
        return fig

    # diagram pokazujący zależność wieku i ilości osób w danym wieku z wykształceniem podanym jako argument
    def create_age_diagram(self, arg):
        font = {'size': 6.5}
        matplotlib.rc('font', **font)
        labels = self.age_data['Wiek']
        values = self.age_data[arg].to_numpy()

        fig, ax = plt.subplots(figsize=(20, 5))

        plt.bar(labels, values, color='purple')
        ax.yaxis.set_major_formatter(format_number)
        plt.show()
        return fig

    # diagram pokazujący zestawienie wszystkich wykształceń według wieku
    def age_general_diagram(self):
        font = {'size': 6.5}
        matplotlib.rc('font', **font)
        fig, ax = plt.subplots(figsize=(20, 5))

        plt.plot(self.age_data['Wiek'], self.age_data['Podstawowe'], c='#8a134e', label='Podstawowe')
        plt.plot(self.age_data['Wiek'], self.age_data['Gimnazjalne'], c='#00c3ff', label='Gimnazjalne')
        plt.plot(self.age_data['Wiek'], self.age_data['Średnie'], c='#FF0000', label='Średnie')
        plt.plot(self.age_data['Wiek'], self.age_data['Zasadnicze zawodowe'], c='#0101DF', label='Zasadnicze zawodowe')
        plt.plot(self.age_data['Wiek'], self.age_data['Wyższe'], c='#74DF00', label='Wyższe')
        ax.yaxis.set_major_formatter(format_number)
        plt.legend()
        plt.show()
        return fig

    # funkcja tworząca diagram zależności wieku od ilości osób z wykształceniem podanym jako argument
    # podzielony na płcie
    def create_age_sex_diagram(self, arg):
        font = {'size': 6.5}
        matplotlib.rc('font', **font)
        fig, ax = plt.subplots(figsize=(20, 5))

        plt.plot(self.age_data_men['Wiek'], self.age_data_men[arg], c='#8a134e', label='Mężczyźni')
        plt.plot(self.age_data_women['Wiek'], self.age_data_women[arg], c='#00c3ff', label='Kobiety')
        ax.yaxis.set_major_formatter(format_number)
        plt.legend()
        plt.show()
        return fig


if __name__ == '__main__':
    #data = Data()
    #data.create_sex_diagram(2)
    pass
