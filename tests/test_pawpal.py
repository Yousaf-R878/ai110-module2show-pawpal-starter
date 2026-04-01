import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from pawpal_system import Pet, Task


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


def test_mark_complete_changes_status(sample_task):
    assert sample_task.is_completed == False
    sample_task.mark_complete()
    assert sample_task.is_completed == True


def test_add_task_increases_pet_task_count(sample_pet, sample_task):
    assert len(sample_pet.tasks) == 0
    sample_pet.add_task(sample_task)
    assert len(sample_pet.tasks) == 1
