import sqlite3
import pandas as pd
from loguru import logger


logger.add(
    'errors.log',
    format='{time} {level} {message}',
    level='DEBUG'
)
logger.info('Бот запущен')


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
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column1_name} TEXT, {column2_name} TEXT)"
        self.cursor.execute(query)
        self.conn.commit()

    @logger.catch
    def load_excel_data(self, file_path, table_name):
        """
        Загружает данные из файла Excel в указанную таблицу базы данных.

        Параметры:
        - file_path (строка): путь к файлу Excel
        - table_name (строка): имя таблицы, в которую будут загружены данные
        """
        df = pd.read_excel(file_path)
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

    @logger.catch
    def close_connection(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()


# Пример использования класса ExcelDatabase
db = ExcelDatabase('DB.db')

# Создание таблицы с названием 'excel_data'
db.create_table(table_name='excel_data123', column1_name='Год', column2_name='Пшеница_яровая')

# Загрузка данных из файла Excel в таблицу 'excel_data'
file_path = 'Октябрьский.xlsx'
db.load_excel_data(file_path=file_path, table_name='excel_data123')

# Получение названий таблиц в базе данных
table_names = db.get_table_names()
print('Названия таблиц в базе данных:', table_names)

# Закрытие соединения с базой данных
db.close_connection()
