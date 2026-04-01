import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


@pytest.fixture
def sample_pet():
    return Pet(pet_name="Buddy", pet_breed="Golden Retriever", pet_gender="Male", pet_age=3)


@pytest.fixture
def sample_task(sample_pet):
    return Task(
        tasked_pets=[sample_pet],
        task_name="Morning Walk",
        task_type="Exercise",
        start_time=7.0,
        end_time=7.5,
        task_priority=2
    )


@pytest.fixture
def owner_with_pet(sample_pet):
    owner = Owner(owner_name="Alex")
    owner.add_pet(sample_pet)
    owner.task_scheduler = Scheduler(owner=owner)
    return owner, sample_pet


def test_mark_complete_changes_status(sample_task):
    assert sample_task.is_completed == False
    sample_task.mark_complete()
    assert sample_task.is_completed == True


def test_add_task_increases_pet_task_count(sample_pet, sample_task):
    assert len(sample_pet.tasks) == 0
    sample_pet.add_task(sample_task)
    assert len(sample_pet.tasks) == 1


# ---------------------------------------------------------------------------
# Recurrence
# ---------------------------------------------------------------------------

def test_daily_task_creates_next_occurrence(sample_pet):
    today = date.today()
    task = Task(
        tasked_pets=[sample_pet],
        task_name="Morning Walk",
        task_type="Exercise",
        start_time=7.0,
        end_time=7.5,
        task_priority=2,
        frequency="daily",
        task_date=today,
    )
    sample_pet.add_task(task)
    task.mark_complete()

    # Original is marked complete; a new task should be added
    assert len(sample_pet.tasks) == 2
    next_task = sample_pet.tasks[1]
    assert next_task.is_completed == False
    assert next_task.task_date == today + timedelta(days=1)


def test_weekly_task_creates_occurrence_seven_days_later(sample_pet):
    today = date.today()
    task = Task(
        tasked_pets=[sample_pet],
        task_name="Vet Check",
        task_type="Medical",
        start_time=10.0,
        end_time=11.0,
        task_priority=3,
        frequency="weekly",
        task_date=today,
    )
    sample_pet.add_task(task)
    task.mark_complete()

    next_task = sample_pet.tasks[1]
    assert next_task.task_date == today + timedelta(weeks=1)


def test_once_task_does_not_create_new_occurrence(sample_pet):
    task = Task(
        tasked_pets=[sample_pet],
        task_name="Bath",
        task_type="Grooming",
        start_time=9.0,
        end_time=9.5,
        task_priority=1,
        frequency="once",
    )
    sample_pet.add_task(task)
    task.mark_complete()

    # No new task should be added
    assert len(sample_pet.tasks) == 1
    assert sample_pet.tasks[0].is_completed == True


def test_recurring_task_added_to_all_assigned_pets():
    """Daily task shared by two pets must spawn the next occurrence on both."""
    pet_a = Pet(pet_name="Buddy", pet_breed="Lab", pet_gender="Male", pet_age=2)
    pet_b = Pet(pet_name="Luna", pet_breed="Poodle", pet_gender="Female", pet_age=4)
    task = Task(
        tasked_pets=[pet_a, pet_b],
        task_name="Joint Walk",
        task_type="Exercise",
        start_time=8.0,
        end_time=8.5,
        task_priority=2,
        frequency="daily",
    )
    pet_a.add_task(task)
    pet_b.add_task(task)
    task.mark_complete()

    assert len(pet_a.tasks) == 2
    assert len(pet_b.tasks) == 2


def test_recurring_task_preserves_attributes(sample_pet):
    """The spawned task should inherit name, type, priority, and frequency."""
    today = date.today()
    task = Task(
        tasked_pets=[sample_pet],
        task_name="Evening Run",
        task_type="Exercise",
        start_time=18.0,
        end_time=18.5,
        task_priority=3,
        frequency="daily",
        task_date=today,
    )
    sample_pet.add_task(task)
    task.mark_complete()

    next_task = sample_pet.tasks[1]
    assert next_task.task_name == "Evening Run"
    assert next_task.task_type == "Exercise"
    assert next_task.task_priority == 3
    assert next_task.frequency == "daily"


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_overlapping_tasks_for_same_pet_flagged(owner_with_pet):
    owner, pet = owner_with_pet
    task_a = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=9.0, end_time=10.0, task_priority=2,
    )
    task_b = Task(
        tasked_pets=[pet], task_name="Bath", task_type="Grooming",
        start_time=9.5, end_time=10.5, task_priority=1,
    )
    owner.add_task(task_a)
    owner.add_task(task_b)
    owner.run_scheduler()

    assert "WARNING" in owner.task_scheduler.schedule_reasoning
    assert "Walk" in owner.task_scheduler.schedule_reasoning
    assert "Bath" in owner.task_scheduler.schedule_reasoning


