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
    --
    addTask()
    removeTask()
    addPet()
    removePet()
    runScheduler()

    -------------------
    Pet
    - String PetName
    - String PetBreed
    - String PetGender
    - Int PetAge
    --
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
    --
    generateNewSchedule()

Here was my initial UML diagram before asking AI to create it within the Mermaid Live Editor.
    
- What classes did you include, and what responsibilities did you assign to each?

I included the Owner, Pet, Task, and Scheduler classes. 
Owner: Responsible for adding pets, and creating tasks for their schedule
Pet: Responsible for containing relevant data information tied to a specific pet
Scheduler: Responsible for taking the owners existing pets and schedule and then creates a new schedule without conflicts and provides reasoning for the changes.
Task: Responsible for representing a single task or care activity, being tied to specific pet. It has start and end times as well as task priority fields to aid with scheduling.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

One change I made to my design during implementation was the fact that the Schdeuler isnt connected to the Owner in any way, so it wouldnt be able to actually change the Owner's schedule.

Another change I saw was that the Task->Pet relation was one to one, which may be restrictive of multiple pets being a part of the same task. This will get rid of the redundancy of tasks, and gets rid of tasks having to overlap if theyre the same task just for multiple pets. For example, you could have a task where you're taking all of your pets to the vet, in which case you would've had to make a bunch of tasks to accomodate that one tast.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My scheduler only considers the constaints of priority as well as the time overlaps in order to display whenever there may be conflicts. 

- How did you decide which constraints mattered most?
The constaint that made sense to matter the most was the priority of a task, and that was because I felt as though even if a task overlapped, that tasks with greater priority should be taken care of, especially if there exists a task like, "take pet to vet" with a priority of 3 against a task like "take dog on walk" with a priority of 1 at the same time. Higher priority tasks matter more as they have more weight and urgency to them in my opinion.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    Currently my filter_tasks() function iterates the entire task list twice when both filters are provided. An optimization would be to implement the filter so that a single pass of the task list occurs in order to have more efficiency. However, this wasn't what the AI implemented initially, I belief it prioritized readability over efficiency.
- Why is that tradeoff reasonable for this scenario?
    This tradeoff is reasonable for the sole reason that this is a small pet app and because in the real world, you are very unlikely to have > 100 tasks or een 10,000 or 100,000 tasks which would begin to give some level of performance hit. Since we dont need to worry about large amounts of tasks for this application, it makes sense to trade readability for performance.

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
    1. Marking a task as complete creating a new occurance of the same task with the same date
    2. Conflict detection
    3. Task sorting (by time)
    4. Task filtering
- Why were these tests important?
    1. They will ensure that tasks that are marked as once dont occur repeatedly, and tasks that are meant to repeat do show up. This guarantees your tasks stay organized and the task list doesnt need to be managed constantly for repeat tasks, making it easier to maintain the schedule.
    2. Time conflicts must throw errors to let the owner know but also shouldnt throw errors when there are no overlaps, to minimize confusion
    3. Testing on task sorting make sure that tasks stay in order and dont end up being missed because of tasks accidentally being out of order
    4. Filtering tests are important to ensure that the owner is able to correctly find tasks that they want to find and only see what theyre asking to. Additionally, we want to ensure some tasks arent being missed. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
    Im at a level of 4.5 for confidence that my scheduler works, as I've not only tested the scheduler myself with my own test cases but also because of the extensive tests that claude was able to create. I also reviewed the test cases to make sure they made sense and ensured that my tests wouldnt produce false results. The only thing that would bring this to a 5 would be the number of tests.
- What edge cases would you test next if you had more time?
    I would consider edge cases related to the owner and pets next such as removing a pet that doesnt exist, removing pets from an empty list of pets, and just tests that ensured proper input validation as well.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Im most satisfied with taking UML diagrams and building out the architecture of a project before actually jumping into actually developing and working with code. It reinforces the idea of really understanding the underlying architecture that way when you move to developing, you have an easier time with guiding the agent.
I did like using different chat sessions for different tasks as it helped me stay more organized with knowing what agent focuses on what task. It also allowed me to have multiple agents run simultaneously which is something I felt as though I rarely used.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would most likely add more tests for all of the other feature and I would spend more time to ensure the UI is as polished as possible. I would also create some tests for the UI as well in order to ensure that the frontend and backend are connected properly and displaying things properly.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Designing systems and working with the underlying logic on a white board or with UML diagrams is much more important than actually getting down to writing code. If you have a solid plan and can properly articulate the design of your system to an AI, youll run into less risks of the AI just assuming certain ways in which your application functions.

---
