import struct
import os
import shutil
import json
import hashlib
from services.contact import Contact
from pathlib import Path

"""
tmaño fijo
- indices.json
- contactos.dat
- contactos.sha256
"""


class ContactsFile:
    def __init__(self, PATH, PATH_TEMP, PATH_BACKUP):
        self.PATH = PATH
        self.PATH_TEMP = PATH_TEMP
        self.PATH_BACKUP = PATH_BACKUP
    
    
    def save(self, contactBytes:bytes):
        try:
            if os.path.exists(self.PATH) and not os.path.exists(self.PATH_TEMP):
                shutil.copy2(self.PATH, self.PATH_TEMP)

            with open(self.PATH_TEMP, 'ab') as file:
                file.write(contactBytes)
                
            if os.path.exists(self.PATH_TEMP):
                shutil.copy2(self.PATH_TEMP, self.PATH_BACKUP)
                os.replace(self.PATH_TEMP, self.PATH)

        except Exception as e:
            print(f"Error detectado durante el guardado: {e}")
            if os.path.exists(self.PATH_TEMP):
                try:
                    os.replace(self.PATH_TEMP, self.PATH)
                except Exception:
                    pass
    
    
    def update(self, contact:Contact, pos):
        with open(self.PATH, 'r+b') as file:
            file.seek(pos)
            file.write(
                contact.setBytes()
            )
    
    def read(self, format:str, size:int, pos):
        with open(self.PATH, 'rb') as file:
            file.seek(pos)
            b = file.read(size)
            data = struct.unpack(format, b)
        
        return Contact(
            data[0],
            data[1].decode('utf-8').rstrip('\x00'),
            data[2].decode('utf-8').rstrip('\x00'),
            data[3].decode('utf-8').rstrip('\x00'),
            data[4].decode('utf-8').rstrip('\x00')
        )
            
    def getLastPos(self):
        try:
            with open(self.PATH, 'rb') as file:
                file.seek(0, 2)
                pos = file.tell()
            return pos
        except:
            return 0
    

class IndexContact:
    __index = {}
    
    def __init__(self, PATH, PATH_TEMP, PATH_BACKUP):
        self.PATH = PATH
        self.PATH_TEMP = PATH_TEMP
        self.PATH_BACKUP = PATH_BACKUP
        self.loadConcatIndex()
    
    #write __index in index.json
    def setContact(self, contact:Contact, pos):
        self.loadConcatIndex()
        if str(contact.id) in self.__index:
            raise Exception(f"El ID {contact.id} ya se encuentra ocupado")
        
        self.__index[str(contact.id)] = pos
        try:
            with open(self.PATH_TEMP, 'w', encoding='utf-8') as file:
                json.dump(self.__index, file, indent=4)
            
            if os.path.exists(self.PATH_TEMP):
                if os.path.exists(self.PATH):
                    shutil.copy2(self.PATH, self.PATH_BACKUP)
                shutil.copy2(self.PATH_TEMP, self.PATH_BACKUP)
                os.replace(self.PATH_TEMP, self.PATH)
        except Exception as e:
            print(f"Error detectado durante el guardado: {e}")
            if os.path.exists(self.PATH_TEMP):
                try:
                    os.replace(self.PATH_TEMP, self.PATH)
                except Exception:
                    pass
    
    #update __index from index.json
    def loadConcatIndex(self):
        try:
            if os.path.exists(self.PATH):
                with open(self.PATH, 'r', encoding='utf-8') as fileIndex:
                    self.__index = json.load(fileIndex) 
        except Exception:
            if os.path.exists(self.PATH_BACKUP):
                try:
                    shutil.copy2(self.PATH_BACKUP, self.PATH)
                    with open(self.PATH, 'r', encoding='utf-8') as fileIndex:
                        self.__index = json.load(fileIndex)
                except Exception:
                    self.__index = {}
            else:
                self.__index = {}
        
    def getPosByID(self, id):
        print(self.__index)
        print(str(id) in self.__index, id)
        if str(id) in self.__index:
            return self.__index[str(id)]
        return -1
    
    def getNextKey(self):
        return max(map(int, self.__index.keys()), default=-1) + 1
        
    def getIndex(self):
        return self.__index
        
        
