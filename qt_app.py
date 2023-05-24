import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create QTableWidget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)

        # Create buttons
        self.import_button = QPushButton("Import Data")
        self.export_button = QPushButton("Export Data")

        # Connect buttons to their functions
        self.import_button.clicked.connect(self.import_data)
        self.export_button.clicked.connect(self.export_data)

        # Add table and buttons to layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.import_button)
        layout.addWidget(self.export_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def import_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Data tables(*.xlsx)", options=options)
        if fileName:
            print(fileName)
        with open("data.csv", "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                row_count = self.table_widget.rowCount()
                self.table_widget.insertRow(row_count)
                for col, data in enumerate(row):
                    self.table_widget.setItem(row_count, col, QTableWidgetItem(data))

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