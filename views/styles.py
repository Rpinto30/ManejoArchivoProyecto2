"""Hoja de estilos (QSS) global: estilo "directorio telefónico antiguo".

Paleta (inspirada en las Páginas Amarillas):
    papel      #F1D56A   papel amarillento
    papel claro#F7E394 / #FFF6CC
    tinta      #2B1B0E   marrón casi negro
    madera     #3E2616   fondo de la ventana
    rojo       #B5301F   acentos (números, modificar)
    verde      #2F6B3A   franja "Páginas Amarillas" (botón aceptar)
"""

APP_STYLE = """
/* ---------- Base ---------- */
QMainWindow, QWidget#root {
    background: #3E2616;
}
QWidget {
    font-family: "Georgia", "Palatino Linotype", "Times New Roman", serif;
    font-size: 14px;
    color: #2B1B0E;
}
QLabel { background: transparent; }

/* ---------- Barra superior ---------- */
QFrame#topBar {
    background: #E9C94B;
    border: 3px solid #2B1B0E;
    border-radius: 6px;
}

/* ---------- Paneles tipo página ---------- */
QFrame#leftPanel, QFrame#rightPanel {
    background: #F1D56A;
    border: 3px solid #2B1B0E;
    border-radius: 6px;
}
QFrame#formFrame { background: transparent; border: none; }

/* ---------- Títulos y etiquetas ---------- */
QLabel#title {
    font-size: 24px; font-weight: bold; letter-spacing: 3px;
}
QLabel#subtitle {
    font-size: 14px; font-style: italic; color: #6B4A2B;
}
QLabel#fieldLabel {
    font-size: 12px; font-weight: bold; letter-spacing: 1px;
}
QLabel#placeholder {
    font-size: 16px; font-style: italic; color: #6B4A2B;
}
QLabel#error {
    color: #B5301F; font-style: italic; font-weight: bold;
}

/* ---------- Botones y combobox ---------- */
QPushButton, QComboBox {
    background: #F7E394;
    border: 2px solid #2B1B0E;
    border-radius: 12px;
    padding: 6px 16px;
    font-weight: bold;
    min-height: 22px;
}
QPushButton:hover, QComboBox:hover { background: #FFF0A8; }
QPushButton:pressed { background: #E6C34A; }
QPushButton:disabled {
    background: #D9C27A; color: #8C7A55; border-color: #8C7A55;
}
QComboBox QAbstractItemView {
    background: #F7E394;
    border: 2px solid #2B1B0E;
    selection-background-color: #B5301F;
    selection-color: #FFF4C2;
    outline: none;
}

QPushButton#primary {
    background: #2F6B3A; color: #FFF4C2; border-color: #1C3F23;
}
QPushButton#primary:hover { background: #3B8248; }
QPushButton#primary:disabled {
    background: #8FA58F; color: #E7E7D0; border-color: #6B7F6B;
}
QPushButton#modify {
    color: #B5301F; border-color: #B5301F;
}
QPushButton#modify:checked {
    background: #B5301F; color: #FFF4C2;
}
QPushButton#modify:disabled {
    color: #A07068; border-color: #A07068;
}

/* ---------- Campos de texto ---------- */
QLineEdit {
    background: #FFF6CC;
    border: 2px solid #2B1B0E;
    border-radius: 10px;
    padding: 6px 10px;
    selection-background-color: #B5301F;
    selection-color: #FFF4C2;
}
QLineEdit:focus { border-color: #B5301F; }
QLineEdit#idField, QLineEdit#idField:read-only {
    background: #8C7A55; color: #FFF4C2; border: 2px solid #2B1B0E;
    border-radius: 10px; font-weight: bold;
}

/* ---------- Tarjeta de contacto ---------- */
QFrame#card {
    background: #FFF1B0;
    border: 3px solid #2B1B0E;
    border-radius: 28px;
}
QFrame#card QLineEdit:read-only {
    background: transparent; border: none; border-radius: 0;
    padding: 2px 4px;
}
QFrame#card QLineEdit#cardName {
    font-size: 20px; font-weight: bold;
}
QLabel#cardNumber {
    color: #B5301F; font-size: 22px; font-weight: bold; letter-spacing: 2px;
}
QFrame#cardSeparator { background: #2B1B0E; border: none; }

/* ---------- Diálogos ---------- */
QMessageBox, QDialog { background: #F1D56A; }
QToolTip {
    background: #FFF6CC; color: #2B1B0E; border: 1px solid #2B1B0E;
}
"""
