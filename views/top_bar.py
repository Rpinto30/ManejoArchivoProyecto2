"""Barra superior: Contactos, Herramientas, Exportar y Ayuda."""
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QComboBox, QFrame, QHBoxLayout, QPushButton,
                               QVBoxLayout)


class MenuCombo(QComboBox):
    """Combobox que actúa como menú: el primer ítem es el título (oculto en
    la lista). Al elegir una opción emite `optionSelected(clave)` y vuelve
    al título."""

    optionSelected = Signal(str)

    def __init__(self, title: str, options: dict[str, str], parent=None):
        super().__init__(parent)
        self.addItem(title, None)
        for key, text in options.items():
            self.addItem(text, key)
        self.view().setRowHidden(0, True)
        self.setMinimumWidth(170)
        self.activated.connect(self._on_activated)

    def _on_activated(self, index: int):
        key = self.itemData(index)
        self.setCurrentIndex(0)
        if key:
            self.optionSelected.emit(key)


class TopBar(QFrame):
    contactsAction = Signal(str)   # "add" | "search"
    toolsAction = Signal(str)      # "integrity" | "backup" | "info"
    exportAction = Signal(str)     # "json" | "report"
    helpClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")

        self.contacts_menu = MenuCombo(
            "Contactos", {"add": "Agregar", "search": "Buscar por ID"})
        self.tools_menu = MenuCombo(
            "Herramientas", {"integrity": "Verificar integridad",
                             "backup": "Crear respaldo ZIP",
                             "info": "Información del archivo"})
        self.export_menu = MenuCombo(
            "Exportar", {"json": "Exportar JSON", "report": "Crear reporte", "both": "Crear ambos"})
        self.help_button = QPushButton("Ayuda")

        right = QVBoxLayout()
        right.setSpacing(6)
        right.addWidget(self.help_button)
        right.addWidget(self.export_menu)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(16)
        layout.addWidget(self.contacts_menu)
        layout.addWidget(self.tools_menu)
        layout.addStretch()
        layout.addLayout(right)

        self.contacts_menu.optionSelected.connect(self.contactsAction)
        self.tools_menu.optionSelected.connect(self.toolsAction)
        self.export_menu.optionSelected.connect(self.exportAction)
        self.help_button.clicked.connect(self.helpClicked)
