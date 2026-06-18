"""Display functions for the CLI"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def show_help():
    """Display command reference menu"""
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
    """Display table of all users with their project counts"""
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
    """Display all projects for a specific user with progress bars"""
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
    """Display all tasks in a project with status and assignee"""
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
    """Display progress dashboard for all users or specific user"""
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
    """Search for users, projects, or tasks matching query string"""
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
