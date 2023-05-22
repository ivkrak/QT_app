import tkinter as tk
from tk_tools import EntryGrid, Graph
from main import ExcelDatabase
from tkinter.filedialog import askopenfilename
import codecs
import chardet
from loguru import logger

logger.add(
    'errors.log',
    format='{time} {level} {message}',
    level='DEBUG'
)


class App:
    def __init__(self, master):
        self.master = master
        self.data = [[0, 0], [0, 0], [0, 0]]

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
    def export_excel(self):
        with open('Ноябрьский.xlsx', 'rb') as f:
            result = chardet.detect(f.read())
        print(result)

    @logger.catch
    def create_buttons(self):
        ex_button = tk.Button(window, text="Экспорт", command=self.export_excel)
        ex_button.grid()
        im_button = tk.Button(window, text="Импорт", command=self.import_excel)
        im_button.grid()

    @logger.catch
    def show_data(self, data):
        if data is not None:
            self.data = data
        grid = EntryGrid(self.master, num_of_columns=2, headers=["Год", "Урожай"])
        for i in self.data:
            grid.add_row(i)

    @logger.catch
    def graph_data(self):
        graph = Graph(
            parent=self.master,
            x_min=-1.0,
            x_max=1.0,
            y_min=0.0,
            y_max=2.0,
            x_tick=0.2,
            y_tick=0.2,
            width=500,
            height=400
        )
        line = [(x / 10, x / 10) for x in range(10)]
        graph.plot_line(line)
        graph.grid()


window = tk.Tk()
window.title("EntryGrid Example")
app = App(window)

app.show_data(None)
app.graph_data()
app.create_buttons()

window.mainloop()
