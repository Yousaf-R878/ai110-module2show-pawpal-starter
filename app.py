import streamlit as st
from datetime import timedelta
from pawpal_system import Owner, Pet, Task


def _fmt_time(h: float) -> str:
    """Convert decimal hour (e.g. 8.5) to HH:MM string (e.g. 08:30)."""
    hours = int(h)
    minutes = int(round((h - hours) * 60))
    return f"{hours:02d}:{minutes:02d}"


def _task_rows(tasks):
    return [
        {
            "Status": "✅ Done" if t.is_completed else "⏳ Pending",
            "Task": t.task_name,
            "Date": str(t.task_date),
            "Type": t.task_type,
            "Start": _fmt_time(t.start_time),
            "End": _fmt_time(t.end_time),
            "Priority": t.task_priority,
            "Frequency": t.frequency,
            "Pets": ", ".join(p.pet_name for p in t.tasked_pets),
        }
        for t in tasks
    ]


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session state ────────────────────────────────────────────────────────────

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name="Jordan")

owner: Owner = st.session_state.owner

# ── Owner ────────────────────────────────────────────────────────────────────

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.owner_name)
if owner_name != owner.owner_name:
    owner.owner_name = owner_name

# ── Add a Pet ────────────────────────────────────────────────────────────────

st.subheader("Add a Pet")
col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    pet_breed = st.text_input("Breed", value="Unknown")
with col3:
    pet_gender = st.selectbox("Gender", ["Male", "Female"])
with col4:
    pet_age = st.number_input("Age", min_value=0, max_value=30, value=1)

if st.button("Add Pet"):
    new_pet = Pet(
        pet_name=pet_name,
        pet_breed=pet_breed,
        pet_gender=pet_gender,
        pet_age=int(pet_age),
    )
    owner.add_pet(new_pet)
    st.success(f"{pet_name} added!")

if owner.pets:
    st.write("Current pets:", [p.pet_name for p in owner.pets])

st.divider()

# ── Add a Task ───────────────────────────────────────────────────────────────

st.subheader("Schedule a Task")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task name", value="Morning walk")
with col2:
    task_type = st.selectbox(
        "Task type", ["Exercise", "Feeding", "Medication", "Appointment", "Other"]
    )
with col3:
    priority_map = {"Low": 1, "Medium": 2, "High": 3}
    priority = st.selectbox("Priority", list(priority_map.keys()), index=2)

col4, col5, col6 = st.columns(3)
with col4:
    start_time = st.number_input(
        "Start (24h, e.g. 8.5 = 8:30)", min_value=0.0, max_value=23.99, value=8.0, step=0.25
    )
with col5:
    end_time = st.number_input(
        "End (24h)", min_value=0.0, max_value=23.99, value=8.5, step=0.25
    )
with col6:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

if owner.pets:
    pet_name_to_obj = {p.pet_name: p for p in owner.pets}
    selected_pet_names = st.multiselect(
        "Assign to pet(s)",
        options=list(pet_name_to_obj.keys()),
        default=list(pet_name_to_obj.keys()),
        help="Select one or more pets for this task. All pets are selected by default.",
    )
else:
    selected_pet_names = []
    st.caption("Add a pet above before scheduling tasks.")

if st.button("Add Task"):
    if not owner.pets:
        st.error("Add at least one pet before scheduling a task.")
    elif not selected_pet_names:
        st.error("Select at least one pet to assign this task to.")
    elif end_time <= start_time:
        st.error("End time must be after start time.")
    else:
        assigned_pets = [pet_name_to_obj[n] for n in selected_pet_names]
        new_task = Task(
            tasked_pets=assigned_pets,
            task_name=task_title,
            task_type=task_type,
            start_time=start_time,
            end_time=end_time,
            task_priority=priority_map[priority],
            frequency=frequency,
        )
        owner.add_task(new_task)
        pet_label = ", ".join(selected_pet_names)
        st.success(f"'{task_title}' added for {pet_label}!")

