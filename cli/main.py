import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#!/usr/bin/env python3
"""
Project Management CLI Tool
Run: python3 cli/main.py
"""
import pyfiglet
import argparse
import random
from rich.console import Console
from rich.panel import Panel


from models.user import User
from models.project import Project
from models.task import Task
from utils.file_handler import save_data, load_data
from cli.display import (
    show_help, show_users, show_projects, show_tasks, 
    show_dashboard, search_all
)

console = Console()

def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    # Define all commands and their arguments
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
    
    # Command handlers
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
        
        # Celebration feedback
        console.print(f"\n[bold green]Task '{t.title}' COMPLETED![/bold green]")
        
        messages = [
            "🔥AMAZING! You're on fire!",
            "💪CRUSHING IT! Employee of the month maybe?",
            "📈GOAL ACHIEVED! What's next?",
            "📊PROGRESS! You're unstoppable!"
        ]
        console.print(f"[bold cyan]{random.choice(messages)}[/bold cyan]")
        console.print(pyfiglet.figlet_format("DONE!", font="slant"))
        
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