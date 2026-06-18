# Project Management CLI Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue)]()

A terminal-based project management system for tracking users, projects, and tasks with progress visualization.

<img src="https://github.com/user-attachments/assets/bd35dd3e-4d24-460a-8945-faedef4438e9" width="600" alt="terminal_demo">

## Live Documentation

[View User Guide](https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/docs/guide.html)

## Features

- User management with email support
- Project and task tracking
- Task assignment and reassignment
- Progress dashboard with visual completion bars
- Search functionality across all data
- Celebration messages and sound on task completion
- Persistent JSON storage

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ToniMoringa/SL_Management_CLI_Tool
cd project-management-cli
```

2. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3.Install dependencies:

```bash
pip install rich
```

Usage
Run the tool:

```bash
python3 cli/main.py
```

## Data Storage

-All data is stored in projects.json in the same directory.
-The file is created automatically on first save.

## Running Tests

bash
python3 test_cli.py

## Dependencies

rich>=15.0.0 - Terminal formatting and colors

## License

MIT License

## Author

Toni Muthwa
