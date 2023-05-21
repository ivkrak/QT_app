import sqlite3
import pandas as pd


class ExcelDatabase:
    def __init__(self, db_name):
        # Подключение к базе данных SQLite
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name):
        # Создание таблицы для хранения данных из Excel
        query = f"CREATE TABLE IF NOT EXISTS {table_name} (file_name TEXT, column1 TEXT, column2 TEXT, column3 TEXT)"
        self.cursor.execute(query)
        self.conn.commit()

    def load_excel_data(self, file_path, table_name):
        # Чтение файла Excel с помощью Pandas
        df = pd.read_excel(file_path)

        # Получение списка столбцов в Excel
        columns = df.columns.tolist()

        # Создание списка значений для каждого столбца
        values = []
        for column in columns:
            column_values = df[column].tolist()
            values.append(column_values)

        # Вставка данных в таблицу базы данных
        for i in range(len(values[0])):
            insert_data = [file_path] + [values[j][i] for j in range(len(values))]
            query = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)"
            self.cursor.execute(query, insert_data)

        # Сохранение изменений
        self.conn.commit()
        print('Данные из файла Excel успешно загружены в базу данных.')

    def get_table_names(self):
        # Получение названий таблиц в базе данных
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        tables = self.cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names

    def close_connection(self):
        # Закрытие соединения с базой данных
        self.conn.close()


# Пример использования класса ExcelDatabase
db = ExcelDatabase('excel_database.db')

# Создание таблицы с названием 'excel_data'
db.create_table('excel_data')

# Загрузка данных из файла Excel в таблицу 'excel_data'
file_path = 'example.xlsx'
db.load_excel_data(file_path, 'excel_data')

# Получение названий таблиц в базе данных
table_names = db.get_table_names()
print('Названия таблиц в базе данных:', table_names)

# Закрытие соединения с базой данных
db.close_connection()
