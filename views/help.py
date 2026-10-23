import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from persistent.concat_save import RepoContact
from datetime import datetime
import stat

class DialogHelp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayuda")
        self.resize(300, 150)
        
        self.layout = QVBoxLayout()
        
        self.user_label = QLabel("<b>Contacta con ayuda:<b>")
        self.layout.addWidget(self.user_label, alignment=Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap("views/help.jpeg")
        
        # 3. Asignar el QPixmap al QLabel
        self.label = QLabel()
        self.label.setPixmap(pixmap)
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        # 4. Opcional: escalar la imagen para que se ajuste al QLabel
        self.label.setScaledContents(True)
        self.resize(pixmap.width(), pixmap.height())
        botones = QDialogButtonBox.StandardButton.Ok
        self.button_box = QDialogButtonBox(botones)
        
        self.button_box.accepted.connect(self.accept) 
        
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

