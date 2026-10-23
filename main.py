import sys
from pathlib import Path

#views
from PySide6.QtWidgets import QApplication
from views import APP_STYLE, MainWindow


#services
from services.contact import Contact
from persistent.concat_save import RepoContact

#PATH
FOLDER_DATA = Path("data")
FOLDER_BAK_DATA = Path("backup")



PATH_FILE_DATA = FOLDER_DATA / "contact.dat"
PATH_FILE_DATA_TEMP = FOLDER_DATA / "contact.temp.dat"
PATH_FILE_DATA_BAK = FOLDER_BAK_DATA / "contact.dat.bak"

PATH_FILE_INDEX = FOLDER_DATA / "index.json"
PATH_FILE_INDEX_TEMP = FOLDER_DATA / "index.temp.json"
PATH_FILE_INDEX_BAK = FOLDER_BAK_DATA / "index.json.bak"

PATH_LOG_HASH = Path(".ignore")
PATH_LOG_HASH_TEMP = Path(".ignore/contact.temp.sha256")
PATH_LOG_HASH_BAK = Path(".ignore/contact.sha256.bak")

FOLDER_DATA.mkdir(parents=True, exist_ok=True)
FOLDER_BAK_DATA.mkdir(parents=True, exist_ok=True)
PATH_LOG_HASH.mkdir(parents=True, exist_ok=True)

def main():
    repo = RepoContact(
        PATH_FILE_DATA, PATH_FILE_DATA_TEMP, PATH_FILE_DATA_BAK,
        PATH_FILE_INDEX, PATH_FILE_INDEX_TEMP, PATH_FILE_INDEX_BAK,
        FOLDER_DATA, PATH_LOG_HASH, PATH_LOG_HASH_TEMP, PATH_LOG_HASH_BAK
    )
    
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    window = MainWindow(repo)
    window.show()
    sys.exit(app.exec())
    repo.genHash()


if __name__ == "__main__":
    main()
