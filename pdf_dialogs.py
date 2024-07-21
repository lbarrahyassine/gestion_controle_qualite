from connexion import *
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF
from PyQt5 import QtGui
import os

class PDFImportDialog(QDialog):
    def __init__(self, ctrl_id, parent=None):
        super().__init__(parent)
        self.ctrl_id = ctrl_id
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Import PDF")
        self.layout = QVBoxLayout(self)

        self.import_button = QPushButton("Import PDF")
        self.import_button.clicked.connect(self.import_pdf)
        self.layout.addWidget(self.import_button)

    def import_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_path:
            self.save_pdf_to_db(file_path)

    def save_pdf_to_db(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                pdf_data = file.read()
                cursor = connection.cursor()
                query = "UPDATE controles SET pdf = %s WHERE id_ctrl = %s"
                cursor.execute(query, (pdf_data, self.ctrl_id))
                connection.commit()
                cursor.close()
                QMessageBox.information(self, "Success", "PDF successfully imported and linked to control!")
                self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")



class PDFViewerDialog(QDialog):
    def __init__(self, ctrl_id, parent=None):
        super().__init__(parent)
        self.ctrl_id = ctrl_id
        self.setupUi()
        self.load_pdf()

    def setupUi(self):
        self.setWindowTitle("View PDF")
        self.layout = QVBoxLayout(self)
        self.pdf_label = QLabel()
        self.pdf_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.pdf_label)

    def load_pdf(self):
        cursor = connection.cursor()
        cursor.execute("SELECT pdf FROM controles WHERE id_ctrl = %s", (self.ctrl_id,))
        pdf_data = cursor.fetchone()[0]
        cursor.close()

        if pdf_data:

            pdf_dir = "./tmp"
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_path = os.path.join(pdf_dir, "pdff.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)

            self.display_pdf(pdf_path)
        else:
            QMessageBox.warning(self, "Warning", "No PDF found for this control.")

    def display_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            width, height = pix.width, pix.height
            samples = pix.samples


            # Convert to RGB format if necessary
            img_format = QtGui.QImage.Format_RGB888 if pix.alpha == 0 else QtGui.QImage.Format_RGBA8888
            img = QtGui.QImage(samples, width, height, pix.stride, img_format)

            if img.isNull():
                raise ValueError("Failed to create QImage from PDF pixmap data.")

            self.pdf_label.setPixmap(QtGui.QPixmap.fromImage(img))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while displaying the PDF: {e}")
