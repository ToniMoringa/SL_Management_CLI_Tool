"""Base Person class - parent for all people in the system"""

class Person:
    """Base class for any person in the system"""
    _next_id = 1
    
    def __init__(self, name, email=None):
        self._set_name(name)
        self._email = email
        self.id = Person._next_id
        Person._next_id += 1
    
    def _set_name(self, name):
        """Validate and set name"""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        self._name = name.strip()
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._set_name(value)
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        """Validate email"""
        if value and '@' not in value:
            raise ValueError("Invalid email")
        self._email = value

