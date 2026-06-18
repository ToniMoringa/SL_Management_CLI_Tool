"""Project model - container for tasks"""

class Project:
    """Project with tasks"""
    def __init__(self, title, description=""):
        self._set_title(title)
        self.description = description
        self.tasks = []
        self.owner = None
    
    def _set_title(self, title):
        """Validate and set project title"""
        if not title or not title.strip():
            raise ValueError("Project title cannot be empty")
        self._title = title.strip()
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._set_title(value)
    
    def add_task(self, task):
        """Add task to project and set project reference"""
        task.project = self
        self.tasks.append(task)
    
    def find_task(self, title):
        """Find task by title (case insensitive)"""
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None
    
    def progress(self):
        """Calculate percentage of all tasks completed"""
        if not self.tasks:
            return 0
        done = sum(1 for t in self.tasks if t.completed)
        return (done / len(self.tasks)) * 100
    
    def to_dict(self):
        """Convert project to dictionary for JSON storage"""
        return {
            'title': self.title,
            'description': self.description,
            'tasks': [t.to_dict() for t in self.tasks]
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Project from dictionary data"""
        return cls(data['title'], data.get('description', ''))
