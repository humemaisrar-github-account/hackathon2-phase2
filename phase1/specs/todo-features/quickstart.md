# Quickstart: Todo CLI App

## Setup
1. Ensure Python 3.13+ is installed
2. Clone the repository
3. Navigate to the project directory

## Running the Application
```bash
cd src/cli
python main.py
```

## Basic Commands
- `add "title" "description"` - Add a new task
- `view` - View all tasks
- `update <id> "new title" "new description"` - Update a task
- `delete <id>` - Delete a task
- `complete <id>` - Mark task as complete
- `incomplete <id>` - Mark task as incomplete

## Example Usage
```bash
# Add a task
python main.py add "Buy groceries" "Milk, bread, eggs"

# View all tasks
python main.py view

# Mark task 1 as complete
python main.py complete 1

# Update task 1
python main.py update 1 "Buy groceries" "Milk, bread, eggs, fruits"
```