class HashContact:
    def __init__(self, PATH_HASH, PATH_FOLDER, PATH_TEMP, PATH_BACKUP):
        self.PATH_HASH = PATH_HASH / "contacts.sha256"
        self.PATH_FOLDER = PATH_FOLDER
        self.PATH_TEMP = PATH_TEMP
        self.PATH_BACKUP = PATH_BACKUP
    
    def blocks(self, path):
        with open(path, "rb") as file:
            c = file.read()
            sha256 = hashlib.sha256(c)
                
            while True:
                b = file.read(4096)
                if not b: break
                sha256.update(b)
        return sha256.hexdigest()

    def comparacion(self):
        lis = [f for f in self.PATH_FOLDER.iterdir() if f.is_file()]
        
        old_ = []
        try:
            with open(self.PATH_HASH, 'r', encoding='utf-8') as reader:
                for l in reader.readlines():
                    old_.append(l.split("|"))
        except Exception:
            if os.path.exists(self.PATH_BACKUP):
                shutil.copy2(self.PATH_BACKUP, self.PATH_HASH)
                with open(self.PATH_HASH, 'r', encoding='utf-8') as reader:
                    for l in reader.readlines():
                        old_.append(l.split("|"))

        with open(self.PATH_HASH, 'w', encoding='utf-8') as file:
            for l in lis:    
                for l2 in old_:
                    if l2[0] == str(l) or l2[0].endswith(l.name):
                        if self.blocks(l) != l2[1].replace('\n',''):
                            print(l.name, "-> MODIFICADO")
                        else:
                            print(l.name, " -> INTEGRO")
        self.generate()
        

    def generate(self):
        try:
            lis = [f for f in self.PATH_FOLDER.iterdir() if f.is_file()]
            with open(self.PATH_TEMP, 'w', encoding='utf-8') as file:
                for l in lis:
                    file.write(
                        f"{self.PATH_FOLDER / l.name}|{self.blocks(l)}\n"
                    )
            
            if os.path.exists(self.PATH_TEMP):
                if os.path.exists(self.PATH_HASH):
                    shutil.copy2(self.PATH_HASH, self.PATH_BACKUP)
                shutil.copy2(self.PATH_TEMP, self.PATH_BACKUP)
                os.replace(self.PATH_TEMP, self.PATH_HASH)
        except Exception as e:
            print(f"Error detectado durante el guardado: {e}")
            if os.path.exists(self.PATH_TEMP):
                try:
                    os.replace(self.PATH_TEMP, self.PATH_HASH)
                except Exception:
                    pass

    def compare(self, path):
        try:
            if not os.path.exists(self.PATH_HASH) and os.path.exists(self.PATH_BACKUP):
                shutil.copy2(self.PATH_BACKUP, self.PATH_HASH)
        except Exception:
            pass

        target_path = str(Path("data") / path)
        hash_file = None

        try:
            with open(self.PATH_HASH, 'r', encoding='utf-8') as file:
                for line in file:
                    data = line.strip().split('|') 
                    if data[0] == target_path:
                        hash_file = data[1]
                        break
        except Exception:
            if os.path.exists(self.PATH_BACKUP):
                shutil.copy2(self.PATH_BACKUP, self.PATH_HASH)
                with open(self.PATH_HASH, 'r', encoding='utf-8') as file:
                    for line in file:
                        data = line.strip().split('|') 
                        if data[0] == target_path:
                            hash_file = data[1]
                            break

        if hash_file is None:
            print(f"Ruta no encontrada en el registro de hashes: {target_path}")
            return False
        
        current_hash = self.blocks(Path("data") / path)
        if str(current_hash) == hash_file:
            return True
            
        return False
        
class RepoContact:
    def __init__(self,
                 PATH_FILE:str, #data/contact.dat
                 PATH_TEMP_FILE: str, #data/contact.temp.dat
                 PATH_BACKUP_FILE, #backup/contact.dat.bak
                 
                 PATH_INDEX:str, #data/index.json
                 PATH_INDEX_TEMP_FILE: str, #data/index.temp.json
                 PATH_INDEX_BACKUP_FILE: str, #backup/index.json.bak
                 
                 PATH_DATA, #data
                 PATH_HASH, #.ignore/contact.sha256
                 PATH_HASH_TEMP, #.ignore/contact.temp.sha256
                 PATH_HASH_BAK #.ignore/contact.sha256.bak
                 ):  
        self.__index = IndexContact(
            PATH_INDEX, PATH_INDEX_TEMP_FILE, PATH_INDEX_BACKUP_FILE
        ) 
        self.__contactFile = ContactsFile(
            PATH_FILE, PATH_TEMP_FILE, PATH_BACKUP_FILE
        )
        self.__hash = HashContact(
            PATH_HASH, PATH_DATA, PATH_HASH_TEMP, PATH_HASH_BAK
        )
        
        
    def write(self, contact:Contact):
        try:
            self.__index.setContact(contact, self.__contactFile.getLastPos())
            self.__contactFile.save(contact.setBytes())
        except:
            self.__contactFile.update(
                contact,
                self.__index.getPosByID(contact.id)
                )
        finally:
            self.__hash.generate()
        
    def update(self, contact:Contact):
        self.__contactFile.update(
                    contact,
                    self.__index.getPosByID(contact.id)
                    )
        self.__hash.generate()

    def loadByID(self, id):
        pos = self.__index.getPosByID(id)
        if pos != -1:
            return self.__contactFile.read(Contact.format(), Contact.calcSize(), pos)
        return None
    
    def getAutoIncrementKey(self):
        return self.__index.getNextKey()
    
    def getIndex(self):
        return self.__index
    
    
    #hash
    def genHash(self):
        self.__hash.generate()
    
    """
    only: data/ ... (FILE)
    """
    def comparePersistent(self, path) -> int:
        if os.path.exists(str(Path("data") / path)):
            return  0 if self.__hash.compare(path) else 1
        else: return -1
    
    
    def getPathData(self):
        return self.__hash.PATH_FOLDER