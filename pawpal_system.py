from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def duration(self) -> float:
        """Return the length of the task in hours."""
        return self.end_time - self.start_time

    def is_valid(self) -> bool:
        """Return True if the task's end time is after its start time."""
        return self.end_time > self.start_time


@dataclass
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

        conflicts = []
        for i, task in enumerate(sorted_tasks):
            for other in sorted_tasks[:i]:
                shared_pets = [p for p in task.tasked_pets if p in other.tasked_pets]
                if shared_pets and task.start_time < other.end_time and other.start_time < task.end_time:
                    conflicts.append((task.task_name, other.task_name))

        self.new_schedule = sorted_tasks

        reasoning = (
            f"Scheduled {len(sorted_tasks)} pending task(s) sorted by priority "
            f"(highest first), then by start time."
        )
        if conflicts:
            conflict_str = ", ".join(f"'{a}' overlaps '{b}'" for a, b in conflicts)
            reasoning += f" WARNING - time conflicts detected: {conflict_str}."

        self.schedule_reasoning = reasoning


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
