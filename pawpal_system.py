from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


@dataclass(eq=False)
class Task:
    tasked_pets: List[Pet]
    task_name: str
    task_type: str
    start_time: float
    end_time: float
    task_priority: int
    description: str = ""
    frequency: str = "once"
    is_completed: bool = False
    task_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed and schedule next occurrence if recurring."""
        self.is_completed = True
        if self.frequency == "daily":
            delta = timedelta(days=1)
        elif self.frequency == "weekly":
            delta = timedelta(weeks=1)
        else:
            return
        next_task = Task(
            tasked_pets=self.tasked_pets,
            task_name=self.task_name,
            task_type=self.task_type,
            start_time=self.start_time,
            end_time=self.end_time,
            task_priority=self.task_priority,
            description=self.description,
            frequency=self.frequency,
            task_date=self.task_date + delta,
        )
        for pet in self.tasked_pets:
            pet.add_task(next_task)

    def duration(self) -> float:
        """Return the length of the task in hours."""
        return self.end_time - self.start_time

    def is_valid(self) -> bool:
        """Return True if the task's end time is after its start time."""
        return self.end_time > self.start_time


@dataclass(eq=False)
class Pet:
    pet_name: str
    pet_breed: str
    pet_gender: str
    pet_age: int
    tasks: List[Task] = field(default_factory=list)

    def set_pet_name(self, name: str) -> None:
        """Update the pet's name."""
        self.pet_name = name

    def set_pet_breed(self, breed: str) -> None:
        """Update the pet's breed."""
        self.pet_breed = breed

    def set_pet_gender(self, gender: str) -> None:
        """Update the pet's gender."""
        self.pet_gender = gender

    def set_pet_age(self, age: int) -> None:
        """Update the pet's age."""
        self.pet_age = age

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks assigned to this pet."""
        return [t for t in self.tasks if not t.is_completed]


@dataclass
class Scheduler:
    owner: Owner = None
    new_schedule: List[Task] = field(default_factory=list)
    schedule_reasoning: str = ""

    def generate_new_schedule(self) -> None:
        """Sort the owner's pending tasks by priority and detect time conflicts."""
        all_tasks = self.owner.get_all_tasks()
        pending = [t for t in all_tasks if not t.is_completed]

        sorted_tasks = sorted(pending, key=lambda t: (-t.task_priority, t.start_time))

        self.new_schedule = sorted_tasks

        warnings = self.detect_conflicts(sorted_tasks)
        reasoning = (
            f"Scheduled {len(sorted_tasks)} pending task(s) sorted by priority "
            f"(highest first), then by start time."
        )
        if warnings:
            reasoning += " " + " ".join(warnings)

        self.schedule_reasoning = reasoning

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Check all task pairs for time overlap and return a list of warning strings.

        Detects both same-pet conflicts (a pet double-booked) and cross-pet
        conflicts (two tasks overlapping in time regardless of which pet).
        Returns warnings without raising exceptions.
        """
        warnings = []
        for i, task in enumerate(tasks):
            for other in tasks[:i]:
                overlaps = task.start_time < other.end_time and other.start_time < task.end_time
                if not overlaps:
                    continue
                shared_pets = [p for p in task.tasked_pets if p in other.tasked_pets]
                if shared_pets:
                    pet_names = ", ".join(p.pet_name for p in shared_pets)
                    warnings.append(
                        f"WARNING: '{task.task_name}' and '{other.task_name}' overlap "
                        f"for the same pet(s): {pet_names}."
                    )
                else:
                    task_pets = ", ".join(p.pet_name for p in task.tasked_pets)
                    other_pets = ", ".join(p.pet_name for p in other.tasked_pets)
                    warnings.append(
                        f"WARNING: '{task.task_name}' ({task_pets}) and "
                        f"'{other.task_name}' ({other_pets}) overlap in time."
                    )
        return warnings

    def sort_by_time(self) -> List[Task]:
        """Return all owner tasks sorted by start_time ascending."""
        all_tasks = self.owner.get_all_tasks()
        return sorted(all_tasks, key=lambda t: t.start_time)

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.

        Args:
            completed: If True, return only completed tasks.
                       If False, return only pending tasks.
                       If None, include all tasks regardless of status.
            pet_name:  If provided, return only tasks assigned to a pet
                       with this name. If None, include all pets.
        """
        tasks = self.owner.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.is_completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if any(p.pet_name == pet_name for p in t.tasked_pets)]
        return tasks


@dataclass
class Owner:
    owner_name: str
    pets: List[Pet] = field(default_factory=list)
    task_scheduler: Scheduler = field(default_factory=Scheduler)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet and cascade-delete any tasks that referenced it."""
        self.pets.remove(pet)
        for owned_pet in self.pets:
            owned_pet.tasks = [t for t in owned_pet.tasks if pet not in t.tasked_pets]

    def add_task(self, task: Task) -> None:
        """Add a task to each of its assigned pets, enforcing ownership."""
        for pet in task.tasked_pets:
            if pet not in self.pets:
                raise ValueError(f"{pet.pet_name} is not one of {self.owner_name}'s pets.")
        for pet in task.tasked_pets:
            pet.add_task(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from all pets it was assigned to."""
        for pet in task.tasked_pets:
            pet.remove_task(task)

    def get_all_tasks(self) -> List[Task]:
        """Return a deduplicated list of all tasks across every pet."""
        seen = set()
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                if id(task) not in seen:
                    seen.add(id(task))
                    all_tasks.append(task)
        return all_tasks

    def run_scheduler(self) -> None:
        """Trigger the scheduler to generate an optimized schedule for all pets."""
        self.task_scheduler.owner = self
        self.task_scheduler.generate_new_schedule()
