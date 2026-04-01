import streamlit as st
from pawpal_system import Owner, Pet, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name=owner_name)

st.subheader("Add a Pet")
pet_name   = st.text_input("Pet name", value="Mochi")
pet_breed  = st.text_input("Breed", value="Unknown")
pet_gender = st.selectbox("Gender", ["Male", "Female"])
pet_age    = st.number_input("Age", min_value=0, max_value=30, value=1)

if st.button("Add Pet"):
    new_pet = Pet(pet_name=pet_name, pet_breed=pet_breed,
                  pet_gender=pet_gender, pet_age=int(pet_age))
    st.session_state.owner.add_pet(new_pet)
    st.success(f"{pet_name} added!")

if st.session_state.owner.pets:
    st.write("Current pets:", [p.pet_name for p in st.session_state.owner.pets])

st.subheader("Schedule a Task")
st.caption("Tasks are assigned to all current pets of this owner.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task name", value="Morning walk")
with col2:
    task_type = st.selectbox("Task type", ["Exercise", "Feeding", "Medication", "Appointment", "Other"])
with col3:
    priority_map = {"Low": 1, "Medium": 2, "High": 3}
    priority = st.selectbox("Priority", list(priority_map.keys()), index=2)

col4, col5 = st.columns(2)
with col4:
    start_time = st.number_input("Start time (24h, e.g. 8.5 = 8:30)", min_value=0.0, max_value=23.99, value=8.0, step=0.25)
with col5:
    end_time = st.number_input("End time (24h)", min_value=0.0, max_value=23.99, value=8.5, step=0.25)

if st.button("Add Task"):
    if not st.session_state.owner.pets:
        st.error("Add at least one pet before scheduling a task.")
    elif end_time <= start_time:
        st.error("End time must be after start time.")
    else:
        new_task = Task(
            tasked_pets=list(st.session_state.owner.pets),
            task_name=task_title,
            task_type=task_type,
            start_time=start_time,
            end_time=end_time,
            task_priority=priority_map[priority]
        )
        st.session_state.owner.add_task(new_task)
        st.success(f"'{task_title}' added!")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([{
        "Task": t.task_name,
        "Type": t.task_type,
        "Start": t.start_time,
        "End": t.end_time,
        "Priority": t.task_priority,
        "Done": t.is_completed
    } for t in all_tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
