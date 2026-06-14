#!/usr/bin/env python3
"""
Project Management CLI Tool
Run: python3 project_cli.py
"""

import json
import os
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
DATA_FILE = "projects.json"

# CLASSES

class Person:
    """ 𓍯𓂃Base class for any person in the system𓍯𓂃"""
    _next_id = 1
    
    def __init__(self, name, email=None):
        self._set_name(name)
        self._email = email
        self.id = Person._next_id
        Person._next_id += 1
    
    def _set_name(self, name):
        """𓍯𓂃Validate and set name𓍯𓂃"""
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
        """𓍯𓂃Validate email𓍯𓂃"""
        if value and '@' not in value:
            raise ValueError("Invalid email")
        self._email = value


class User(Person):
    """𓍯𓂃User who owns projects and tasks𓍯𓂃"""
    def __init__(self, name, email=None):
        super().__init__(name, email)
        self.projects = []
    
    def add_project(self, project):
        """𓍯𓂃Add project to user and give ownership𓍯𓂃"""
        project.owner = self
        self.projects.append(project)
    
    def find_project(self, title):
        """𓍯𓂃Find project by title (case insensitive)𓍯𓂃"""
        for p in self.projects:
            if p.title.lower() == title.lower():
                return p
        return None
    
    def to_dict(self):
        """𓍯𓂃Convert user object to dictionary for JSON storage𓍯𓂃"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'projects': [p.to_dict() for p in self.projects]
        }
    
    @classmethod
    def from_dict(cls, data):
        """𓍯𓂃Create User object from dictionary data𓍯𓂃"""
        user = cls(data['name'], data.get('email'))
        user.id = data['id']
        return user


class Project:
    """𓍯𓂃Project with tasks𓍯𓂃"""
    def __init__(self, title, description=""):
        self._set_title(title)
        self.description = description
        self.tasks = []
        self.owner = None
    
    def _set_title(self, title):
        """𓍯𓂃Validate and set project title𓍯𓂃"""
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
        """𓍯𓂃Add task to project and set project reference𓍯𓂃"""
        task.project = self
        self.tasks.append(task)
    
    def find_task(self, title):
        """𓍯𓂃Find task by title (case insensitive)𓍯𓂃"""
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None
    
    def progress(self):
        """𓍯𓂃Calculate percentage of all tasks completed𓍯𓂃"""
        if not self.tasks:
            return 0
        done = sum(1 for t in self.tasks if t.completed)
        return (done / len(self.tasks)) * 100
    
    def to_dict(self):
        """𓍯𓂃Convert project to dictionary for JSON storage𓍯𓂃"""
        return {
            'title': self.title,
            'description': self.description,
            'tasks': [t.to_dict() for t in self.tasks]
        }
    
    @classmethod
    def from_dict(cls, data):
        """𓍯𓂃Create Project from dictionary data𓍯𓂃"""
        return cls(data['title'], data.get('description', ''))


class Task:
    """𓍯𓂃Individual task within a project𓍯𓂃"""
    def __init__(self, title, assignee=None):
        self._set_title(title)
        self.assignee = assignee
        self.completed = False
        self.project = None
    
    def _set_title(self, title):
        """𓍯𓂃Validate and set task title𓍯𓂃"""
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
        """𓍯𓂃Mark task as completed𓍯𓂃"""
        self.completed = True
    
    def to_dict(self):
        """𓍯𓂃Convert task to dictionary for JSON storage𓍯𓂃"""
        return {
            'title': self.title,
            'assignee': self.assignee,
            'completed': self.completed
        }
    
    @classmethod
    def from_dict(cls, data):
        """𓍯𓂃Create Task from dictionary data𓍯𓂃"""
        task = cls(data['title'], data.get('assignee'))
        task.completed = data.get('completed', False)
        return task


# STORAGE FUNCTIONS

def save_data(users):
    """𓍯𓂃Save all user data to JSON file𓍯𓂃"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump([u.to_dict() for u in users], f, indent=2)
        return True
    except Exception as e:
        console.print(f"[red]Save error: {e}[/red]")
        return False

def load_data():
    """𓍯𓂃Load all user data from JSON file𓍯𓂃"""
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
        console.print(f"[red]Load error: {e}[/red]")
        return []


