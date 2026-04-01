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

# Conflict task 1: Buddy grooming overlaps morning_walk (both 7:00–7:30, same pet)
buddy_grooming = Task(
    tasked_pets=[buddy],
    task_name="Brushing",
    task_type="Grooming",
    start_time=7.0,
    end_time=7.5,
    task_priority=2,
    description="Quick brush before the walk",
    frequency="once"
)

# Conflict task 2: Luna playtime overlaps luna_medication (9:00–9:30 vs 9:00–9:10, different pet issue)
luna_playtime = Task(
    tasked_pets=[luna],
    task_name="Playtime",
    task_type="Exercise",
    start_time=9.0,
    end_time=9.5,
    task_priority=2,
    description="Feather wand session",
    frequency="once"
)

# Add tasks out of order (luna_medication at 9:00, then feeding at 8:00, then morning_walk at 7:00)
owner.add_task(luna_medication)
owner.add_task(feeding)
owner.add_task(morning_walk)
owner.add_task(buddy_grooming)   # same-pet conflict with morning_walk
owner.add_task(luna_playtime)    # same-pet conflict with luna_medication

# --- Run Scheduler ---
owner.run_scheduler()
schedule = owner.task_scheduler.new_schedule
reasoning = owner.task_scheduler.schedule_reasoning


def print_task(task):
    start_h = int(task.start_time)
    start_m = int((task.start_time % 1) * 60)
    end_h   = int(task.end_time)
    end_m   = int((task.end_time % 1) * 60)
    pets    = ", ".join(p.pet_name for p in task.tasked_pets)
    status  = "Done" if task.is_completed else "Pending"
    print(f"[{start_h:02d}:{start_m:02d} - {end_h:02d}:{end_m:02d}]  "
          f"{task.task_name} ({task.task_type})")
    print(f"   Pets:     {pets}")
    print(f"   Date:     {task.task_date}  |  Frequency: {task.frequency}")
    print(f"   Priority: {task.task_priority}  |  Status: {status}")
    print()


# --- Print Priority Schedule ---
print("=" * 40)
print("       PAWPAL - TODAY'S SCHEDULE")
print("       (sorted by priority)")
print("=" * 40)
print(f"Owner: {owner.owner_name}")
print(f"Pets:  {', '.join(p.pet_name for p in owner.pets)}")
print("-" * 40)
for task in schedule:
    print_task(task)
print(f"Scheduler notes: {reasoning}")
print("=" * 40)

# --- Print sort_by_time() results ---
print()
print("=" * 40)
print("   SORTED BY TIME (chronological)")
print("=" * 40)
for task in owner.task_scheduler.sort_by_time():
    print_task(task)

# --- Print filter_tasks() results ---
print("=" * 40)
print("   FILTER: Pending tasks only")
print("=" * 40)
for task in owner.task_scheduler.filter_tasks(completed=False):
    print_task(task)

print("=" * 40)
print("   FILTER: Completed tasks only")
print("=" * 40)
for task in owner.task_scheduler.filter_tasks(completed=True):
    print_task(task)

print("=" * 40)
print("   FILTER: Buddy's tasks only")
print("=" * 40)
for task in owner.task_scheduler.filter_tasks(pet_name="Buddy"):
    print_task(task)

print("=" * 40)
print("   FILTER: Buddy's pending tasks")
print("=" * 40)
for task in owner.task_scheduler.filter_tasks(completed=False, pet_name="Buddy"):
    print_task(task)

# --- Demonstrate Auto-Recurrence ---
print()
print("=" * 40)
print("   MARKING morning_walk COMPLETE...")
print("   (daily task → next occurrence auto-created)")
print("=" * 40)
morning_walk.mark_complete()

# Re-run scheduler to include the newly created next-day task
owner.run_scheduler()

print()
print("ALL TASKS after mark_complete (sorted by time):")
print("-" * 40)
for task in owner.task_scheduler.sort_by_time():
    print_task(task)
