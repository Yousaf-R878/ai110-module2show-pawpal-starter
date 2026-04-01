from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(owner_name="Alex", task_scheduler=Scheduler())

buddy = Pet(pet_name="Buddy", pet_breed="Golden Retriever", pet_gender="Male", pet_age=3)
luna  = Pet(pet_name="Luna",  pet_breed="Siamese Cat",      pet_gender="Female", pet_age=5)

owner.add_pet(buddy)
owner.add_pet(luna)

# --- Tasks ---
morning_walk = Task(
    tasked_pets=[buddy],
    task_name="Morning Walk",
    task_type="Exercise",
    start_time=7.0,
    end_time=7.5,
    task_priority=2,
    description="30-minute walk around the park",
    frequency="daily"
)

feeding = Task(
    tasked_pets=[buddy, luna],
    task_name="Breakfast Feeding",
    task_type="Feeding",
    start_time=8.0,
    end_time=8.25,
    task_priority=3,
    description="Morning meal for both pets",
    frequency="daily"
)

luna_medication = Task(
    tasked_pets=[luna],
    task_name="Allergy Medication",
    task_type="Medication",
    start_time=9.0,
    end_time=9.17,
    task_priority=1,
    description="Daily allergy pill hidden in a treat",
    frequency="daily"
)

owner.add_task(morning_walk)
owner.add_task(feeding)
owner.add_task(luna_medication)

# --- Run Scheduler ---
owner.run_scheduler()
schedule = owner.task_scheduler.new_schedule
reasoning = owner.task_scheduler.schedule_reasoning

# --- Print Today's Schedule ---
print("=" * 40)
print("       PAWPAL - TODAY'S SCHEDULE")
print("=" * 40)
print(f"Owner: {owner.owner_name}")
print(f"Pets:  {', '.join(p.pet_name for p in owner.pets)}")
print("-" * 40)

for task in schedule:
    start_h = int(task.start_time)
    start_m = int((task.start_time % 1) * 60)
    end_h   = int(task.end_time)
    end_m   = int((task.end_time % 1) * 60)
    pets    = ", ".join(p.pet_name for p in task.tasked_pets)
    status  = "Done" if task.is_completed else "Pending"

    print(f"[{start_h:02d}:{start_m:02d} - {end_h:02d}:{end_m:02d}]  "
          f"{task.task_name} ({task.task_type})")
    print(f"   Pets:     {pets}")
    print(f"   Note:     {task.description}")
    print(f"   Priority: {task.task_priority}  |  Status: {status}")
    print()

print("-" * 40)
print(f"Scheduler notes: {reasoning}")
print("=" * 40)
