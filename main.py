import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker
from loguru import logger
import numpy as np

logger.add(
    'errors.log',
    format='{time} {level} {message}',
    level='DEBUG'
)


class ExcelDatabase:
    """
    Класс ExcelDatabase представляет базу данных, способную загружать данные из файлов Excel.

    Атрибуты:
    - conn: объект подключения к базе данных SQLite
    - cursor: объект для выполнения операций базы данных

    Методы:
    - __init__(db_name): инициализирует объект ExcelDatabase с указанным именем базы данных SQLite
    - create_table(table_name): создает таблицу с указанным именем в базе данных
    - load_excel_data(file_path, table_name): загружает данные из файла Excel в указанную таблицу базы данных
    - get_table_names(): возвращает список названий таблиц в базе данных
    - close_connection(): закрывает соединение с базой данных
    """

    @logger.catch
    def __init__(self, db_name):
        """
        Инициализирует объект ExcelDatabase с указанным именем базы данных SQLite.

        Параметры:
        - db_name (строка): имя базы данных SQLite
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    @logger.catch
    def create_table(self, table_name, column1_name, column2_name):
        """
        Создает таблицу с указанным именем в базе данных.

        Параметры:
        - table_name (строка): имя таблицы
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column1_name} REAL, {column2_name} REAL)"
        self.cursor.execute(query)
        self.conn.commit()

    @logger.catch
    def load_excel_data(self, file_path):
        """
        Загружает данные из файла Excel в указанную таблицу базы данных.

        Параметры:
        - file_path (строка): путь к файлу Excel
        - table_name (строка): имя таблицы, в которую будут загружены данные
        """
        df = pd.read_excel(file_path)
        columns_names = df.columns.tolist()
        # region НА_ПРОВЕРКУ
        if '/' in file_path:
            table_name = (file_path.split('/')[-1]).split('.')[0]
        elif "\\" in file_path:
            table_name = (file_path.split('\\')[-1]).split('.')[0]
        # endregion
        print(f'{table_name=}')
        print(f'{file_path=}')
        # table_name = file_path.split('.')[0]
        column1_name = columns_names[0].replace(' ', '_')
        column2_name = columns_names[1].replace(' ', '_')
        self.create_table(table_name=table_name, column1_name=column1_name, column2_name=column2_name)

        columns = df.columns.tolist()
        values = []
        for column in columns:
            column_values = df[column].tolist()
            values.append(column_values)

        placeholders = ', '.join(['?' for _ in range(len(columns))])
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"

        for i in range(len(values[0])):
            insert_data = [values[j][i] for j in range(len(values))]
            self.cursor.execute(query, insert_data)

        self.conn.commit()
        print('Данные из файла Excel успешно загружены в базу данных.')
        return table_name

    @logger.catch
    def get_table_names(self):
        """
        Возвращает список названий таблиц в базе данных.

        Возвращаемое значение:
        - table_names (список строк): список названий таблиц
        """
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names

    def create_dct_from_table(self, path, table_name):
        # Установка соединения с базой данных
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        # Получение списка названий столбцов таблицы
        query = f"PRAGMA table_info({table_name})"
        cursor.execute(query)
        column_names = [column[1] for column in cursor.fetchall()]

        # Создание пустого словаря
        dictionary = {}

        # Заполнение словаря данными из таблицы
        for column in column_names:
            query = f"SELECT {column} FROM {table_name}"
            cursor.execute(query)
            column_data = [row[0] for row in cursor.fetchall()]
            dictionary[column] = column_data

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Возвращение словаря
        return dictionary

    @logger.catch
    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()


