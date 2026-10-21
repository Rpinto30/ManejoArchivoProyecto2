import sys
from pathlib import Path

#views
from PySide6.QtWidgets import QApplication
from views import APP_STYLE, MainWindow
from report.reports import exportJSON

#services
from services.contact import Contact
from persistent.concat_save import RepoContact

#PATH
FOLDER_DATA = Path("data")
PATH_FILE_DATA = FOLDER_DATA / "contact.dat"
PATH_FILE_DATA_TEMP = FOLDER_DATA / "contact.temp.dat"
PATH_FILE_DATA_BAK = FOLDER_DATA / "contact.dat.bak"

PATH_FILE_INDEX = FOLDER_DATA / "index.json"
PATH_FILE_INDEX_TEMP = FOLDER_DATA / "index.temp.json"
PATH_FILE_INDEX_BAK = FOLDER_DATA / "index.json.bak"

PATH_LOG_HASH = Path(".ignore")

def main():
    repo = RepoContact(
        PATH_FILE_DATA, PATH_FILE_DATA_TEMP, PATH_FILE_DATA_BAK,
        PATH_FILE_INDEX, PATH_FILE_INDEX_TEMP, PATH_FILE_INDEX_BAK,
        FOLDER_DATA, PATH_LOG_HASH
    )
    
    c = Contact(
        0, "PEPE", "1234-1523", "email.correo@correo.gmail.com", "CUIDAD DE LOS ALTOS"
    )
    c2 = Contact(
            2, "RODRIGO", "0000-0000", "email.correo@correo.gmail.com", "sixseve"
        )
    c3 = Contact(
                1, "este será el no 1", "6666-7777", "email.correo@correo.gmail.com", "GUATEMALA"
            )
    
    
    print(repo.comparePersistent("contact.dat"))
    repo.write(c)
    repo.write(c2)
    repo.write(c3)
    
    repo.loadByID(1)
    
    c2.email = "corerrro@gmail.com"
    c2.phone = "7790-0000"
    repo.update(c2)
    exportJSON(repo)
    #app = QApplication(sys.argv)
    #app.setStyleSheet(APP_STYLE)
    #window = MainWindow()
    #window.show()
    #sys.exit(app.exec())
    repo.genHash()


if __name__ == "__main__":
    main()
