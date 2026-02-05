# Data Model: Todo CLI App

## Task Entity

### Attributes
- **id** (int): Unique identifier for each task, auto-incremented
- **title** (str): Title of the task, required field
- **description** (str): Detailed description of the task, optional field
- **status** (bool): Completion status (True for complete, False for incomplete)

### Relationships
- None (standalone entity)

### Constraints
- id: Must be unique and positive integer
- title: Must not be empty
- status: Must be boolean value

## TaskList Collection

### Structure
- Internal storage: Dictionary mapping ID to Task objects for O(1) lookup
- Sequential ID generation: Track next available ID

### Operations
- Add task: Insert with auto-generated unique ID
- Get task: Retrieve by ID
- Update task: Modify existing task by ID
- Delete task: Remove by ID
- List all: Return all tasks in insertion order