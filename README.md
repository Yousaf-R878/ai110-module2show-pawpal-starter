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
