---
description: "Task list for Todo CLI application implementation"
---

# Tasks: Todo Features Implementation

**Input**: Design documents from `/specs/todo-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Tests**: Test tasks included as requested in feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are generated based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks are organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan: src/, tests/ directories
- [x] T002 [P] Create src/models/ directory
- [x] T003 [P] Create src/services/ directory
- [x] T004 [P] Create src/cli/ directory
- [x] T005 [P] Create src/lib/ directory
- [x] T006 [P] Create tests/unit/ directory
- [x] T007 [P] Create tests/integration/ directory
- [x] T008 [P] Create tests/contract/ directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 [P] Create Task model in src/models/task.py
- [x] T010 [P] Create TodoService in src/services/todo_service.py with empty methods
- [x] T011 Create CLI entry point in src/cli/main.py
- [x] T012 Create utility functions in src/lib/utils.py
- [x] T013 [P] Create unit test files: tests/unit/test_task.py and tests/unit/test_todo_service.py
- [x] T014 [P] Create integration test file: tests/integration/test_cli.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: User can create new tasks by providing a title and description, with unique ID assignment and initial "incomplete" status

**Independent Test**: Can be fully tested by adding a task and verifying it appears in the task list with a unique ID and "incomplete" status

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T015 [P] [US1] Create unit test for Task creation in tests/unit/test_task.py
- [x] T016 [P] [US1] Create unit test for TodoService.add_task method in tests/unit/test_todo_service.py
- [x] T017 [P] [US1] Create integration test for adding task via CLI in tests/integration/test_cli.py

### Implementation for User Story 1

- [x] T018 [P] [US1] Implement Task model with id, title, description, status attributes in src/models/task.py
- [x] T019 [US1] Implement TodoService.add_task method with unique ID generation in src/services/todo_service.py
- [x] T020 [US1] Add CLI command for adding tasks in src/cli/main.py
- [x] T021 [US1] Add validation for required title field in src/services/todo_service.py
- [x] T022 [US1] Add error handling for invalid inputs in src/services/todo_service.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P2)

**Goal**: User can see all tasks with their details including ID, title, description, and completion status

**Independent Test**: Can be fully tested by adding tasks and then viewing the complete list

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T023 [P] [US2] Create unit test for TodoService.get_all_tasks method in tests/unit/test_todo_service.py
- [x] T024 [P] [US2] Create integration test for viewing tasks via CLI in tests/integration/test_cli.py

### Implementation for User Story 2

- [x] T025 [US2] Implement TodoService.get_all_tasks method in src/services/todo_service.py
- [x] T026 [US2] Add CLI command for viewing tasks in src/cli/main.py
- [x] T027 [US2] Add display formatting for task list in src/cli/main.py
- [x] T028 [US2] Handle empty task list case in src/services/todo_service.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P3)

**Goal**: User can change the status of tasks between complete and incomplete by ID

**Independent Test**: Can be fully tested by adding a task, marking it complete, then marking it incomplete again

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T029 [P] [US3] Create unit test for TodoService.mark_task_complete method in tests/unit/test_todo_service.py
- [x] T030 [P] [US3] Create unit test for TodoService.mark_task_incomplete method in tests/unit/test_todo_service.py
- [x] T031 [P] [US3] Create integration test for marking tasks via CLI in tests/integration/test_cli.py

### Implementation for User Story 3

- [x] T032 [US3] Implement TodoService.mark_task_complete method in src/services/todo_service.py
- [x] T033 [US3] Implement TodoService.mark_task_incomplete method in src/services/todo_service.py
- [x] T034 [US3] Add CLI command for marking tasks complete in src/cli/main.py
- [x] T035 [US3] Add CLI command for marking tasks incomplete in src/cli/main.py
- [x] T036 [US3] Add error handling for invalid task IDs in src/services/todo_service.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task Details (Priority: P4)

**Goal**: User can modify the title or description of existing tasks by ID

**Independent Test**: Can be fully tested by adding a task, updating its details, then viewing it to confirm changes

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [x] T037 [P] [US4] Create unit test for TodoService.update_task method in tests/unit/test_todo_service.py
- [x] T038 [P] [US4] Create integration test for updating tasks via CLI in tests/integration/test_cli.py

### Implementation for User Story 4

- [x] T039 [US4] Implement TodoService.update_task method in src/services/todo_service.py
- [x] T040 [US4] Add CLI command for updating tasks in src/cli/main.py
- [x] T041 [US4] Add validation for update inputs in src/services/todo_service.py
- [x] T042 [US4] Add error handling for invalid task IDs in src/services/todo_service.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Task (Priority: P5)

**Goal**: User can remove tasks by ID from the in-memory list

**Independent Test**: Can be fully tested by adding tasks, deleting one, then viewing the list to confirm removal

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [x] T043 [P] [US5] Create unit test for TodoService.delete_task method in tests/unit/test_todo_service.py
- [x] T044 [P] [US5] Create integration test for deleting tasks via CLI in tests/integration/test_cli.py

### Implementation for User Story 5

- [x] T045 [US5] Implement TodoService.delete_task method in src/services/todo_service.py
- [x] T046 [US5] Add CLI command for deleting tasks in src/cli/main.py
- [x] T047 [US5] Add error handling for invalid task IDs in src/services/todo_service.py
- [x] T048 [US5] Handle edge case when deleting the last task in src/services/todo_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T049 [P] Add comprehensive docstrings to all methods in src/models/task.py, src/services/todo_service.py, src/cli/main.py
- [x] T050 [P] Add comments to utility functions in src/lib/utils.py
- [x] T051 [P] Add input validation for all CLI commands in src/cli/main.py
- [x] T052 [P] Add proper error messages for all error cases in src/services/todo_service.py
- [x] T053 [P] Implement proper exit codes in CLI application in src/cli/main.py
- [x] T054 [P] Add README.md with setup instructions
- [x] T055 Run all unit tests and ensure they pass
- [x] T056 Run all integration tests and ensure they pass
- [x] T057 Test quickstart scenarios from quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints/CLI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Create unit test for Task creation in tests/unit/test_task.py"
Task: "Create unit test for TodoService.add_task method in tests/unit/test_todo_service.py"
Task: "Create integration test for adding task via CLI in tests/integration/test_cli.py"

# Launch all implementation for User Story 1 together:
Task: "Implement Task model with id, title, description, status attributes in src/models/task.py"
Task: "Implement TodoService.add_task method with unique ID generation in src/services/todo_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence