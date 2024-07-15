import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from connexion import *
from datetime import *
from create_ctrl_ui import Ui_Dialog2 as CreateCtrlDialog


class ControlsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.load_data()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.tableWidget = QTableWidget(self)
        self.layout.addWidget(self.tableWidget)

        self.tableWidget.setColumnCount(8)  # 7 data columns + 1 for the button
        self.tableWidget.setHorizontalHeaderLabels(
            ["id_ctrl", "date_echeance", "date_planifie", "date_ctrl", "id_org", "id_type", "id_freq", "Modify"])

    def load_data(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id_ctrl, date_echeance, date_planifie, date_ctrl, id_org, id_type, id_freq FROM controles")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

            modify_button = QPushButton("Modify")
            modify_button.clicked.connect(lambda _, r=row: self.modify_row(r))
            self.tableWidget.setCellWidget(row_idx, 7, modify_button)

        cursor.close()

    def modify_row(self, row_data):
        try :
            dialog = ModifyDialog(row_data, self)
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()
                self.save_changes(row_data[0], new_data)
        except Exception as e:
            print(e)

    def save_changes(self, id_ctrl, new_data):
        cursor = connection.cursor()
        query = (f"UPDATE controles SET date_echeance='{new_data[0]}', date_planifie='{new_data[1]}', "
                 f"date_ctrl='{new_data[2]}', id_org={new_data[3]}, id_type={new_data[4]}, id_freq={new_data[5]} "
                 f"WHERE id_ctrl={id_ctrl}")

        try:
            cursor.execute(query)
            connection.commit()
            QMessageBox.information(self, "Success", "Changes saved successfully!")
            self.load_data()
        except Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            cursor.close()


class ModifyDialog(QDialog):
    def __init__(self, row_data, parent=None):
        super().__init__(parent)
        self.row_data = row_data
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ModifyDialog")
        self.resize(400, 300)
        self.formLayout = QFormLayout(self)

        self.date_echeance = QLineEdit(self)
        self.date_planifie = QLineEdit(self)
        self.date_ctrl = QLineEdit(self)
        self.id_org = QLineEdit(self)
        self.id_type = QLineEdit(self)
        self.id_freq = QLineEdit(self)

        self.formLayout.addRow("Date Echeance", self.date_echeance)
        self.formLayout.addRow("Date Planifie", self.date_planifie)
        self.formLayout.addRow("Date Ctrl", self.date_ctrl)
        self.formLayout.addRow("ID Org", self.id_org)
        self.formLayout.addRow("ID Type", self.id_type)
        self.formLayout.addRow("ID Freq", self.id_freq)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.formLayout.addRow(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.load_data()
        self.setWindowTitle("Modify Control")

    from datetime import datetime, date  # Ensure correct import

    def load_data(self):
        def parse_date(date_value):
            if isinstance(date_value, str):
                return datetime.strptime(date_value, "%Y-%m-%d").date()
            return date_value

        date_echeance = parse_date(self.row_data[1])
        date_planifie = parse_date(self.row_data[2])
        date_ctrl = parse_date(self.row_data[3])

        self.date_echeance.setText(
            date_echeance.strftime("%Y-%m-%d") if isinstance(date_echeance, date) else str(date_echeance))
        self.date_planifie.setText(
            date_planifie.strftime("%Y-%m-%d") if isinstance(date_planifie, date) else str(date_planifie))
        self.date_ctrl.setText(date_ctrl.strftime("%Y-%m-%d") if isinstance(date_ctrl, date) else str(date_ctrl))

        self.id_org.setText(str(self.row_data[4]))
        self.id_type.setText(str(self.row_data[5]))
        self.id_freq.setText(str(self.row_data[6]))

    def get_data(self):
        return [
            self.date_echeance.text(),
            self.date_planifie.text(),
            self.date_ctrl.text(),
            self.id_org.text(),
            self.id_type.text(),
            self.id_freq.text(),
        ]