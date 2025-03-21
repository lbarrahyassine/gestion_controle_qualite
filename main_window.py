import sys
from PyQt5.QtWidgets import *
from first_in_menu import *
from create_ctrl_ui import Ui_Dialog2 as CreateCtrlDialog
from show_controls import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Main Window'
        self.left = 100
        self.top = 100
        self.width = 1400
        self.height = 700
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.central_widget = App()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_menu()
    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('tables')

        open_equipement_action = QAction('Open Equipements', self)
        open_equipement_action.triggered.connect(self.central_widget.open_equipement_tab)
        file_menu.addAction(open_equipement_action)

        open_categorie_action = QAction('Open Categories', self)
        open_categorie_action.triggered.connect(self.central_widget.open_categorie_tab)
        file_menu.addAction(open_categorie_action)

        open_sous_categorie_action = QAction('Open Sous Categories', self)
        open_sous_categorie_action.triggered.connect(self.central_widget.open_sous_categorie_tab)
        file_menu.addAction(open_sous_categorie_action)

        file_menu2 = menubar.addMenu('controles')
        create_ctrl_action = QAction('nouveau Ctrl', self)
        create_ctrl_action.triggered.connect(self.show_create_ctrl_dialog)
        file_menu2.addAction(create_ctrl_action)


        actionShowControls = QtWidgets.QAction("Show Controls", self)
        actionShowControls.triggered.connect(self.show_controls)
        file_menu2.addAction(actionShowControls)

    def show_controls(self):
        try:
            self.central_widget.show_controls()
        except Exception as e:
            print(e)


    def show_create_ctrl_dialog(self):
        dialog = QDialog(self)
        ui = CreateCtrlDialog()
        ui.setupUi(dialog)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
