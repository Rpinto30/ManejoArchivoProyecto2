import zipfile, os
from persistent.concat_save import RepoContact
from pathlib import Path

def saveZIP(repo:RepoContact, pathSave):
    print("Comprimiendo...")
    data = None
    path = Path(str(pathSave)) / "backup_contacts.zip"
    try:
        repo_path = Path(repo.getPathData())
        
        with zipfile.ZipFile(
                path, 'w', compression=zipfile.ZIP_DEFLATED
            ) as zip:
                
                for file in os.listdir(repo_path):
                    file_path = repo_path / file
                    zip.write(file_path, arcname=file)
        
        origin = sum(f.stat().st_size for f in repo_path.glob('*') if f.is_file())
        c = path.stat().st_size
        
        r = ((origin - c) / origin) * 100 if origin > 0 else 0
        
        data = {
            "origin": origin,
            "zip": c,
            "per": max(0, r)
        }
    except Exception as e:
        print(f"Error durante la compresión: {e}")
    print("backup.zip creado exitosamente")
    return data