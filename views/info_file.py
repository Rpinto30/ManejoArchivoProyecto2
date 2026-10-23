import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox
)
from PySide6.QtCore import Qt

from persistent.concat_save import RepoContact
from datetime import datetime
import stat

class DialogInfoMetadata(QDialog):
    def __init__(self, repo:RepoContact, parent=None):
        super().__init__(parent)
        self.repo = repo
        self.setWindowTitle("Metadatos - Archivo data")
        self.resize(300, 150)
        
        self.layout = QVBoxLayout()
        
        self.ll = QVBoxLayout()
        self.layout.addLayout(self.ll)
        #layout.addWidget(self.user_label)
        #layout.addWidget(self.user_input)
        #layout.addWidget(self.pass_label)
        #layout.addWidget(self.pass_input)
        
        
        botones = QDialogButtonBox.StandardButton.Ok
        self.button_box = QDialogButtonBox(botones)
        
        self.button_box.accepted.connect(self.accept) 
        
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
        self.setLabels()


    def setLabels(self):
        tittle = QLabel("INFORMACIÓN DE ARCHIVOS EN \\data")
        tittle.setStyleSheet("font-weight: bold;")
        self.ll.addWidget(tittle, alignment=Qt.AlignmentFlag.AlignCenter)

        path_data = self.repo.getPathData()
        if path_data and path_data.exists():
            for file in path_data.iterdir():
                if file.is_file():
                    data = file.stat()
                    date = datetime.fromtimestamp(data.st_mtime)

                    # Corrección de sintaxis en las cadenas de texto (uso de f-strings)
                    lname = QLabel(f"<b>=== Nombre: {file.name} ===</b>")
                    lpath = QLabel(f"Ruta absoluta:\n{file.resolve()}")
                    lsize = QLabel(f"Tamaño: {data.st_size:,} bytes")
                    ldate = QLabel(f"Fecha: {date}")
                    laut = QLabel(f"Permisos: {stat.filemode(data.st_mode)}\n\n")

                    # Agregar al layout
                    self.ll.addWidget(lname)
                    self.ll.addWidget(lpath)
                    self.ll.addWidget(lsize)
                    self.ll.addWidget(ldate)
                    self.ll.addWidget(laut)
        else:
            self.ll.addWidget(
                QLabel("El directorio de datos no existe o está vacío.")
            )
