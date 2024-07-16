import sys

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from connexion import *
from modify_ctrl import *
from statut import *
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

        self.tableWidget.setColumnCount(9)  # 7 data columns + 1 for the button + 1 statut
        self.tableWidget.setHorizontalHeaderLabels(
            ["id_ctrl", "date_echeance", "date_planifie", "date_ctrl", "id_org", "id_type", "id_freq", "Modify", "Statut"])

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

            # Calculate and set the status
            date_echeance = row[1] if row[1] != 'None' else None
            date_ctrl = row[3] if row[3] != 'None' else None
            statut = get_statut(date_echeance, date_ctrl)
            self.tableWidget.setItem(row_idx, 8, QTableWidgetItem(statut))

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
        if not new_data[2]:
            new_data[2]="NULL"
        else :
            new_data[2] = f"'{new_data[2]}'"
        cursor = connection.cursor()

        query = (f"UPDATE controles SET date_echeance='{new_data[0]}', date_planifie='{new_data[1]}', "
                 f"date_ctrl={new_data[2]}, id_org={new_data[3]}, id_type={new_data[4]}, id_freq={new_data[5]} "
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


