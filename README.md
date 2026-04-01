# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The `Scheduler` class (in `pawpal_system.py`) has been extended with three new features:

**Sort by time**
`Scheduler.sort_by_time()` returns all tasks in chronological order using a lambda key:
```python
sorted(tasks, key=lambda t: t.start_time)
```

**Filter by status or pet**
`Scheduler.filter_tasks(completed, pet_name)` filters tasks in a single pass. Both arguments are optional and compose together — for example, `filter_tasks(completed=False, pet_name="Buddy")` returns only Buddy's pending tasks.

**Conflict detection**
`Scheduler.detect_conflicts(tasks)` checks every pair of tasks for time overlap and returns warning strings without crashing. It distinguishes two cases:
- *Same-pet conflict* — a pet is double-booked at the same time
- *Cross-pet conflict* — two tasks for different pets overlap in time

**Auto-recurrence**
`Task.mark_complete()` now checks the task's `frequency` field. If it is `"daily"` or `"weekly"`, a new Task is automatically added to each assigned pet's list with the date advanced by `timedelta(days=1)` or `timedelta(weeks=1)`. Tasks with `frequency="once"` are simply marked done with no follow-up created.

## Features

### Pet & Owner Management
- **Add and track multiple pets** — Each owner can manage any number of pets, each storing a name, breed, gender, and age.
- **Per-pet task lists** — Tasks live directly on each pet rather than on the owner, keeping each animal's schedule self-contained.
- **Ownership enforcement** — Adding a task validates that every assigned pet belongs to the owner, preventing orphaned or misrouted tasks.
- **Cascade removal** — Removing a pet automatically removes all tasks that referenced it, keeping the schedule consistent.

### Task Scheduling
- **Priority-based scheduling** — `Scheduler.generate_new_schedule()` sorts all pending tasks by priority (highest first), then by start time as a tiebreaker, so the most critical care always appears at the top of the plan.
- **Chronological view** — `Scheduler.sort_by_time()` returns all tasks sorted by start time, giving a clean hour-by-hour view of the day regardless of priority.
- **Multi-pet task assignment** — A single task (e.g., a joint walk or shared feeding) can be assigned to multiple pets at once and appears in each pet's schedule.

### Conflict Detection
- **Same-pet conflict warnings** — `Scheduler.detect_conflicts()` flags any two tasks that share at least one pet and have overlapping time windows, warning that the pet is double-booked.
- **Cross-pet conflict warnings** — Overlapping tasks assigned to *different* pets are also flagged, alerting the owner that two activities are scheduled at the same time even if no single pet is double-booked.
- **Back-to-back tasks allowed** — Tasks that share an exact boundary (one ends at 9:00, the next starts at 9:00) are intentionally not flagged as conflicts.

### Auto-Recurrence
- **Daily recurrence** — Marking a `frequency="daily"` task complete automatically creates a new identical task dated one day later and adds it to every assigned pet's list.
- **Weekly recurrence** — Marking a `frequency="weekly"` task complete schedules the next occurrence seven days out.
- **One-time tasks** — Tasks with `frequency="once"` are simply marked done with no follow-up created.

### Filtering
- **Filter by status** — `Scheduler.filter_tasks(completed=True/False)` returns only completed or only pending tasks.
- **Filter by pet** — Passing a `pet_name` returns only tasks assigned to that pet, including multi-pet tasks the pet shares with others.
- **Combined filters** — Status and pet filters compose together (e.g., all pending tasks for Buddy only).

### Streamlit UI
- **Live session persistence** — The `Owner` object is stored in `st.session_state` so pets and tasks survive page interactions without resetting.
- **Inline schedule generation** — The "Generate Schedule" button calls the Scheduler and displays the prioritized plan alongside the scheduler's reasoning and any conflict warnings.
- **Mark complete from UI** — Any pending task can be marked complete directly from the task list; recurring tasks show a confirmation message with the next scheduled date.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

The tests cover four core scheduling behaviors:

**Recurrence** — Verifies that marking a `"daily"` task complete automatically creates a new task dated one day later, a `"weekly"` task advances by seven days, and a `"once"` task creates no follow-up. Also checks that recurring tasks shared by multiple pets are added to every pet's list.

**Conflict detection** — Confirms the Scheduler emits a `WARNING` when two tasks overlap in time, distinguishing same-pet double-bookings from cross-pet time conflicts. Verifies that back-to-back tasks (end time == start time) and non-overlapping tasks produce no warnings, and that completed tasks are excluded from conflict checks.

**Sorting by time** — Ensures `sort_by_time()` returns tasks in chronological order regardless of insertion order, handles a single task and an empty schedule without error, and includes completed tasks (not just pending ones).

**Filtering** — Checks that `filter_tasks(completed=True/False)` correctly separates done and pending tasks, `completed=None` returns all tasks, filtering by `pet_name` returns only that pet's tasks, an unknown pet name returns an empty list, a multi-pet task appears when filtering by any of its assigned pets, and combined filters (status + pet name) compose correctly.


## 📸 Demo

<a href="/ai110-module2show-pawpal-starter/images/PawPal.png" target="_blank"><img src='/course_images/ai110/PawPal.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>