import sys
from PyQt5.QtCore import QDate
from PyQt5 import QtCore
from datetime import *

from PyQt5.QtWidgets import *


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
        self.date_ctrl = QDateEdit(self)
        self.date_ctrl.setCalendarPopup(True)
        self.date_ctrl.setDisplayFormat("yyyy-MM-dd")
        self.date_ctrl.setSpecialValueText("")  # Set special value text to indicate an empty state
        self.date_ctrl.setDate(QDate(2000, 1, 1))  # Set a default date, it will be cleared later
        #self.date_ctrl.clear()  # Clear the default date to show the empty state
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

    def load_data(self):
        def parse_date(date_value_probably_string):
            if isinstance(date_value_probably_string, str):
                return datetime.strptime(date_value_probably_string, "%Y-%m-%d").date()
            return date_value_probably_string

        date_echeance = parse_date(self.row_data[1])
        date_planifie = parse_date(self.row_data[2])
        date_ctrl = parse_date(self.row_data[3])

        self.date_echeance.setText(
            date_echeance.strftime("%Y-%m-%d") if isinstance(date_echeance, date) else str(date_echeance))
        self.date_planifie.setText(
            date_planifie.strftime("%Y-%m-%d") if isinstance(date_planifie, date) else str(date_planifie))

        if date_ctrl is None:
            self.date_ctrl.clear()  # Clear the date edit to show as empty
        else:
            self.date_ctrl.setDate(date_ctrl)
        self.id_org.setText(str(self.row_data[4]))
        self.id_type.setText(str(self.row_data[5]))
        self.id_freq.setText(str(self.row_data[6]))


    def get_data(self):
        if self.date_ctrl.date() == QDate(2000, 1, 1):
            date_ctrl = None
        else:
            date_ctrl = self.date_ctrl.date().toString("yyyy-MM-dd")
        return [
            self.date_echeance.text(),
            self.date_planifie.text(),
            date_ctrl,

            self.id_org.text(),
            self.id_type.text(),
            self.id_freq.text(),
        ]
