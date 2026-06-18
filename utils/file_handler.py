"""File handling utilities for JSON persistence"""

import json
import os
from models.user import User
from models.project import Project
from models.task import Task

DATA_FILE = "data/projects.json"

def save_data(users):
    """Save all user data to JSON file"""
    try:
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump([u.to_dict() for u in users], f, indent=2)
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False

def load_data():
    """Load all user data from JSON file"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        users = []
        for user_data in data:
            user = User.from_dict(user_data)
            for project_data in user_data.get('projects', []):
                project = Project.from_dict(project_data)
                for task_data in project_data.get('tasks', []):
                    task = Task.from_dict(task_data)
                    project.add_task(task)
                user.add_project(project)
            users.append(user)
        return users
    except Exception as e:
        print(f"Load error: {e}")
        return []