import sys
from PyQt5.QtWidgets import *
from modify_equipement import *
from show_tables import *
from add_cat import *
from modify_category import *
from Add_equi import *
import warnings
from PyQt5.QtCore import Qt
warnings.filterwarnings("ignore", category=DeprecationWarning)
from show_controls import *
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'controle qualité'
        self.left = 100
        self.top = 100
        self.width = 1100
        self.height = 600
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        # Create a placeholder widget
        self.tab_widget = QTabWidget()
        placeholder = QWidget()
        placeholder_layout = QVBoxLayout()

        # Create a label for the placeholder
        placeholder_label = QLabel("Select a tab from the menu.")
        font = placeholder_label.font()
        font.setPointSize(22)  # Set font size
        placeholder_label.setFont(font)
        placeholder_label.setAlignment(Qt.AlignCenter)  # Center the text
        placeholder_label.setStyleSheet("padding: 10px;")  # Additional styling

        placeholder_layout.addWidget(placeholder_label)
        placeholder.setLayout(placeholder_layout)

        # Add placeholder widget as the only initial tab
        self.tab_widget.addTab(placeholder, "Home")

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # Initialize other tabs without adding them to the tab widget yet
        self.equipement_tab = self.equipement_win()
        self.categorie_tab = self.categ_win()
        self.sous_categorie_tab = self.sous_categorie_win()


    def create_table(self, data, headers, context):
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers)+2)
        table.setHorizontalHeaderLabels(headers+["modify"]+["delete"])

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(item)))
            modify_button = QPushButton("Modify")
            if context == "equipement":
                modify_button.clicked.connect(lambda _, r=i: self.modify_row(r))
            elif context == "categorie":
                modify_button.clicked.connect(lambda _, r=i: self.modify_category_row(r))
            elif context == "sous_categorie":
                modify_button.clicked.connect(lambda _, r=i: self.modify_sous_categorie_row(r))
            table.setCellWidget(i, len(headers), modify_button)
            #modify_button.clicked.connect(lambda _, r=i: ModifyEquipementDialog.modify_row(r))  # Connect to your modify function
            #table.setCellWidget(i, len(headers), modify_button)

            # Create Delete button
            delete_button = QPushButton("Delete")
            if context == "equipement":
                delete_button.clicked.connect(lambda _, r=i: self.delete_row(r))
            elif context == "categorie":
                delete_button.clicked.connect(lambda _, r=i: self.delete_category_row(r))
            elif context == "sous_categorie":
                modify_button.clicked.connect(lambda _, r=i: self.delete_sous_categorie_row(r))
            table.setCellWidget(i, len(headers), modify_button)
            #delete_button.clicked.connect(lambda _, r=i: self.delete_row(r))  # Connect to your delete function
            table.setCellWidget(i, len(headers) + 1, delete_button)
        return table

    def modify_row(self, row):
        try:
            dialog = ModifyEquipementDialog(self, row)
            dialog.exec_()
            self.refresh_equipements()
        except Exception as e:
            print(f"Error in modify_row: {e}")

    def refresh_equipements(self):
        data = fetch_equipements()
        self.equipements_table.setRowCount(0)  # Clear existing rows
        self.equipements_table.setRowCount(len(fetch_equipements()))  # Set new row count

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.equipements_table.setItem(i, j, QTableWidgetItem(str(item)))
            modify_button = QPushButton("Modify")
            modify_button.clicked.connect(lambda _, r=i: self.modify_row(r))  # Connect to your modify function
            self.equipements_table.setCellWidget(i, len(["id", "Libelle", "id_sous_cat","date_service","actif","rebut","id_energie"]), modify_button)

            # Create Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=i: self.delete_row(r))  # Connect to your delete function
            self.equipements_table.setCellWidget(i, len(["id", "Libelle", "id_sous_cat","date_service","actif","rebut","id_energie"]) + 1, delete_button)

    def equipement_win(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.equipements_table = self.create_table(fetch_equipements(), ["id", "Libelle", "id_sous_cat","date_service","actif","rebut","id_energie"],"equipement")
        layout.addWidget(self.equipements_table)

        ajouter_button = QPushButton("Ajouter")
        ajouter_button.setMinimumHeight(40)
        ajouter_button.setStyleSheet("background-color:#C3C0C0;")
        ajouter_button.clicked.connect(self.open_add_dialog)  # Connect the button to a function
        layout.addWidget(ajouter_button)

        widget.setLayout(layout)
        return widget

    def sous_categorie_win(self):
        try:
            widget = QWidget()
            layout = QVBoxLayout()

            self.sous_categorie_table = self.create_table(fetch_sous_categories(), ["id", "Libelle", "id_cat"],"sous_categorie")
            layout.addWidget(self.sous_categorie_table)

            widget.setLayout(layout)
        except Exception as e:
            print(e)
        return widget
    def delete_sous_categorie_row(self, row):
        sous_categorie_id = self.sous_categorie_table.item(row, 0).text()
        category_id = self.sous_categorie_table.item(row, 2).text()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM sous_categorie WHERE id_sous_cat = %s", (sous_categorie_id,))
            #cursor.execute("DELETE FROM categorie WHERE id_cat = %s", (category_id,))
            connection.commit()
            cursor.close()
            self.sous_categorie_table.removeRow(row)
        except Error as e:
            print(f"The error '{e}' occurred")
        print("delete sous_categorie and its category is clicked")

    def modify_sous_categorie_row(self):
        print("j ai pas encore implementé modifier sous categorie")
    def open_add_dialog(self):
        dialog = AddEquipementDialog(self)
        dialog.exec_()
        self.refresh_equipements()

    def show_add_cat_dialog(self):
        dialog = QDialog(self)
        ui = Ui_Dialog()
        ui.setupUi(dialog)
        dialog.exec_()
        self.refresh_categories()

    def categ_win(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.categorie_table = self.create_table(fetch_categories(), ["id", "Libelle"], "categorie")
        layout.addWidget(self.categorie_table)

        ajouter_button2 = QPushButton("Ajouter")
        ajouter_button2.clicked.connect(self.show_add_cat_dialog)  # Connect the button to a function
        layout.addWidget(ajouter_button2)

        widget.setLayout(layout)
        return widget

    def delete_row(self, row):
        print("delete equipement is clicked")
        equipement_id = self.equipements_table.item(row, 0).text()
        print(equipement_id)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM equipement WHERE id = %s", (equipement_id,))
            connection.commit()
            cursor.close()
            self.equipements_table.removeRow(row)
        except Error as e:
            print(f"The error '{e}' occurred")

    def modify_category_row(self, row):
        dialog = ModifyCategoryDialog(self, row, self.categorie_table)
        dialog.exec_()
        self.refresh_categories()

    def delete_category_row(self, row):
        category_id = self.categorie_table.item(row, 0).text()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM sous_categorie WHERE id_cat = %s", (category_id,))
            cursor.execute("DELETE FROM categorie WHERE id_cat = %s", (category_id,))
            connection.commit()
            cursor.close()
            self.categorie_table.removeRow(row)
        except Error as e:
            print(f"The error '{e}' occurred")
        print("delete cat is clicked")
    def refresh_categories(self):
        data = fetch_categories()
        self.categorie_table.setRowCount(0)
        self.categorie_table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.categorie_table.setItem(i, j, QTableWidgetItem(str(item)))
            modify_button = QPushButton("Modify")
            modify_button.clicked.connect(lambda _, r=i: self.modify_category_row(r))
            self.categorie_table.setCellWidget(i, len(["id", "Libelle"]), modify_button)

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, r=i: self.delete_category_row(r))
            self.categorie_table.setCellWidget(i, len(["id", "Libelle"]) + 1, delete_button)

    def open_equipement_tab(self):
        self.tab_widget.addTab(self.equipement_tab, "Equipements")  # Add tab if not already added
        self.tab_widget.setCurrentWidget(self.equipement_tab)

    def open_categorie_tab(self):
        self.tab_widget.addTab(self.categorie_tab, "Categories")  # Add tab if not already added
        self.tab_widget.setCurrentWidget(self.categorie_tab)

    def open_sous_categorie_tab(self):
        self.tab_widget.addTab(self.sous_categorie_tab, "Sous Categories")  # Add tab if not already added
        self.tab_widget.setCurrentWidget(self.sous_categorie_tab)

    def show_controls(self):
        controls_widget = ControlsWidget()
        self.tab_widget.addTab(controls_widget, "Show Controls")
        self.tab_widget.setCurrentWidget(controls_widget)
"""if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())"""
