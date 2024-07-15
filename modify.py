"""from show_tables import *
import sys
from PyQt5.QtCore import QDate
from mysql.connector import Error"""
from connexion import *
from PyQt5.QtWidgets import *
class ModifyEquipementDialog(QDialog):
    def __init__(self, parent=None, row=None, equipements_table=None):
        super().__init__(parent)
        self.equipements_table = equipements_table
        self.setWindowTitle("Modifier un Equipement")
        self.row = row
        self.parent = parent
        self.layout = QFormLayout()
        self.equipement_id = parent.equipements_table.item(self.row, 0)
        self.libelle_input = QLineEdit(parent.equipements_table.item(row, 1).text())
        self.id_sous_cat_input = QLineEdit(parent.equipements_table.item(row, 2).text())
        self.date_service_input = QLineEdit(parent.equipements_table.item(row, 3).text())
        #self.date_service_input.setCalendarPopup(True)
        #self.actif_input = QLineEdit(parent.equipements_table.item(row, 4).text())
        self.actif_input.setChecked(parent.equipements_table.item(row, 4).text() == 'oui')
        #self.rebut_input = QLineEdit(parent.equipements_table.item(row, 5).text())
        self.rebut_input.setChecked(parent.equipements_table.item(row, 5).text() == 'oui')
        self.id_energie_input = QLineEdit(parent.equipements_table.item(row, 6).text())
        print(parent.equipements_table)
        print(parent.equipements_table.item(row, 1).text())
        self.layout.addRow("Libelle:", self.libelle_input)
        self.layout.addRow("ID Sous Cat:", self.id_sous_cat_input)
        self.layout.addRow("Date Service:", self.date_service_input)
        self.layout.addRow("Actif:", self.actif_input)
        self.layout.addRow("Rebut:", self.rebut_input)
        self.layout.addRow("ID Energie:", self.id_energie_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.modify_equipement)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def modify_equipement(self):
        libelle = self.libelle_input.text()
        id_sous_cat = self.id_sous_cat_input.text()
        date_service = self.date_service_input.text()
        #actif = self.actif_input.text()
        #rebut = self.rebut_input.text()
        actif = "oui" if self.actif_checkbox.isChecked() else "non"
        rebut = "oui" if self.actif_checkbox.isChecked() else "non"
        id_energie = self.id_energie_input.text()
        print("clicked")
        print(f"Row index: {self.row}")
        equipement_id = self.parent.equipements_table.item(self.row, 0).text()
        print(equipement_id)

        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE equipement SET libele = %s, id_sous_cat = %s, date_service = %s, actif = %s, rebut = %s, id_energie = %s WHERE id = %s",
                (libelle, id_sous_cat, date_service, actif, rebut, id_energie, equipement_id))
            connection.commit()
            cursor.close()
            self.accept()
        except Error as e:
            print(f"The error '{e}' occurred")


