"""Frame "Contactos > Buscar por ID" (trabaja junto con la ContactCard)."""
from PySide6.QtCore import QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QMessageBox)

from .contact_card import ContactCard
from .dialogs import confirm_discard, show_warning
from .validators import validate_contact


class SearchContactView(QFrame):
    searchRequested = Signal(int)    # ID a buscar -> responder con show_result()
    contactUpdated = Signal(dict)    # datos modificados y validados
    closed = Signal()                # el usuario salió del frame

    def __init__(self, card: ContactCard, parent=None):
        super().__init__(parent)
        self.setObjectName("formFrame")
        self.card = card
        self._found = False

        title = QLabel("CONTACTOS")
        title.setObjectName("title")
        subtitle = QLabel("Buscar por ID")
        subtitle.setObjectName("subtitle")

        id_label = QLabel("ID")
        id_label.setObjectName("fieldLabel")
        self.id_edit = QLineEdit()
        self.id_edit.setPlaceholderText("Ingresa ID")
        self.id_edit.setValidator(
            QRegularExpressionValidator(QRegularExpression(r"\d{0,9}")))

        self.search_btn = QPushButton("Buscar")
        self.modify_btn = QPushButton("Modificar")
        self.modify_btn.setObjectName("modify")
        self.modify_btn.setCheckable(True)
        search_row = QHBoxLayout()
        search_row.addWidget(self.search_btn)
        search_row.addWidget(self.modify_btn)

        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.setWordWrap(True)

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
        root.addSpacing(20)
        root.addWidget(id_label)
        root.addWidget(self.id_edit)
        root.addLayout(search_row)
        root.addWidget(self.error_label)
        root.addStretch()
        root.addLayout(buttons)

        self.search_btn.clicked.connect(self._on_search)
        self.id_edit.returnPressed.connect(self._on_search)
        self.modify_btn.toggled.connect(self.card.set_editable)
        self.cancel_btn.clicked.connect(self._on_cancel)
        self.accept_btn.clicked.connect(self._on_accept)
        self._update_buttons()

    # --- API pública ---
    def reset(self) -> None:
        """Deja el frame en su estado inicial."""
        self.id_edit.clear()
        self.error_label.clear()
        self._found = False
        self.modify_btn.setChecked(False)
        self.card.set_editable(False)
        self.card.hide()
        self._update_buttons()

    def show_result(self, contact: dict | None) -> None:
        """Llamar con el contacto encontrado o None si no existe."""
        self.modify_btn.setChecked(False)
        if contact:
            self.card.set_contact(contact)
            self.card.show()
            self.error_label.clear()
            self._found = True
        else:
            self.card.hide()
            self.error_label.setText("No existe un contacto con ese ID.")
            self._found = False
        self._update_buttons()

    def is_dirty(self) -> bool:
        return self._found and self.card.is_modified()

    def can_leave(self) -> bool:
        return not self.is_dirty() or confirm_discard(self)

    # --- Slots internos ---
    def _update_buttons(self):
        self.modify_btn.setEnabled(self._found)
        self.accept_btn.setEnabled(self._found)

    def _on_search(self):
        text = self.id_edit.text().strip()
        if not text:
            show_warning(self, "ID requerido", "Ingrese el ID que desea buscar.")
            return
        if not self.can_leave():
            return
        self.searchRequested.emit(int(text))

    def _on_cancel(self):
        if self.can_leave():
            self.closed.emit()

    def _on_accept(self):
        data = self.card.get_data()
        errors = validate_contact(data)
        if errors:
            show_warning(self, "Datos inválidos", "\n".join(errors))
            return
        
        ans = QMessageBox.question(
                    self, 
                    "Registrar Contacto", 
                    "¿Estas seguro de registrar la información de este contacto?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
        
        if ans == QMessageBox.StandardButton.Yes:
            self.contactUpdated.emit(data)
            self.card.set_contact(data)
            self.modify_btn.setChecked(False)
