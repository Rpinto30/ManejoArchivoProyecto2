import re
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
    
    
    @property
    def id(self):
        return self.id
    @id.setter
    def id(self, id: int):
        self.id = id
    
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
            
    
    
    def __str__(self):
        print(f""" ID: {self.id}
    - name: {self.name}
    - phone: {self.phone}
    - email: {self.email}
    - city: {self.city}
""")
        
    def get_json(self) -> dict:
        return  {
            self.id : {
                "name" : self.name,
                "phone" : self.phone,
                "email" : self.email,
                "city" : self.city
            }
        }