from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    pet_name: str
    pet_breed: str
    pet_gender: str
    pet_age: int

    def set_pet_name(self, name: str) -> None:
        pass

    def set_pet_breed(self, breed: str) -> None:
        pass

    def set_pet_gender(self, gender: str) -> None:
        pass

    def set_pet_age(self, age: int) -> None:
        pass


@dataclass
class Task:
    tasked_pet: Pet
    task_name: str
    task_type: str
    start_time: float
    end_time: float
    task_priority: int


@dataclass
class Scheduler:
    owners_pets: List[Pet] = field(default_factory=list)
    owner_schedule: List[Task] = field(default_factory=list)
    new_schedule: List[Task] = field(default_factory=list)
    schedule_reasoning: str = ""

    def generate_new_schedule(self) -> None:
        pass


@dataclass
class Owner:
    owner_name: str
    pets: List[Pet] = field(default_factory=list)
    schedule: List[Task] = field(default_factory=list)
    task_scheduler: Scheduler = field(default_factory=Scheduler)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def run_scheduler(self) -> None:
        pass