st.divider()

# ── Task list with filters ───────────────────────────────────────────────────

st.subheader("All Tasks")

if "_flash" in st.session_state:
    level, msg = st.session_state.pop("_flash")
    if level == "success":
        st.success(msg)

all_tasks = owner.get_all_tasks()

if all_tasks:
    if st.session_state.pop("_reset_filter", False):
        st.session_state["status_filter"] = "Pending"

    with st.expander("Filter tasks", expanded=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            status_choice = st.selectbox("Status", ["All", "Pending", "Completed"], index=1, key="status_filter")
        with f_col2:
            pet_choices = ["All"] + [p.pet_name for p in owner.pets]
            pet_choice = st.selectbox("Pet", pet_choices)

    completed_filter = {"All": None, "Pending": False, "Completed": True}[status_choice]
    pet_filter = None if pet_choice == "All" else pet_choice

    owner.task_scheduler.owner = owner
    filtered = owner.task_scheduler.filter_tasks(
        completed=completed_filter, pet_name=pet_filter
    )
    filtered_sorted = sorted(filtered, key=lambda t: t.start_time)

    if filtered_sorted:
        st.dataframe(_task_rows(filtered_sorted), use_container_width=True)
    else:
        st.info("No tasks match the current filters.")

    # Mark complete
    pending_tasks = [t for t in all_tasks if not t.is_completed]
    if pending_tasks:
        st.markdown("**Mark a task complete**")
        mc_col1, mc_col2 = st.columns([3, 1])
        with mc_col1:
            selected_idx = st.selectbox(
                "Select task",
                range(len(pending_tasks)),
                format_func=lambda i: f"{pending_tasks[i].task_name} ({_fmt_time(pending_tasks[i].start_time)})",
                label_visibility="collapsed",
            )
        with mc_col2:
            if st.button("Mark Complete"):
                task_to_complete = pending_tasks[selected_idx]
                task_to_complete.mark_complete()
                msg = f"'{task_to_complete.task_name}' marked complete."
                if task_to_complete.frequency in ("daily", "weekly"):
                    delta = timedelta(days=1) if task_to_complete.frequency == "daily" else timedelta(weeks=1)
                    next_date = task_to_complete.task_date + delta
                    msg += f" Next occurrence scheduled for {next_date}."
                st.session_state["_reset_filter"] = True
                st.session_state["_flash"] = ("success", msg)
                st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Generate Schedule ────────────────────────────────────────────────────────

st.subheader("Generate Schedule")
st.caption("Sorts pending tasks by priority (highest first), then start time, and checks for conflicts.")

if st.button("Generate Schedule"):
    if not owner.pets:
        st.error("Add at least one pet first.")
    elif not owner.get_all_tasks():
        st.info("No tasks to schedule yet.")
    else:
        owner.run_scheduler()
        schedule = owner.task_scheduler.new_schedule
        reasoning = owner.task_scheduler.schedule_reasoning

        if not schedule:
            st.info("No pending tasks to schedule — all tasks are already completed.")
        else:
            # Extract warning lines and the summary line separately
            warning_lines = [
                line.strip()
                for line in reasoning.split("WARNING:")
                if line.strip() and "WARNING:" not in line.split("WARNING:")[0]
            ]
            # Simpler: split reasoning into sentences and flag WARNING ones
            sentences = reasoning.replace("WARNING:", "|||WARNING:").split("|||")
            summary = sentences[0].strip()
            warnings = [s.strip() for s in sentences[1:] if s.strip()]

            st.info(summary)

            if warnings:
                for w in warnings:
                    st.warning(f"Conflict detected — {w.removeprefix('WARNING:').strip()}")
            else:
                st.success("No conflicts detected — schedule looks good!")

            st.markdown("**Optimized Schedule**")
            st.dataframe(_task_rows(schedule), use_container_width=True)
