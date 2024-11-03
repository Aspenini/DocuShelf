import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget, QGridLayout, QScrollArea, QDialog, QVBoxLayout, QDialogButtonBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import fitz  # PyMuPDF, for rendering PDF cover pages

class LoadPdfThread(QThread):
    page_loaded = pyqtSignal(QLabel)

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path

    def run(self):
        doc = fitz.open(self.pdf_path)
        for page_number in range(len(doc)):
            pix = doc.load_page(page_number).get_pixmap()
            page_image_path = self.pdf_path.replace('.pdf', f'_page_{page_number}.png')
            pix.save(page_image_path)
            pdf_pixmap = QPixmap(page_image_path)
            pdf_page_label = QLabel()
            pdf_page_label.setPixmap(pdf_pixmap.scaled(400, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.page_loaded.emit(pdf_page_label)

class DocuShelf(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocuShelf")
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        self.main_layout = QVBoxLayout()
        
        # Add "Add PDF" button
        self.add_pdf_button = QPushButton("+")
        self.add_pdf_button.setFixedSize(50, 50)
        self.add_pdf_button.clicked.connect(self.import_pdf)
        self.main_layout.addWidget(self.add_pdf_button)
        
        # Scroll area to display PDF tiles
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.scroll_area_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        
        self.main_layout.addWidget(self.scroll_area)
        
        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
        
        # Directory to store PDFs
        self.pdf_directory = os.path.join(os.path.expanduser("~"), "Documents", "DocuShelf")
        if not os.path.exists(self.pdf_directory):
            os.makedirs(self.pdf_directory)
        
        # Load existing PDFs
        self.load_pdfs()

    def import_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            # Copy PDF to internal directory
            shutil.copy(file_path, self.pdf_directory)
            self.load_pdfs()

    def load_pdfs(self):
        # Clear current grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Load and display PDFs as tiles
        pdf_files = [f for f in os.listdir(self.pdf_directory) if f.endswith('.pdf')]
        row, col = 0, 0
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.pdf_directory, pdf_file)
            cover_label = self.get_pdf_cover(pdf_path)
            self.grid_layout.addWidget(cover_label, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def get_pdf_cover(self, pdf_path):
        # Extract cover page as an image
        doc = fitz.open(pdf_path)
        pix = doc.load_page(0).get_pixmap()
        cover_path = pdf_path.replace('.pdf', '.png')
        pix.save(cover_path)
        
        # Create QLabel to display cover
        cover_label = QLabel()
        cover_pixmap = QPixmap(cover_path)
        cover_label.setPixmap(cover_pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        cover_label.mousePressEvent = lambda event, path=pdf_path: self.open_pdf_dialog(path)
        return cover_label

    def open_pdf_dialog(self, pdf_path):
        # Create a dialog to display the PDF within the app
        pdf_dialog = QDialog(self)
        pdf_dialog.setWindowTitle(os.path.basename(pdf_path))
        pdf_dialog.setGeometry(150, 150, 800, 600)
        
        dialog_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_layout = QHBoxLayout()
        scroll_area_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setWidgetResizable(True)
        
        dialog_layout.addWidget(scroll_area)

        # Add close button to dialog
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(pdf_dialog.reject)
        dialog_layout.addWidget(button_box)

        pdf_dialog.setLayout(dialog_layout)

        # Load PDF pages in a separate thread
        self.load_thread = LoadPdfThread(pdf_path)
        self.load_thread.page_loaded.connect(lambda label: scroll_layout.addWidget(label))
        self.load_thread.start()
        
        pdf_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocuShelf()
    window.show()
    sys.exit(app.exec_())
