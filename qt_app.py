import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from main import picture, ExcelDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Годы", "Урожай"])

        # Create buttons
        self.import_button = QPushButton("Импорт")
        self.export_button = QPushButton("Экспорт")

        # Connect buttons to their functions
        self.import_button.clicked.connect(self.import_data)
        self.export_button.clicked.connect(self.export_data)

        self.label = QLabel(self)

        # loading image
        self.pixmap = QPixmap(picture.create_picture([1,1,1], [1997,1998,1999], "График", "Урожай", "Годы"))

        # adding image to label
        self.label.setPixmap(self.pixmap)

        # Optional, resize label to image size
        self.label.resize(200, 200)

        self.xses = []
        self.yses = []

        # Add table and buttons to layout
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.table_widget)
        layoutH.stretch(1)
        layoutH.addWidget(self.label)
        layoutV = QVBoxLayout()

        layoutV.addWidget(self.import_button)
        layoutV.addWidget(self.export_button)
        layoutV.addLayout(layoutH)

        central_widget = QWidget()
        central_widget.setLayout(layoutV)

        self.setCentralWidget(central_widget)

    def import_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Data tables(*.xlsx)", options=options)
        if fileName:
            print(fileName)

        db = ExcelDatabase('DB.db')
        table_name = db.load_excel_data(file_path=fileName)
        dct = db.create_dct_from_table('DB.db', table_name)
        keys = list(dct.keys())
        for i in range(len(dct[keys[0]])):
            self.xses.append(dct[keys[0]][i])
        for i in range(len(dct[keys[1]])):
            self.yses.append(dct[keys[1]][i])

        rows = [[dct[keys[0]][i], dct[keys[1]][j]] for i in range(len(dct[keys[0]])) for j in range(len(dct[keys[1]]))
                if i == j]
        db.close_connection()

        for i in rows:
            rowPosition = self.table_widget.rowCount()
            self.table_widget.insertRow(rowPosition)
            self.table_widget.setItem(rowPosition, 0, QTableWidgetItem(str(i[0])))
            self.table_widget.setItem(rowPosition, 1, QTableWidgetItem(str(i[1])))

        self.pixmap = QPixmap(picture.create_picture(self.yses, self.xses, "График", "Урожай", "Годы"))
        self.label.setPixmap(self.pixmap)

    def export_data(self):
        with open("output.csv", "w", newline="") as file:
            csv_writer = csv.writer(file)
            for row in range(self.table_widget.rowCount()):
                row_data = []
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                csv_writer.writerow(row_data)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())