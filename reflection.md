# PawPal+ Project Reflection

3 Core Actions:
- A User shall be able to see all their different tasks categorized
- A user shall be able to add and remove tasks 
- A user shall be able to see why the assistant made the plan it made

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design consists of Owner, Pet, Scheduler, and Task classes. 
    - An owner has pets and can have many pets
    - An owner has tasks which make up its schedule 
    - Many tasks can belong to a single owner
    - A pet also has owner 
    - An owner also has a scheduler, which can create a new schedule for the owner. 
    - Many tasks can be associated to many pets
    
    Owner
    - String OwnerName
    - List<Pet> Pets
    - List<Tasks> Schedule
    - Scheduler TaskScheduler
    ------------------
    addTask()
    removeTask()
    addPet()
    removePet()
    runScheduler()


    Pet
    - String PetName
    - String PetBreed
    - String PetGender
    - Int PetAge
    ------------------
    setPetName()
    setPetBreed()
    setPetGender()
    setPetAge()



    Task
    - Pet TaskedPet
    - String TaskName
    - String TaskType
    - Float StartTime
    - Float EndTime
    - Int TaskPriority
    ------------------

    Scheduler:
    - List<Pet> OwnersPets
    - List<Task> OwnerSchedule
    - List<Task> NewSchedule
    - String ScheduleReasoning
    ------------------
    generateNewSchedule()

    
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