# DISPLAY FUNCTIONS

def show_help():
    """𓍯𓂃Display command reference menu𓍯𓂃"""
    console.print("""
╔══════════════════════════════════════════════════════════╗
║  PROJECT MANAGER           REFERENCE                     ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  USER COMMANDS:                                          ║
║    add-user NAME        Create new user                  ║
║    set-email USER EMAIL Update user email                ║
║    list-users           Show all users                   ║
║                                                          ║
║  PROJECT COMMANDS:                                       ║
║    add-project USER TITLE   Add project to user          ║
║    list-projects USER       Show user's projects         ║
║                                                          ║
║  TASK COMMANDS:                                          ║
║    add-task USER PROJ TASK [--assignee NAME]             ║
║    list-tasks USER PROJ      Show tasks                  ║
║    done USER PROJ TASK       Mark task complete          ║
║    reassign USER PROJ TASK NEW  Reassign task            ║
║                                                          ║
║  VIEW COMMANDS:                                          ║
║    dashboard [USER]         Progress dashboard           ║
║    search WORD              Find anything                ║
║    help                    This menu                     ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

EXAMPLES:
  add-user Beatrice
  set-email Beatrice beatrice@email.com
  add-project Beatrice Web App
  add-task Beatrice Web App "Design" --assignee Beatrice
  reassign Beatrice Web App "Design" Bob
  done Beatrice Web App "Design"
  dashboard
""")

