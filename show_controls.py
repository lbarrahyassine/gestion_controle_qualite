import sys
from show_tables import execute_query, id_equip, freq_from_id
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from PyQt5 import QtGui
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

        self.tableWidget.setColumnCount(10)  # 8 data columns + 1 for the button + 1 statut
        self.tableWidget.setHorizontalHeaderLabels(
            ["equip","id_ctrl", "date_echeance", "date_planifie", "date_ctrl", "id_org", "id_type", "id_freq", "Modify", "Statut"])

    def load_data(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT libele, controles.id_ctrl, date_echeance, date_planifie, date_ctrl, id_org, id_type, id_freq FROM controles JOIN assoc_id_idctrl ON controles.id_ctrl =assoc_id_idctrl.id_ctrl  join equipement on assoc_id_idctrl.id = equipement.id")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

            modify_button = QPushButton("Modify")
            modify_button.clicked.connect(lambda _, r=row: self.modify_row(r))
            self.tableWidget.setCellWidget(row_idx, 8, modify_button)

            # Calculate and set the status
            date_echeance = row[2] if row[2] != 'None' else None
            date_ctrl = row[4] if row[4] != 'None' else None
            date_planif = row[3] if row[3] != 'None' else None
            statut = get_statut(date_echeance,date_planif, date_ctrl)
            statut_item = QTableWidgetItem(statut)

            # Set background color based on status
            if statut == "Controlé":
                statut_item.setBackground(QtGui.QColor(0, 240, 0))  # vert
            elif statut == "Urgent Non Planifié":
                statut_item.setBackground(QtGui.QColor(240, 0, 0))  # Red
            else:
                statut_item.setBackground(QtGui.QColor(255,153,51))
            self.tableWidget.setItem(row_idx, 9, statut_item)
        cursor.close()

    def modify_row(self, row_data):
        try :
            dialog = ModifyDialog(row_data, self)
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()
                self.save_changes(row_data[1], new_data,row_data[0])
        except Exception as e:
            print(e)

    def save_changes(self, id_ctrl, new_data, libele_equip):
        # Ensure `date_ctrl` and `id_freq` are properly handled
        date_ctrl = new_data[2] #if new_data[2] != "NULL" else None
        id_freq = int(new_data[5])
        mois_freq = freq_from_id(str(id_freq))
        equipe=id_equip(libele_equip)
        if not new_data[2]:
            new_data[2]="NULL"
        else :
            new_data[2] = f"'{new_data[2]}'"
        if not new_data[1]:
            new_data[1]="NULL"
        else :
            new_data[1] = f"'{new_data[1]}'"
        cursor = connection.cursor()

        query = (f"UPDATE controles SET date_echeance='{new_data[0]}', date_planifie={new_data[1]}, "
                 f"date_ctrl={new_data[2]}, id_org={new_data[3]}, id_type={new_data[4]}, id_freq={new_data[5]} "
                 f"WHERE id_ctrl={id_ctrl}")

        try:
            cursor.execute(query)
            connection.commit()
            # If `date_ctrl` is set, create new control entry
            if date_ctrl:
                new_date_echeance = datetime.strptime(date_ctrl, '%Y-%m-%d') + timedelta(days=mois_freq*30)
                new_date_echeance_str = new_date_echeance.strftime('%Y-%m-%d')
                execute_query(connection,
                              f"INSERT INTO controles (date_echeance, date_planifie, date_ctrl, id_org, id_type, id_freq) VALUES ('{new_date_echeance_str}', NULL,NULL,{new_data[3]},{new_data[4]},{id_freq});")
                cursor = connection.cursor()
                cursor.execute("SELECT LAST_INSERT_ID();")
                ctrl_id = cursor.fetchone()[0]
                execute_query(connection, f"INSERT INTO assoc_id_idctrl (id, id_ctrl) VALUES ({equipe},{ctrl_id});")

            QMessageBox.information(self, "Success", "Controle enregistré et nouveau contrôle créé!")
            self.load_data()
        except Error as e:
            QMessageBox.critical(self, "Error", f"l'erreur est: {e}")
        finally:
            cursor.close()


