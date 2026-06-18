"""Task model - individual work item within a project"""

class Task:
    """Individual task within a project"""
    def __init__(self, title, assignee=None):
        self._set_title(title)
        self.assignee = assignee
        self.completed = False
        self.project = None
    
    def _set_title(self, title):
        """Validate and set task title"""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        self._title = title.strip()
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        self._set_title(value)
    
    def mark_done(self):
        """Mark task as completed"""
        self.completed = True
    
    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        return {
            'title': self.title,
            'assignee': self.assignee,
            'completed': self.completed
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Task from dictionary data"""
        task = cls(data['title'], data.get('assignee'))
        task.completed = data.get('completed', False)
        return task
