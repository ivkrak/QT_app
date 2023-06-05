import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from main import picture, ExcelDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VKR_Project")
        # Create QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Годы", "Урожайность"])


        self.coefficients_table_widget = QTableWidget()
        self.coefficients_table_widget.setColumnCount(2)
        self.coefficients_table_widget.setHorizontalHeaderLabels(["Коэффициент", "Значение"])
        # Create buttons
        self.import_button = QPushButton("Импорт")
        self.export_button = QPushButton("Экспорт")

        self.linear_button = QPushButton("Линейная")
        self.exponent_button = QPushButton("Степенная")
        self.logistic_button = QPushButton("Логистическая")
        self.asymptotic_button = QPushButton("Асимптотическая")

        # Connect buttons to their functions
        self.import_button.clicked.connect(self.import_data)
        self.export_button.clicked.connect(self.export_data)

        self.linear_button.clicked.connect(self.recalculate_linear)
        self.exponent_button.clicked.connect(self.recalculate_exponential)
        self.logistic_button.clicked.connect(self.recalculate_logistic)
        self.asymptotic_button.clicked.connect(self.recalculate_asymptotic)

        self.parametric_table = QTableWidget()
        self.parametric_table.setColumnCount(3)

        self.label = QLabel(self)

        self.imported_once = False

        # loading image
        self.pixmap = QPixmap(picture.create_picture([1,1,1], [1997,1998,1999], "График", "Урожайность", "Годы", "exponential"))

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
        layoutCV = QVBoxLayout()
        layoutCV.addWidget(self.label)
        layoutCV.addWidget(self.coefficients_table_widget)
        layoutCV.stretch(2)
        layoutH.addLayout(layoutCV)
        layoutH.addWidget(self.parametric_table)
        self.layoutV = QVBoxLayout()

        self.layoutV.addWidget(self.import_button)
        self.layoutV.addWidget(self.export_button)
        self.layoutV.addLayout(layoutH)

        central_widget = QWidget()
        central_widget.setLayout(self.layoutV)



        self.setCentralWidget(central_widget)

    def import_data(self):
        if not self.imported_once:
            layoutHB = QHBoxLayout()
            layoutHB.addWidget(self.linear_button)
            layoutHB.addWidget(self.exponent_button)
            layoutHB.addWidget(self.logistic_button)
            layoutHB.addWidget(self.asymptotic_button)
            self.layoutV.addLayout(layoutHB)
            self.imported_once = True

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

        rows = [[int(dct[keys[0]][i]), dct[keys[1]][j]] for i in range(len(dct[keys[0]])) for j in range(len(dct[keys[1]]))
                if i == j]
        db.close_connection()

        for i in rows:
            rowPosition = self.table_widget.rowCount()
            self.table_widget.insertRow(rowPosition)
            self.table_widget.setItem(rowPosition, 0, QTableWidgetItem(str(i[0])))
            self.table_widget.setItem(rowPosition, 1, QTableWidgetItem(str(i[1])))

        self.pixmap = QPixmap(picture.create_picture(self.yses, self.xses, "График", "Урожайность", "Годы", "linear"))
        self.label.setPixmap(self.pixmap)

        self.update_coefficents(picture.calculate_statistic(self.yses, self.xses, "linear"))

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

    def recalculate_linear(self):
        self.pixmap = QPixmap(picture.create_picture(self.yses, self.xses, "График", "Урожайность", "Годы", "linear"))
        self.label.setPixmap(self.pixmap)
        self.update_coefficents(picture.calculate_statistic(self.yses, self.xses, "linear"))
    def recalculate_exponential(self):
        self.pixmap = QPixmap(picture.create_picture(self.yses, self.xses, "График", "Урожайность", "Годы", "exponential"))
        self.label.setPixmap(self.pixmap)
        self.update_coefficents(picture.calculate_statistic(self.yses, self.xses, "exponential"))
    def recalculate_logistic(self):
        self.pixmap = QPixmap(picture.create_picture(self.yses, self.xses, "График", "Урожайность", "Годы", "logistic"))
        self.label.setPixmap(self.pixmap)
        self.update_coefficents(picture.calculate_statistic(self.yses, self.xses, "logistic"))
    def recalculate_asymptotic(self):
        print('Asymptotic')

    def update_coefficents(self, dict_data):
        for i in dict_data.keys():
            rowPosition = self.coefficients_table_widget.rowCount()
            self.coefficients_table_widget.insertRow(rowPosition)
            self.coefficients_table_widget.setItem(rowPosition, 0, QTableWidgetItem(str(i)))
            self.coefficients_table_widget.setItem(rowPosition, 1, QTableWidgetItem(str(dict_data[i])))

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())