def test_back_to_back_tasks_not_flagged(owner_with_pet):
    """Tasks that touch (end == start) should not be treated as overlapping."""
    owner, pet = owner_with_pet
    task_a = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=9.0, end_time=10.0, task_priority=2,
    )
    task_b = Task(
        tasked_pets=[pet], task_name="Feed", task_type="Feeding",
        start_time=10.0, end_time=10.5, task_priority=2,
    )
    owner.add_task(task_a)
    owner.add_task(task_b)
    owner.run_scheduler()

    assert "WARNING" not in owner.task_scheduler.schedule_reasoning


def test_non_overlapping_tasks_not_flagged(owner_with_pet):
    owner, pet = owner_with_pet
    task_a = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=8.0, end_time=9.0, task_priority=2,
    )
    task_b = Task(
        tasked_pets=[pet], task_name="Nap", task_type="Rest",
        start_time=14.0, end_time=15.0, task_priority=1,
    )
    owner.add_task(task_a)
    owner.add_task(task_b)
    owner.run_scheduler()

    assert "WARNING" not in owner.task_scheduler.schedule_reasoning


def test_cross_pet_overlap_flagged():
    """Two different pets with overlapping tasks still get a warning."""
    pet_a = Pet(pet_name="Buddy", pet_breed="Lab", pet_gender="Male", pet_age=2)
    pet_b = Pet(pet_name="Luna", pet_breed="Poodle", pet_gender="Female", pet_age=4)
    owner = Owner(owner_name="Alex")
    owner.add_pet(pet_a)
    owner.add_pet(pet_b)
    owner.task_scheduler = Scheduler(owner=owner)

    task_a = Task(
        tasked_pets=[pet_a], task_name="Walk Buddy", task_type="Exercise",
        start_time=9.0, end_time=10.0, task_priority=2,
    )
    task_b = Task(
        tasked_pets=[pet_b], task_name="Groom Luna", task_type="Grooming",
        start_time=9.5, end_time=10.5, task_priority=2,
    )
    owner.add_task(task_a)
    owner.add_task(task_b)
    owner.run_scheduler()

    assert "WARNING" in owner.task_scheduler.schedule_reasoning


def test_completed_tasks_excluded_from_conflict_check(owner_with_pet):
    """Completed tasks are excluded from the schedule, so no conflict should fire."""
    owner, pet = owner_with_pet
    task_a = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=9.0, end_time=10.0, task_priority=2, is_completed=True,
    )
    task_b = Task(
        tasked_pets=[pet], task_name="Bath", task_type="Grooming",
        start_time=9.5, end_time=10.5, task_priority=1,
    )
    owner.add_task(task_a)
    owner.add_task(task_b)
    owner.run_scheduler()

    assert "WARNING" not in owner.task_scheduler.schedule_reasoning


# ---------------------------------------------------------------------------
# Sorting by time
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order(owner_with_pet):
    owner, pet = owner_with_pet
    late = Task(
        tasked_pets=[pet], task_name="Evening Walk", task_type="Exercise",
        start_time=18.0, end_time=18.5, task_priority=1,
    )
    early = Task(
        tasked_pets=[pet], task_name="Morning Feed", task_type="Feeding",
        start_time=7.0, end_time=7.25, task_priority=1,
    )
    mid = Task(
        tasked_pets=[pet], task_name="Midday Play", task_type="Play",
        start_time=12.0, end_time=12.5, task_priority=1,
    )
    # Add out of order on purpose
    for t in [late, early, mid]:
        owner.add_task(t)

    sorted_tasks = owner.task_scheduler.sort_by_time()
    start_times = [t.start_time for t in sorted_tasks]
    assert start_times == sorted(start_times)


def test_sort_by_time_single_task(owner_with_pet):
    owner, pet = owner_with_pet
    task = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=9.0, end_time=9.5, task_priority=2,
    )
    owner.add_task(task)
    assert owner.task_scheduler.sort_by_time() == [task]


def test_sort_by_time_empty_schedule():
    owner = Owner(owner_name="Alex")
    owner.task_scheduler = Scheduler(owner=owner)
    assert owner.task_scheduler.sort_by_time() == []


