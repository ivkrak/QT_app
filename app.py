import tkinter as tk
from tk_tools import EntryGrid, Graph
from main import ExcelDatabase
from tkinter.filedialog import askopenfilename
import codecs
import chardet
from loguru import logger

"""
DEPRECATED!
"""

logger.add(
    'errors.log',
    format='{time} {level} {message}',
    level='DEBUG'
)


class App:
    def __init__(self, master):
        self.master = master
        self.data = [[1997, 12], [1998, 15], [1999, 21], [2000, 15], [2001, 16], [2002, 11], [2003, 10], [2004, 9]]
        self.export_button = tk.Button(self.master, text="Экспорт", command=self.export_excel)
        self.import_button = tk.Button(self.master, text="Импорт", command=self.import_excel)
        #self.entryGridFrame = tk.Frame(self.master, width=100, height=100, background="bisque")
        self.entryGrid = EntryGrid(self.master, num_of_columns=2, headers=["Год", "Урожай"])
        for i in self.data:
            self.entryGrid.add_row(i)
        #self.scrollbar = tk.Scrollbar(orient="vertical", command = self.entryGrid.yview)
        self.graph = None

    @logger.catch
    def import_excel(self):
        db = ExcelDatabase('DB.db')
        file_name = askopenfilename(filetypes=[("Text files", "*.xlsx")])
        #file_name = askopenfilename(filetypes=[("Text files", "*.xlsx")]).split('/')[-1]
        table_name = db.load_excel_data(file_path=file_name)
        dct = db.create_dct_from_table('DB.db', table_name)
        keys = list(dct.keys())
        rows = [[dct[keys[0]][i], dct[keys[1]][j]] for i in range(len(dct[keys[0]])) for j in range(len(dct[keys[1]]))
                if i == j]
        db.close_connection()
        self.show_data(rows)

    @logger.catch
    def grid_placement(self):
        self.export_button.grid(row="0", column="0", columnspan="2")
        self.import_button.grid(row="0", column="2", columnspan="2")
        #self.entryGridFrame.grid(row="1", column="0")
        self.entryGrid.grid(row="1", column="0")
        self.graph.grid(row="3", column="6")


    @logger.catch
    def export_excel(self):
        with open('Ноябрьский.xlsx', 'rb') as f:
            result = chardet.detect(f.read())
        print(result)

    @logger.catch
    def show_data(self, data):
        if data is not None:
            self.data = data
        self.entryGrid.grid_forget()
        self.entryGrid = EntryGrid(self.master, num_of_columns=2, headers=["Год", "Урожай"])
        for i in self.data:
            self.entryGrid.add_row(i)
        self.grid_placement()

    @logger.catch
    def graph_data(self):
        self.graph = Graph(
            parent=self.master,
            x_min=1997,
            x_max=2023,
            y_min=0.0,
            y_max=40.0,
            x_tick=1.0,
            y_tick=2.0,
            width=3000,
            height=1600
        )
        line = [(x / 10, x / 10) for x in range(10)]
        for i in self.data:
            self.graph.plot_point(i[0], i[1])



window = tk.Tk()
window.title("EntryGrid Example")
app = App(window)

app.graph_data()
app.grid_placement()

window.mainloop()
