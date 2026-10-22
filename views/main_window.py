"""Ventana principal."""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QFrame, QLabel, QMainWindow,
                               QStackedWidget, QVBoxLayout, QWidget, QMessageBox, QFileDialog)

from .add_contact_view import AddContactView
from .contact_card import ContactCard
from .search_contact_view import SearchContactView
from .top_bar import TopBar

from services.contact import Contact
from persistent.concat_save import RepoContact

from report.reports import exportJSON, exportPDF

class MainWindow(QMainWindow):
    def __init__(self, repo: RepoContact):
        super().__init__()
        self.repo = repo
        self.setWindowTitle("Agenda de Contactos")
        self.resize(1000, 620)
        self.setMinimumSize(900, 560)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        # --- Barra superior ---
        self.top_bar = TopBar()

        # --- Panel izquierdo: FRAME cambiante ---
        self.card = ContactCard()
        self.card.hide()
        self.add_view = AddContactView()
        self.search_view = SearchContactView(self.card)

        placeholder = QLabel("Seleccione una opción\ndel menú «Contactos»")
        placeholder.setObjectName("placeholder")
        placeholder.setAlignment(Qt.AlignCenter)

        self.left_stack = QStackedWidget()
        self.left_stack.addWidget(placeholder)
        self.left_stack.addWidget(self.add_view)
        self.left_stack.addWidget(self.search_view)

        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(360)
        QVBoxLayout(left_panel).addWidget(self.left_stack)

        # --- Panel derecho: tarjeta ---
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.addStretch()
        right_layout.addWidget(self.card, 0, Qt.AlignHCenter)
        right_layout.addStretch()

        body = QHBoxLayout()
        body.setSpacing(12)
        body.addWidget(left_panel)
        body.addWidget(right_panel, 1)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)
        layout.addWidget(self.top_bar)
        layout.addLayout(body, 1)

        self._connect_signals()
        if not repo.comparePersistent("contact.dat"):
            QMessageBox.warning(self, "Datos Modificados", "Los datos fueron alterados fuera del sistema")

    def _connect_signals(self):
        tb = self.top_bar
        tb.contactsAction.connect(self._on_contacts_action)
        tb.toolsAction.connect(self._on_tools_action)
        tb.exportAction.connect(self._on_export_action)
        tb.helpClicked.connect(self.show_help)

        self.add_view.contactCreated.connect(self._on_contact_created)
        self.add_view.closed.connect(self._close_frame)

        self.search_view.searchRequested.connect(self._on_search_requested)
        self.search_view.contactUpdated.connect(self._on_contact_updated)
        self.search_view.closed.connect(self._close_frame)

    def _can_leave_current(self) -> bool:
        current = self.left_stack.currentWidget()
        return not hasattr(current, "can_leave") or current.can_leave()

    def _close_frame(self):
        self.card.hide()
        self.left_stack.setCurrentIndex(0)

    def _on_contacts_action(self, action: str):
        if not self._can_leave_current():
            return
        self.card.hide()
        if action == "add":
            self.add_view.prepare(self.get_next_id())
            self.left_stack.setCurrentWidget(self.add_view)
        elif action == "search":
            self.search_view.reset()
            self.left_stack.setCurrentWidget(self.search_view)

    def _on_tools_action(self, action: str):
        {"integrity": self.verify_integrity,
         "backup": self.create_zip_backup,
         "info": self.show_file_info}[action]()

    def _on_export_action(self, action: str):
        {"json": self.export_json, "report": self.create_report, "both": self.exportBoth}[action]()


    def _on_contact_created(self, data: dict):
        saved = self.save_contact(data) or data
        self.card.set_contact(saved)
        self.card.set_editable(False)
        self.card.show()
        self.add_view.prepare(self.get_next_id())

    def _on_search_requested(self, contact_id: int):
        self.search_view.show_result(self.find_contact(contact_id))

    def _on_contact_updated(self, data: dict):
        self.update_contact(data)


    #backend

    def get_next_id(self) -> int | None:
        return self.repo.getAutoIncrementKey()
        
    def save_contact(self, data: dict) -> dict | None:
        print(data)
        new_concat = Contact(
            data['id'],
            data['name'],
            data['phone'],
            data['email'],
            data['city']
        )
        
        
        self.repo.write(new_concat)
        QMessageBox.information(self, "Operación Exitosa", "Los datos se han guardado correctamente.")

    def find_contact(self, contact_id: int) -> dict | None:
        r = self.repo.loadByID(
            contact_id
        )
        
        if r != None:
            return r.setJson()
        else :
            return None
        
    def update_contact(self, data: dict) -> None:
        u_concat = Contact(
                data['id'],
                data['name'],
                data['phone'],
                data['email'],
                data['city']
            )
        self.repo.update(u_concat)
        QMessageBox.information(self, "Operación Exitosa", "Los datos se han guardado correctamente.")
        
    def verify_integrity(self) -> None:
        pass

    def create_zip_backup(self) -> None:
        pass

    def show_file_info(self) -> None:
        pass

    def export_json(self) -> None:
        dialog = QFileDialog(None, "Select Folders")
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_folders = dialog.selectedFiles() 
            try:
                exportJSON(self.repo, selected_folders[0])
                QMessageBox.information(self, "Operación Exitosa", f"Reporte JSON creado correctamente en:\n{selected_folders[0]}")
            except Exception as e:
                QMessageBox.critical(None, "Error al crear el reporte", f"Ha ocurrido un error inesperado al crear el reporte:\n {e}")
                
    def create_report(self) -> None:
        dialog = QFileDialog(None, "Select Folders")
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_folders = dialog.selectedFiles() 
            try:
                exportPDF(self.repo, selected_folders[0])
                QMessageBox.information(self, "Operación Exitosa", f"Reporte PDF creado correctamente en:\n{selected_folders[0]}")
            except Exception as e:
                QMessageBox.critical(None, "Error al crear el reporte", f"Ha ocurrido un error inesperado al crear el reporte:\n {e}")
                

    def exportBoth(self) -> None:
        dialog = QFileDialog(None, "Select Folders")
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_folders = dialog.selectedFiles() 
            try:
                exportJSON(self.repo, selected_folders[0])
                exportPDF(self.repo, selected_folders[0])
                QMessageBox.information(self, "Operación Exitosa", f"Reportes creados correctamente en:\n{selected_folders[0]}")
            except Exception as e:
                QMessageBox.critical(None, "Error al crear el reporte", f"Ha ocurrido un error inesperado al crear el reporte:\n {e}")
                

    def show_help(self) -> None:
        pass
    