def test_sort_by_time_includes_completed_tasks(owner_with_pet):
    """sort_by_time operates on all tasks, not just pending ones."""
    owner, pet = owner_with_pet
    done = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=7.0, end_time=7.5, task_priority=2, is_completed=True,
    )
    pending = Task(
        tasked_pets=[pet], task_name="Feed", task_type="Feeding",
        start_time=8.0, end_time=8.25, task_priority=2,
    )
    owner.add_task(done)
    owner.add_task(pending)

    sorted_tasks = owner.task_scheduler.sort_by_time()
    assert len(sorted_tasks) == 2
    assert sorted_tasks[0].start_time <= sorted_tasks[1].start_time


# ---------------------------------------------------------------------------
# Task filtering
# ---------------------------------------------------------------------------

def test_filter_completed_tasks(owner_with_pet):
    owner, pet = owner_with_pet
    done = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=7.0, end_time=7.5, task_priority=2, is_completed=True,
    )
    pending = Task(
        tasked_pets=[pet], task_name="Feed", task_type="Feeding",
        start_time=8.0, end_time=8.25, task_priority=2,
    )
    owner.add_task(done)
    owner.add_task(pending)

    completed = owner.task_scheduler.filter_tasks(completed=True)
    assert all(t.is_completed for t in completed)
    assert len(completed) == 1

    not_completed = owner.task_scheduler.filter_tasks(completed=False)
    assert all(not t.is_completed for t in not_completed)
    assert len(not_completed) == 1


def test_filter_none_returns_all_tasks(owner_with_pet):
    owner, pet = owner_with_pet
    done = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=7.0, end_time=7.5, task_priority=2, is_completed=True,
    )
    pending = Task(
        tasked_pets=[pet], task_name="Feed", task_type="Feeding",
        start_time=8.0, end_time=8.25, task_priority=2,
    )
    owner.add_task(done)
    owner.add_task(pending)

    all_tasks = owner.task_scheduler.filter_tasks(completed=None)
    assert len(all_tasks) == 2


def test_filter_by_pet_name(owner_with_pet):
    owner, buddy = owner_with_pet
    luna = Pet(pet_name="Luna", pet_breed="Poodle", pet_gender="Female", pet_age=4)
    owner.add_pet(luna)

    buddy_task = Task(
        tasked_pets=[buddy], task_name="Walk Buddy", task_type="Exercise",
        start_time=9.0, end_time=9.5, task_priority=2,
    )
    luna_task = Task(
        tasked_pets=[luna], task_name="Groom Luna", task_type="Grooming",
        start_time=10.0, end_time=10.5, task_priority=1,
    )
    owner.add_task(buddy_task)
    owner.add_task(luna_task)

    buddy_tasks = owner.task_scheduler.filter_tasks(pet_name="Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].task_name == "Walk Buddy"


def test_filter_by_nonexistent_pet_name_returns_empty(owner_with_pet):
    owner, pet = owner_with_pet
    task = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=9.0, end_time=9.5, task_priority=2,
    )
    owner.add_task(task)

    result = owner.task_scheduler.filter_tasks(pet_name="Ghost")
    assert result == []


def test_filter_multi_pet_task_by_one_pet_name():
    """A task shared by two pets should appear when filtering by either pet."""
    pet_a = Pet(pet_name="Buddy", pet_breed="Lab", pet_gender="Male", pet_age=2)
    pet_b = Pet(pet_name="Luna", pet_breed="Poodle", pet_gender="Female", pet_age=4)
    owner = Owner(owner_name="Alex")
    owner.add_pet(pet_a)
    owner.add_pet(pet_b)
    owner.task_scheduler = Scheduler(owner=owner)

    shared = Task(
        tasked_pets=[pet_a, pet_b], task_name="Joint Walk", task_type="Exercise",
        start_time=9.0, end_time=9.5, task_priority=2,
    )
    owner.add_task(shared)

    assert len(owner.task_scheduler.filter_tasks(pet_name="Buddy")) == 1
    assert len(owner.task_scheduler.filter_tasks(pet_name="Luna")) == 1


def test_filter_combined_completed_and_pet_name(owner_with_pet):
    owner, pet = owner_with_pet
    done = Task(
        tasked_pets=[pet], task_name="Walk", task_type="Exercise",
        start_time=7.0, end_time=7.5, task_priority=2, is_completed=True,
    )
    pending = Task(
        tasked_pets=[pet], task_name="Feed", task_type="Feeding",
        start_time=8.0, end_time=8.25, task_priority=2,
    )
    owner.add_task(done)
    owner.add_task(pending)

    result = owner.task_scheduler.filter_tasks(completed=True, pet_name="Buddy")
    assert len(result) == 1
    assert result[0].task_name == "Walk"
