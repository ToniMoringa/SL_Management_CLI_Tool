"""User model - person who owns projects and tasks"""

from models.person import Person

class User(Person):
    """User who owns projects and tasks"""
    def __init__(self, name, email=None):
        super().__init__(name, email)
        self.projects = []
    
    def add_project(self, project):
        """Add project to user and give ownership"""
        project.owner = self
        self.projects.append(project)
    
    def find_project(self, title):
        """Find project by title (case insensitive)"""
        for p in self.projects:
            if p.title.lower() == title.lower():
                return p
        return None
    
    def to_dict(self):
        """Convert user object to dictionary for JSON storage"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'projects': [p.to_dict() for p in self.projects]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create User object from dictionary data"""
        user = cls(data['name'], data.get('email'))
        user.id = data['id']
        return user
