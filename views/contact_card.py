"""Tarjeta de contacto (panel derecho)."""
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPixmap
from PySide6.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel,
                               QLineEdit, QVBoxLayout, QSizePolicy)


def _avatar_pixmap(size: int = 96) -> QPixmap:
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor("#2B1B0E"))
    p.drawEllipse(QRectF(size * 0.28, size * 0.06, size * 0.44, size * 0.44))
    body = QPainterPath()
    body.moveTo(size * 0.08, size)
    body.cubicTo(size * 0.08, size * 0.50, size * 0.92, size * 0.50, size * 0.92, size)
    body.closeSubpath()
    p.drawPath(body)
    p.end()
    return pm


class ContactCard(QFrame):
    """Muestra un contacto. Es de solo lectura salvo que se llame a
    `set_editable(True)`."""

    FIELDS = ("name", "phone", "email", "city")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumWidth(480)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self._original: dict = {}
        self._id = None

        avatar = QLabel()
        avatar.setPixmap(_avatar_pixmap())
        avatar.setFixedSize(96, 96)

        self.number_label = QLabel("NO. ----")
        self.number_label.setObjectName("cardNumber")
        self.name_edit = QLineEdit()
        self.name_edit.setObjectName("cardName")
        self.name_edit.setPlaceholderText("Nombre completo")
        self.name_edit.setMaxLength(30)
        self.name_edit.setMinimumHeight(50)

        head_text = QVBoxLayout()
        head_text.addWidget(self.number_label)
        head_text.addWidget(self.name_edit)

        head = QHBoxLayout()
        head.setSpacing(16)
        head.addWidget(avatar, 0, Qt.AlignTop)
        head.addLayout(head_text, 1)

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("XXXX-XXXX")
        self.phone_edit.setMaxLength(9)
        self.phone_edit.setMinimumHeight(45)
        self.email_edit = QLineEdit()
        self.email_edit.setMaxLength(17)
        self.email_edit.setMinimumHeight(45)
        self.city_edit = QLineEdit()
        self.city_edit.setMaxLength(40)
        self.city_edit.setMinimumHeight(45)

        left = QGridLayout()
        left.addWidget(self._label("TEL:"), 0, 0)
        left.addWidget(self.phone_edit, 0, 1)
        left.addWidget(self._label("EMAIL:"), 1, 0)
        left.addWidget(self.email_edit, 1, 1)

        right = QVBoxLayout()
        right.addWidget(self._label("CIUDAD:"))
        right.addWidget(self.city_edit)
        right.addStretch()

        separator = QFrame()
        separator.setObjectName("cardSeparator")
        separator.setFixedWidth(2)

        info = QHBoxLayout()
        info.setSpacing(14)
        info.addLayout(left, 3)
        info.addWidget(separator)
        info.addLayout(right, 2)

        root = QVBoxLayout(self)
        root.setContentsMargins(26, 24, 26, 24)
        root.setSpacing(18)
        root.addLayout(head)
        root.addLayout(info)

        self.set_editable(False)

    @staticmethod
    def _label(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        return lbl

    def _edits(self):
        return (self.name_edit, self.phone_edit, self.email_edit, self.city_edit)

    # --- API pública ---
    def set_contact(self, contact: dict) -> None:
        """Carga un contacto y lo toma como estado base (sin modificaciones)."""
        self._id = contact.get("id")
        self.number_label.setText(
            f"NO. {int(self._id):04d}" if self._id is not None else "NO. ----")
        for key, edit in zip(self.FIELDS, self._edits()):
            edit.setText(str(contact.get(key, "")))
        self._original = self.get_data()

    def get_data(self) -> dict:
        data = {"id": self._id}
        for key, edit in zip(self.FIELDS, self._edits()):
            data[key] = edit.text().strip()
        return data

    def set_editable(self, editable: bool) -> None:
        for edit in self._edits():
            edit.setReadOnly(not editable)

    def is_modified(self) -> bool:
        return self.get_data() != self._original
