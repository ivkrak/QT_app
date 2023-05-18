import sqlite3
import pandas as pd


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def execute_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def import_from_db_file(self, db_file):
        with sqlite3.connect(db_file) as conn:
            conn.row_factory = sqlite3.Row
            self.cur.execute("SELECT * FROM data")
            rows = self.cur.fetchall()
            data = [dict(row) for row in rows]
        return data

    def import_from_excel_file(self, excel_file):
        df = pd.read_excel(excel_file)
        data = df.to_dict('records')
        return data

    def close(self):
        self.conn.close()
