import re
import struct
"""
ID = 4 i
NAME = 30 s
PHONE = 9 s
EMAIL = 17 s
CITY = 40 s
"""
class Contact:
    __FORMAT = "<i30s9s17s40s"
    def __init__(self, 
        id, name, phone, email, city
    ):
        self.id:int = id
        self.name:str = name
        self.phone:str = phone
        self.email:str = email
        self.city:str = city
    
   
    
    def __str__(self):
        return f""" ID: {self.id}
    - name: {self.name}
    - phone: {self.phone}
    - email: {self.email}
    - city: {self.city}"""
        
    def setJson(self) -> dict:
        return  {
                "id": self.id,
                "name" : self.name,
                "phone" : self.phone,
                "email" : self.email,
                "city" : self.city
            }

    def setBytes(self) -> bytes:
        return struct.pack(self.__FORMAT, 
                           self.id, self.name.encode("utf-8"), 
                           self.phone.encode("utf-8"), 
                           self.email.encode("utf-8"), 
                           self.city.encode("utf-8"))

    
    @staticmethod
    def format():
        return "<i30s9s17s40s"

    @staticmethod
    def calcSize():
        return struct.calcsize("<i30s9s17s40s")


"""

@property
def name(self):
    return self.name
@name.setter
def name(self, name: str):
    self.name = name[:30]
    
@property
def phone(self):
    return self.phone
@phone.setter
def phone(self, phone: str):
    if re.match("^\d{4}-\d{4}$", phone):
        self.phone = phone
@property
def email(self):
    return self.email
@email.setter
def email(self, email: str):
    if re.match("^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,6}$", email):
        self.email = email
        
"""