class picture:

    @staticmethod
    def create_picture(x, y, label, x_info, y_info, func):
        """
        :param x: список со значениями по оси x
        :param y: список со значениями по оси y
        :param label: название графика
        :param x_info: описания данных по оси x
        :param y_info: описания данных по оси y
        :return: путь до графика
        :func: тип математической модели
        """
        x, y = np.array(x), np.array(y)
        fig, ax = plt.subplots()
        ax.scatter(x,y)
        locator = matplotlib.ticker.MultipleLocator(1)
        ax.yaxis.set_major_locator(locator)
        ax.grid()
        is_ones = True
        for i in x:
            if i != 1:
                is_ones = False
        if not is_ones:
            if func == "exponential":
                xx = np.array([(i/9)**2 for i in range(30,49)])
                yy = np.array([i for i in range(1997, 2016)])
                ax.plot(xx, yy)
            if func == "linear":
                slope, intercept = np.polyfit(x, y, 1)
                ax.plot(x, slope*x + intercept, color='blue')
            if func == "logistic":
                x_max = np.max(x)
                for i in range(len(x)):
                    #print(f'Supposedly correct value number {i}:  {np.log(x_max / x[i] - 1) }. X_max is {x_max}, value of x is {x[i]}')
                    print(f'Supposedly correct value number {i}:  {x_max/(1+np.exp(-0.1*(i+1) + 0.25))}. X_max is {x_max}, value of x is {x[i]}, i is {i}')
                xx = np.array([x_max/(1+np.exp(-0.1*(i+1) + 0.25)) for i in range(len(x))])
                yy = np.array([i for i in range(1997, 1997+len(x))])
                ax.plot(xx, yy)
            if func == "asymptotic":
                x_max = np.max(x)
                x_min = np.min(x)
                xx = np.array([x_max - (x_max - x_min)*np.exp(-0.1 * (i + 1) +0.12) for i in range(len(x))])
                yy = np.array([i for i in range(1997, 1997 + len(x))])
                ax.plot(xx, yy)
            """
            x_avg = np.average(x)
            SSE = 0
            for i in range(len(xx)):
                SSE += (x[i] - xx[i])**2
            SST = 0
            for i in range(len(x)):
                SST += (x[i] - x_avg)**2
                
            ax.text(x[0], y[0], f'Коэффициент детерминации - {1 - (SSE / SST):.2f}')
            """


        ax.set_xlabel(x_info, fontsize=15, color='red', )
        ax.set_ylabel(y_info, fontsize=15, color='red', )

        ax.set_title(label)
        items = os.listdir('Images')
        # Перебираем все элементы
        count = 0
        for item in items:
            # Проверяем, является ли текущий элемент файлом
            if os.path.isfile(os.path.join('Images', item)):
                count += 1
        plt.savefig(f"Images/picture{count + 1}.png")
        return f"Images/picture{count + 1}.png"

    @staticmethod
    def calculate_statistic(x, y, func):
        stats = {"R2" : 0, "F": 0, "Student": 0}
        xx, yy = 0, 0
        print('start of calculation')
        match func:
            case "linear":
                xx = np.array([i for i in range(30, 49)])
                yy = np.array([i for i in range(1997, 2016)])
            case "exponential":
                xx = np.array([(i / 9) ** 2 for i in range(30, 49)])
                yy = np.array([i for i in range(1997, 2016)])
            case "logistic":
                x_max = np.max(x)
                xx = np.array([x_max / (1 + np.exp(-0.1 * (i + 1) + 0.25)) for i in range(len(x))])
                yy = np.array([i for i in range(1997, 1997 + len(x))])
            case "asymptotic":
                x_max = np.max(x)
                x_min = np.min(x)
                xx = np.array([x_max - (x_max - x_min) * np.exp(-0.1 * (i + 1) + 0.12) for i in range(len(x))])
                yy = np.array([i for i in range(1997, 1997 + len(x))])
        print('xx and yy calculated')
        x_avg = np.average(x)
        xx_avg = np.average(xx)
        print('averages calculated')
        SSE = 0
        print('calculating SSE')
        for i in range(len(xx)):
            SSE += (x[i] - xx[i]) ** 2
        SST = 0
        print('calculating SST')
        for i in range(len(x)):
            SST += (x[i] - x_avg) ** 2
        print('calculating R2')
        stats["R2"] = float(f'{1 - (SSE / SST):.2f}')
        print(stats["R2"])

        o1, o2 = np.var(x), np.var(xx)
        if o1 >= o2:
            stats["F"] = o1 ** 2 / o2 ** 2
        else:
            stats["F"] = o2 ** 2 / o1 ** 2
        print(stats["F"])
        stats["Student"] = (x_avg - xx_avg)/ (np.sqrt((o1**2 / len(x)) + ((o2**2 / len(xx)))))
        print(stats["Student"])
        return stats
    @staticmethod
    def get_file_list(folder_path):
        # Получаем список файлов и папок в указанной директории
        items = os.listdir(folder_path)

        # Отфильтровываем только файлы
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

        return files

    @staticmethod
    def get_last_picture():
        pic_arr = picture.get_file_list('Images')
        pic_arr = sorted(list(map((lambda x: x.split('.png')[0]), pic_arr)))
        return f'{pic_arr[-1]}.png'


if __name__ == "__main__":
    # Пример использования класса ExcelDatabase
    db = ExcelDatabase('DB.db')

    # Создание таблицы с названием 'excel_data'
    # db.create_table(table_name='excel_data1234', column1_name='Год', column2_name='Пшеница_яровая')

    # Загрузка данных из файла Excel в таблицу 'excel_data'
    file_path = 'Октябрьский.xlsx'
    db.load_excel_data(file_path=file_path)

    # Получение названий таблиц в базе данных
    table_names = db.get_table_names()
    print('Названия таблиц в базе данных:', table_names)

    # Закрытие соединения с базой данных
    db.close_connection()

    # Пример использования функции
    db_name = 'DB.db'
    table_name = 'Октябрьский'
    result = db.create_dct_from_table(db_name, table_name)
    print(result)
    print(len(result['Год']))
