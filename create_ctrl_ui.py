# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDateEdit, QMessageBox
from show_tables import *
from PyQt5 import QtCore, QtGui, QtWidgets
import datetime

class Ui_Dialog2(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(655, 715)
        self.buttonBox2 = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox2.setGeometry(QtCore.QRect(420, 660, 193, 28))
        self.buttonBox2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox2.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox2.setObjectName("buttonBox2")

        self.label_type = QtWidgets.QLabel(Dialog)
        self.label_type.setGeometry(QtCore.QRect(30, 60, 151, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_type.setFont(font)
        self.label_type.setObjectName("label_type")

        self.label_2_freq = QtWidgets.QLabel(Dialog)
        self.label_2_freq.setGeometry(QtCore.QRect(30, 140, 89, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2_freq.setFont(font)
        self.label_2_freq.setObjectName("label_2_freq")

        self.label_3_equip = QtWidgets.QLabel(Dialog)
        self.label_3_equip.setGeometry(QtCore.QRect(30, 220, 111, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3_equip.setFont(font)
        self.label_3_equip.setObjectName("label_3_equip")

        self.comboBox_type = QtWidgets.QComboBox(Dialog)
        self.comboBox_type.setGeometry(QtCore.QRect(190, 60, 151, 22))
        self.comboBox_type.setObjectName("comboBox_type")

        self.comboBox_2_freq = QtWidgets.QComboBox(Dialog)
        self.comboBox_2_freq.setGeometry(QtCore.QRect(190, 140, 151, 22))
        self.comboBox_2_freq.setObjectName("comboBox_2_freq")

        self.comboBox_3_equip = QtWidgets.QComboBox(Dialog)
        self.comboBox_3_equip.setGeometry(QtCore.QRect(190, 220, 151, 22))
        self.comboBox_3_equip.setObjectName("comboBox_3_equip")

        self.label_4_date_ech = QtWidgets.QLabel(Dialog)
        self.label_4_date_ech.setGeometry(QtCore.QRect(20, 430, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4_date_ech.setFont(font)
        self.label_4_date_ech.setObjectName("label_4_date_ech")

        self.date_ech_input = QDateEdit(Dialog)
        self.date_ech_input.setGeometry(QtCore.QRect(170, 430, 141, 22))
        self.date_ech_input.setObjectName("date_date_ech")
        self.date_ech_input.setDisplayFormat("yyyy-MM-dd")
        self.date_ech_input.setCalendarPopup(True)

        self.label_5_date_plan = QtWidgets.QLabel(Dialog)
        self.label_5_date_plan.setGeometry(QtCore.QRect(340, 430, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5_date_plan.setFont(font)
        self.label_5_date_plan.setObjectName("label_5_date_plan")

        self.lineEdit_2_date_plan = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2_date_plan.setGeometry(QtCore.QRect(490, 430, 141, 22))
        self.lineEdit_2_date_plan.setText("")
        self.lineEdit_2_date_plan.setObjectName("lineEdit_2_date_plan")

        self.label_6_date_ctrl = QtWidgets.QLabel(Dialog)
        self.label_6_date_ctrl.setGeometry(QtCore.QRect(20, 490, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6_date_ctrl.setFont(font)
        self.label_6_date_ctrl.setObjectName("label_6_date_ctrl")

        self.lineEdit_3_date_ctrl = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3_date_ctrl.setGeometry(QtCore.QRect(170, 490, 141, 22))
        self.lineEdit_3_date_ctrl.setObjectName("lineEdit_3_date_ctrl")

        self.label_7_auditeur = QtWidgets.QLabel(Dialog)
        self.label_7_auditeur.setGeometry(QtCore.QRect(30, 550, 89, 22))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7_auditeur.setFont(font)
        self.label_7_auditeur.setObjectName("label_7_auditeur")

        self.comboBox_4_auditeur = QtWidgets.QComboBox(Dialog)
        self.comboBox_4_auditeur.setGeometry(QtCore.QRect(160, 550, 151, 22))
        self.comboBox_4_auditeur.setObjectName("comboBox_4_auditeur")

        self.retranslateUi(Dialog)
        self.buttonBox2.accepted.connect(self.accept)  # type: ignore
        self.buttonBox2.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.load_data()

        self.comboBox_type.currentIndexChanged.connect(self.update_load_freq)
        self.comboBox_2_freq.currentIndexChanged.connect(self.update_load_equip)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ajout_ctrl"))
        self.label_type.setText(_translate("Dialog", "type du controle :"))
        self.label_2_freq.setText(_translate("Dialog", "frequence :"))
        self.label_3_equip.setText(_translate("Dialog", "Equipement : "))
        self.label_4_date_ech.setText(_translate("Dialog", "date echeance : "))
        self.label_5_date_plan.setText(_translate("Dialog", "date planifié : "))
        self.label_6_date_ctrl.setText(_translate("Dialog", "date du controle : "))
        self.label_7_auditeur.setText(_translate("Dialog", "auditeur :"))

    def load_data(self):
        self.comboBox_type.addItem("- - select - -")
        self.comboBox_4_auditeur.addItem("- - select - -")
        for row in fetch_type_combo():
            libele = row[0]
            self.comboBox_type.addItem(libele)
        for row in fetch_auditeur():
            libele = row[0]
            self.comboBox_4_auditeur.addItem(libele)

    def update_load_freq(self):
        self.comboBox_2_freq.clear()
        type = self.comboBox_type.currentText()
        if type == "- - select - -":
            return
        temp = id_type(type)
        for row in fetch_frequence2_combo(str(temp)):
            self.comboBox_2_freq.addItem(str(row[0]) + " " + row[1])

    def update_load_equip(self):
        self.comboBox_3_equip.clear()
        type = self.comboBox_type.currentText()
        if type == "- - select - -":
            return
        temp = id_type(type)
        freq = self.comboBox_2_freq.currentText()
        if not freq:
            return
        freq = freq.split(" ")
        frequence = id_freq(freq[0], freq[1])
        for row in fetch_equipement2_combo(str(temp), str(frequence)):
            libele = row[0]
            self.comboBox_3_equip.addItem(libele)

    def accept(self):
        try:
            type = self.comboBox_type.currentText()
            temp = id_type(type)
            freq = self.comboBox_2_freq.currentText()
            freq = freq.split(" ")
            frequence = id_freq(freq[0], freq[1])
            equip = self.comboBox_3_equip.currentText()
            equipe = id_equip(equip)
            org = self.comboBox_4_auditeur.currentText()
            orga = id_org(org)
            date_ech = self.date_ech_input.date().toString("yyyy-MM-dd")
            date_ctrl = self.lineEdit_3_date_ctrl.text()
            date_plan = self.lineEdit_2_date_plan.text()

            if not date_ech:
                QMessageBox.warning(None, "Input Error", "tu dois entrer la date d'echeance.")
                return

            if not date_ctrl:
                date_ctrl = "NULL"
            else:
                try:
                    date_ctrl = f"'{datetime.datetime.strptime(date_ctrl, '%Y-%m-%d').strftime('%Y-%m-%d')}'"
                except ValueError:
                    QtWidgets.QMessageBox.warning(None, "Input Error",
                                                  "Format de date invalide pour date du controle, utilise YYYY-MM-DD.")
                    return

            try:
                date_ech = datetime.datetime.strptime(date_ech, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                QMessageBox.warning(None, "Input Error",
                                    "Format de date invalide pour date echeance, utilise YYYY-MM-DD.")
                return

            if date_plan:
                try:
                    date_plan = datetime.datetime.strptime(date_plan, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    QMessageBox.warning(None, "Input Error",
                                        "Format de date invalide pour date planifie, utilise YYYY-MM-DD.")
                    return
            else:
                date_plan = None

            execute_query(connection, f"INSERT INTO controles (date_echeance, date_planifie, date_ctrl, id_org, id_type, id_freq) VALUES ('{date_ech}', '{date_plan}',{date_ctrl},{orga},{temp},{frequence});")
            cursor = connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID();")
            ctrl_id = cursor.fetchone()[0]
            execute_query(connection,f"INSERT INTO assoc_id_idctrl (id, id_ctrl) VALUES ({equipe},{ctrl_id});")
            cursor.close()

            QMessageBox.information(None, "Success", "Controle ajouté avec succès!")
            QtWidgets.QApplication.quit()

        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(None, "Error", f"An error occurred: {e}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog2()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