def show_users(users):
    """𓍯𓂃Display table of all users with their project counts𓍯𓂃"""
    if not users:
        console.print("[yellow]No users. Try: add-user Name[/yellow]")
        return
    table = Table(title="TEAM MEMBERS", header_style="bold cyan")
    table.add_column("ID", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Projects", justify="center")
    for u in users:
        table.add_row(str(u.id), u.name, u.email or "-", str(len(u.projects)))
    console.print(table)

def show_projects(user):
    """𓍯𓂃Display all projects for a specific user with progress bars𓍯𓂃"""
    if not user.projects:
        console.print(f"[yellow]No projects for {user.name}[/yellow]")
        return
    table = Table(title=f"PROJECTS: {user.name}", header_style="bold cyan")
    table.add_column("Title", style="green")
    table.add_column("Tasks", justify="center")
    table.add_column("Done", justify="center")
    table.add_column("Progress", width=25)
    for p in user.projects:
        total = len(p.tasks)
        done = sum(1 for t in p.tasks if t.completed)
        percent = p.progress()
        bar = "█" * int(percent/5) + "░" * (20 - int(percent/5))
        table.add_row(p.title, str(total), f"{done}/{total}", f"[green]{bar}[/green] {percent:.0f}%")
    console.print(table)

def show_tasks(project):
    """𓍯𓂃Display all tasks in a project with status and assignee𓍯𓂃"""
    if not project.tasks:
        console.print(f"[yellow]No tasks for {project.title}[/yellow]")
        return
    table = Table(title=f"TASKS: {project.title}", header_style="bold cyan")
    table.add_column("Status", width=10)
    table.add_column("Task", style="green")
    table.add_column("Assignee", style="blue")
    for t in project.tasks:
        status = "[green]✓ DONE[/green]" if t.completed else "[red]○ PENDING[/red]"
        table.add_row(status, t.title, t.assignee or "unassigned")
    console.print(table)

def show_dashboard(users, specific=None):
    """𓍯𓂃Display progress dashboard for all users or specific user𓍯𓂃"""
    if specific:
        users = [u for u in users if u.name.lower() == specific.lower()]
        if not users:
            console.print(f"[red]User '{specific}' not found[/red]")
            return
    if not users:
        console.print("[yellow]No data[/yellow]")
        return
    
    console.print("\n[bold cyan]PROJECT DASHBOARD[/bold cyan]")
    console.print("-" * 45)
    
    total_projects = total_tasks = total_done = 0
    for u in users:
        u_tasks = sum(len(p.tasks) for p in u.projects)
        u_done = sum(1 for p in u.projects for t in p.tasks if t.completed)
        total_projects += len(u.projects)
        total_tasks += u_tasks
        total_done += u_done
        rate = (u_done / u_tasks * 100) if u_tasks > 0 else 0
        bar = "█" * int(rate/5) + "░" * (20 - int(rate/5))
        console.print(f"\n[bold green]{u.name}[/bold green] [{bar}] {rate:.0f}%")
        console.print(f"  📁 {len(u.projects)} projects | 📋 {u_tasks} tasks | ✅ {u_done} done")
        for p in u.projects[:2]:
            console.print(f"    └─ {p.title} [{p.progress():.0f}%]")
        if len(u.projects) > 2:
            console.print(f"    └─ ... and {len(u.projects)-2} more")
    
    if total_tasks > 0:
        console.print(f"\n[bold]OVERALL:[/bold] {total_projects} projects, {total_tasks} tasks, {(total_done/total_tasks*100):.0f}% complete")

def search_all(users, query):
    """𓍯𓂃Search for users, projects, or tasks matching query string𓍯𓂃"""
    q = query.lower()
    results = []
    for u in users:
        if q in u.name.lower():
            results.append(("USER", u.name, f"ID: {u.id}"))
        for p in u.projects:
            if q in p.title.lower():
                results.append(("PROJECT", p.title, f"Owner: {u.name}"))
            for t in p.tasks:
                if q in t.title.lower():
                    results.append(("TASK", t.title, f"Project: {p.title}"))
    if not results:
        console.print(f"[yellow]No results for '{query}'[/yellow]")
        return
    table = Table(title=f"Search: '{query}'")
    table.add_column("Type", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Context", style="dim")
    for r in results:
        table.add_row(*r)
    console.print(table)


# MAIN CLI

def main():
    """𓍯𓂃Main entry point for CLI𓍯𓂃"""
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    # 𓍯𓂃Define all commands and their arguments𓍯𓂃
    subparsers.add_parser("help", help="Show help")
    
    p = subparsers.add_parser("add-user")
    p.add_argument("name")
    p.add_argument("--email")
    
    subparsers.add_parser("list-users")
    
    p = subparsers.add_parser("add-project")
    p.add_argument("user")
    p.add_argument("title")
    
    p = subparsers.add_parser("list-projects")
    p.add_argument("user")
    
    p = subparsers.add_parser("add-task")
    p.add_argument("user")
    p.add_argument("project")
    p.add_argument("title")
    p.add_argument("--assignee")
    
    p = subparsers.add_parser("list-tasks")
    p.add_argument("user")
    p.add_argument("project")
    
    p = subparsers.add_parser("done")
    p.add_argument("user")
    p.add_argument("project")
    p.add_argument("task")
    
    p = subparsers.add_parser("dashboard")
    p.add_argument("user", nargs="?")
    
    p = subparsers.add_parser("search")
    p.add_argument("query")
    
    # New feature commands
    p = subparsers.add_parser("set-email")
    p.add_argument("user")
    p.add_argument("email")
    
    p = subparsers.add_parser("reassign")
    p.add_argument("user")
    p.add_argument("project")
    p.add_argument("task")
    p.add_argument("new_assignee")
    
    args = parser.parse_args()
    users = load_data()
    
    console.print(Panel.fit("[bold cyan]PROJECT MANAGER[/bold cyan]\n[dim]Type 'help' for commands[/dim]", border_style="blue"))
    
    if not args.command or args.command == "help":
        show_help()
        return
    
    # 𓍯𓂃Command handlers𓍯𓂃
    if args.command == "add-user":
        try:
            if any(u.name.lower() == args.name.lower() for u in users):
                console.print(f"[red]User '{args.name}' exists[/red]")
                return
            users.append(User(args.name, args.email))
            save_data(users)
            console.print(f"[green]User '{args.name}' created[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
    
    elif args.command == "set-email":
        """𓍯𓂃Update email for existing user𓍯𓂃"""
        u = next((x for x in users if x.name.lower() == args.user.lower()), None)
        if not u:
            console.print(f"[red]User '{args.user}' not found[/red]")
            return
        try:
            u.email = args.email
            save_data(users)
            console.print(f"[green]Email for {u.name} set to {u.email}[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
    
    elif args.command == "list-users":
        show_users(users)
    
    elif args.command == "add-project":
        u = next((x for x in users if x.name.lower() == args.user.lower()), None)
        if not u:
            console.print(f"[red]User '{args.user}' not found[/red]")
            return
        try:
            if u.find_project(args.title):
                console.print(f"[red]Project '{args.title}' exists[/red]")
                return
            u.add_project(Project(args.title))
            save_data(users)
            console.print(f"[green]Project '{args.title}' added to {u.name}[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
    
    elif args.command == "list-projects":
        u = next((x for x in users if x.name.lower() == args.user.lower()), None)
        if u:
            show_projects(u)
        else:
            console.print(f"[red]User '{args.user}' not found[/red]")
    
    elif args.command == "add-task":
        u = next((x for x in users if x.name.lower() == args.user.lower()), None)
        if not u:
            console.print(f"[red]User '{args.user}' not found[/red]")
            return
        p = u.find_project(args.project)
        if not p:
            console.print(f"[red]Project '{args.project}' not found[/red]")
            return
        try:
            if p.find_task(args.title):
                console.print(f"[red]Task '{args.title}' exists[/red]")
                return
            p.add_task(Task(args.title, args.assignee))
            save_data(users)
            console.print(f"[green]Task '{args.title}' added[/green]")
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
    
    elif args.command == "list-tasks":
        u = next((x for x in users if x.name.lower() == args.user.lower()), None)
        if not u:
            console.print(f"[red]User '{args.user}' not found[/red]")
            return
        p = u.find_project(args.project)
        if p:
            show_tasks(p)
        else:
            console.print(f"[red]Project '{args.project}' not found[/red]")
    
    elif args.command == "reassign":
        """𓍯𓂃Transfer task ownership to diff user𓍯𓂃"""
        u = next((x for x in users if x.name.lower() == args.user.lower()), None)
        if not u:
            console.print(f"[red]User '{args.user}' not found[/red]")
            return
        p = u.find_project(args.project)
        if not p:
            console.print(f"[red]Project '{args.project}' not found[/red]")
            return
        t = p.find_task(args.task)
        if not t:
            console.print(f"[red]Task '{args.task}' not found[/red]")
            return
        
        new_user = next((x for x in users if x.name.lower() == args.new_assignee.lower()), None)
        if not new_user:
            console.print(f"[red]Assignee '{args.new_assignee}' not found[/red]")
            return
        
        old_assignee = t.assignee or "unassigned"
        t.assignee = args.new_assignee
        save_data(users)
        console.print(f"[cyan]Task reassigned: {old_assignee} -> {args.new_assignee}[/cyan]")
    
    elif args.command == "done":
        """𓍯𓂃Mark task complete with celebration message𓍯𓂃"""
        u = next((x for x in users if x.name.lower() == args.user.lower()), None)
        if not u:
            console.print(f"[red]User '{args.user}' not found[/red]")
            return
        p = u.find_project(args.project)
        if not p:
            console.print(f"[red]Project '{args.project}' not found[/red]")
            return
        t = p.find_task(args.task)
        if not t:
            console.print(f"[red]Task '{args.task}' not found[/red]")
            return
        if t.completed:
            console.print("[yellow]Task already done[/yellow]")
            return
        t.mark_done()
        save_data(users)
        
        # 𓍯𓂃Celebration feedback𓍯𓂃
        console.print(f"\n[bold green]Task '{t.title}' COMPLETED![/bold green]")
        
        import random
        messages = [
            "🔥AMAZING! You're on fire!",
            "💪CRUSHING IT! Employee of the month maybe?",
            "📈GOAL ACHIEVED! What's next?",
            "📊PROGRESS! You're unstoppable!"
        ]
        console.print(f"[bold cyan]{random.choice(messages)}[/bold cyan]")
        
        print('\a', end='', flush=True)  # System bell sound
        
        console.print(f"[dim]Project now {p.progress():.0f}% complete[/dim]")
        remaining = len([t for t in p.tasks if not t.completed])
        console.print(f"[dim]Tasks remaining: {remaining}[/dim]\n")
    
    elif args.command == "dashboard":
        show_dashboard(users, args.user)
    
    elif args.command == "search":
        search_all(users, args.query)

if __name__ == "__main__":
    main()