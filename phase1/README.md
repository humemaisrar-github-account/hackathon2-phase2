# Todo CLI Application

A command-line interface application for managing todo tasks. This application allows users to add, view, update, delete, and mark tasks as complete/incomplete using an in-memory storage system.

## Features

- **Add Tasks**: Create new tasks with a title and description
- **View Tasks**: Display all tasks with their status
- **Update Tasks**: Modify existing task titles and descriptions
- **Delete Tasks**: Remove tasks by ID
- **Mark Complete/Incomplete**: Change task completion status

## Requirements

- Python 3.13+

## Installation

1. Clone the repository
2. Navigate to the project directory
3. The application is ready to use (no external dependencies required)

## Usage

### Adding a Task
```bash
python -m src.cli.main add "Task Title" "Task Description"
```

### Viewing All Tasks
```bash
python -m src.cli.main view
```

### Updating a Task
```bash
python -m src.cli.main update <task_id> "New Title" "New Description"
```

### Deleting a Task
```bash
python -m src.cli.main delete <task_id>
```

### Marking a Task as Complete
```bash
python -m src.cli.main complete <task_id>
```

### Marking a Task as Incomplete
```bash
python -m src.cli.main incomplete <task_id>
```

## Examples

### Add a new task
```bash
python -m src.cli.main add "Buy groceries" "Milk, bread, eggs"
```

### View all tasks
```bash
python -m src.cli.main view
```

### Mark task #1 as complete
```bash
python -m src.cli.main complete 1
```

## Architecture

The application follows a clean architecture with three main layers:

- **Models**: Define the data structures (Task model)
- **Services**: Contain business logic (TodoService)
- **CLI**: Handle user input and output

## Testing

Unit and integration tests are available in the `tests/` directory:

```bash
# Run all tests
python -m pytest tests/

# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/
```