from services.contact import Contact
from persistent.concat_save import RepoContact
from pathlib import Path
import os
import json

FOLDER_EXPORT = Path("export")

def exportJSON(repo: RepoContact):
    l = []
    for key  in repo.getIndex().getIndex():
        data = repo.loadByID(key)
        l.append(data.setJson())
        
    if len(l) > 0:
        FOLDER_EXPORT.mkdir(parents=True, exist_ok=True)
        with open(FOLDER_EXPORT / "contactos.json", 'w', encoding='utf-8') as file:
            json.dump(l, file, ensure_ascii=False, indent=4)