"""Diálogos reutilizables."""
from PySide6.QtWidgets import QMessageBox


def confirm_discard(parent) -> bool:
    """Pregunta si se desea salir sin guardar. True = salir."""
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Question)
    box.setWindowTitle("Salir sin guardar")
    box.setText("Hay cambios sin guardar.\n¿Desea salir sin guardar?")
    yes = box.addButton("Salir sin guardar", QMessageBox.AcceptRole)
    no = box.addButton("Seguir editando", QMessageBox.RejectRole)
    box.setDefaultButton(no)
    box.exec()
    return box.clickedButton() is yes


def show_warning(parent, title: str, text: str) -> None:
    QMessageBox.warning(parent, title, text)
