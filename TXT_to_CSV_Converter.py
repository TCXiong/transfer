import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QMessageBox, QLineEdit
import csv

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Text to CSV Converter'
        self.left = 50
        self.top = 100
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.import_button = QPushButton('Import Text File', self)
        self.import_button.move(50, 50)
        self.import_button.clicked.connect(self.get_file)

        self.convert_button = QPushButton('Convert to CSV File', self)
        self.convert_button.move(200, 50)
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.convert_file)

        self.status_label = QLabel('', self)
        self.status_label.move(50, 100)

        self.show()

    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.txt)", options=options)
        if file_name:
            self.file_name = file_name
            self.convert_button.setEnabled(True)
            self.status_label.setText('Selected file: ' + self.file_name)

    def convert_file(self):
        # Prompt the user for an output file name
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        default_file_name = os.path.splitext(os.path.basename(self.file_name))[0] + '_converted.csv'
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", default_file_name, "CSV Files (*.csv)", options=options)
        if file_name:
            with open(self.file_name, 'r') as f:
                lines = f.readlines()[6:]
                data = []
                for line in lines:
                    line = line.strip()
                    columns = line.split('\t')
                    first_column = columns[0].split('    ')[-1]
                    second_column = columns[1]
                    data.append([first_column, second_column])
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            msg = QMessageBox()
            msg.setWindowTitle("Conversion Complete")
            msg.setText("The conversion is DONE!")
            msg.exec_()
            self.status_label.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())