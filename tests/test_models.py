import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from models.user import User
from models.project import Project
from models.task import Task

class TestProjectCLI(unittest.TestCase):
    
    def test_create_user(self):
        user = User("Alice")
        self.assertEqual(user.name, "Alice")
    
    def test_empty_name_raises_error(self):
        with self.assertRaises(ValueError):
            User("")
        with self.assertRaises(ValueError):
            User("   ")
    
    def test_invalid_email(self):
        user = User("Bob")
        with self.assertRaises(ValueError):
            user.email = "not-an-email"
    
    def test_add_project_to_user(self):
        user = User("Carol")
        project = Project("Website")
        user.add_project(project)
        self.assertIn(project, user.projects)
        self.assertEqual(project.owner, user)
    
    def test_add_task_to_project(self):
        project = Project("App")
        task = Task("Build UI")
        project.add_task(task)
        self.assertIn(task, project.tasks)
        self.assertEqual(task.project, project)
    
    def test_mark_task_done(self):
        task = Task("Test")
        self.assertFalse(task.completed)
        task.mark_done()
        self.assertTrue(task.completed)
    
    def test_project_progress(self):
        project = Project("Website")
        task1 = Task("Design")
        task2 = Task("Code")
        project.add_task(task1)
        project.add_task(task2)
        self.assertEqual(project.progress(), 0)
        task1.mark_done()
        self.assertEqual(project.progress(), 50)
        task2.mark_done()
        self.assertEqual(project.progress(), 100)
    
    def test_find_project(self):
        user = User("Dave")
        project = Project("Mobile App")
        user.add_project(project)
        found = user.find_project("Mobile App")
        self.assertEqual(found, project)
        self.assertIsNone(user.find_project("Nothing"))
    
    def test_find_task(self):
        project = Project("Backend")
        task = Task("Create API")
        project.add_task(task)
        found = project.find_task("Create API")
        self.assertEqual(found, task)
        self.assertIsNone(project.find_task("Missing"))

if __name__ == "__main__":
    unittest.main()