"""Frame "Contactos > Agregar"."""
from PySide6.QtCore import QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (QFormLayout, QFrame, QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QVBoxLayout)

from .dialogs import confirm_discard, show_warning
from .validators import validate_contact


class AddContactView(QFrame):
    contactCreated = Signal(dict)   # datos del nuevo contacto (id puede ser None)
    closed = Signal()               # el usuario salió del frame

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("formFrame")

        title = QLabel("CONTACTOS")
        title.setObjectName("title")
        subtitle = QLabel("Agregar")
        subtitle.setObjectName("subtitle")

        self.id_edit = QLineEdit()
        self.id_edit.setObjectName("idField")
        self.id_edit.setReadOnly(True)
        self.id_edit.setPlaceholderText("Automático")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ingresa Nombre")
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("XXXX-XXXX")
        self.phone_edit.setMaxLength(9)
        self.phone_edit.setValidator(
            QRegularExpressionValidator(QRegularExpression(r"[0-9\-]{0,9}")))
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Ingresa correo")
        self.city_edit = QLineEdit()
        self.city_edit.setPlaceholderText("Ingresa ciudad")

        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.WrapAllRows)
        form.setVerticalSpacing(8)
        for text, widget in (("ID", self.id_edit), ("NOMBRE", self.name_edit),
                             ("TELÉFONO", self.phone_edit),
                             ("CORREO", self.email_edit),
                             ("CIUDAD", self.city_edit)):
            lbl = QLabel(text)
            lbl.setObjectName("fieldLabel")
            form.addRow(lbl, widget)

        self.cancel_btn = QPushButton("Cancelar")
        self.accept_btn = QPushButton("Aceptar")
        self.accept_btn.setObjectName("primary")
        buttons = QHBoxLayout()
        buttons.addWidget(self.cancel_btn)
        buttons.addWidget(self.accept_btn)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.addWidget(title)
        root.addWidget(subtitle)
        root.addSpacing(10)
        root.addLayout(form)
        root.addStretch()
        root.addLayout(buttons)

        self.cancel_btn.clicked.connect(self._on_cancel)
        self.accept_btn.clicked.connect(self._on_accept)

    # --- API pública ---
    def prepare(self, next_id) -> None:
        """Limpia el formulario y muestra el siguiente ID (o None)."""
        self.id_edit.setText("" if next_id is None else str(next_id))
        for edit in (self.name_edit, self.phone_edit, self.email_edit, self.city_edit):
            edit.clear()

    def is_dirty(self) -> bool:
        return any(e.text().strip() for e in
                   (self.name_edit, self.phone_edit, self.email_edit, self.city_edit))

    def can_leave(self) -> bool:
        return not self.is_dirty() or confirm_discard(self)

    # --- Slots internos ---
    def _on_cancel(self):
        if self.can_leave():
            self.closed.emit()

    def _on_accept(self):
        data = {
            "id": int(self.id_edit.text()) if self.id_edit.text().isdigit() else None,
            "name": self.name_edit.text().strip(),
            "phone": self.phone_edit.text().strip(),
            "email": self.email_edit.text().strip(),
            "city": self.city_edit.text().strip(),
        }
        errors = validate_contact(data)
        if errors:
            show_warning(self, "Datos inválidos", "\n".join(errors))
            return
        self.contactCreated.emit(data)
