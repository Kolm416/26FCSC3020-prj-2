# Overview

In this project, you will work in Scrum teams to develop a software product over three sprints. Together with your team you will create and manage a Product Backlog, participate in Scrum meetings, and document your progress. The project also emphasizes the use of version control, automated testing, and continuous deployment to simulate real-world development practices.

This is a team project, and each team must consist of up to 3 members—no exceptions. Your team for this project does not need to be the same as the one from the previous project. 

# Project Vision

The goal of this project is to develop a web app that streamlines the creation, management, and execution of Capture the Flag (CTF) competitions. The platform will enable organizers to design challenges, manage teams, track progress in real time, and automate scoring. Participants will be able to register, join teams, and submit solutions through an intuitive interface. 

# User Stories 

This section describes key **user stories** identified for the project.

## US#1: User Registration

As a new user, I want to register on the CTF platform by providing my name, a unique email address, a password, and selecting my role as either a participant or a competition organizer, so that I can access the appropriate features and functionalities based on my role; once all required information is provided and I click "Submit," my account should be successfully created and stored in the system.

## US#2: CTF Competitions Visualization

As a logged-in competition organizer, I want to view a list of all the CTF competitions I have created, so that I can easily manage, update, or monitor the status of each competition from a centralized dashboard; given that I have successfully logged in, I should be able to see all the competitions I’ve created displayed in an organized and accessible format.

## US#3: CTF New Competitions

As a logged-in competition organizer, I want to create a new CTF competition by providing details such as the competition name, description, start and end dates, and any relevant settings, so that I can launch and manage a new event for participants; given that I have entered all the required information and clicked "Submit," the system should create and store the new competition successfully.

## US#4: Add Challeges to a Competition 

As a logged-in competition organizer, I want to add challenges to a CTF competition that I have created by providing details such as the challenge title, description, category, point value, and flag, so that participants can engage with the challenges during the competition; given that I have selected one of my competitions and submitted all required challenge information, the new challenge should be saved and associated with that competition.

## US#5: Register for a Competition

As a logged-in participant, I want to register for a CTF competition that has not yet started, so that I can secure my spot and be ready to compete when the event begins; given that the competition is open for registration and I meet any eligibility requirements, I should be able to join the competition by clicking a "Register" button, after which my participation will be confirmed and recorded in the system.

## US#6: Submit an Answer to a Challenge

As a registered participant in an active CTF competition, I want to submit my answer (flag) for a specific challenge, so that I can attempt to solve it and earn points; given that I am logged in, registered for the competition, and the competition is currently active, I should be able to enter my answer and receive immediate feedback on whether it is correct, with my score updated accordingly.

## US#7: View Final Results

As a participant or organizer, I want to view the final results of a CTF competition that has ended, so that I can see the rankings, scores, and performance of all participating teams or individuals; given that the competition has concluded, I should be able to access a results page summarizing the final standings and relevant statistics.

# Design 

Finish the design by creating:

* The domain model in [uml/class.wsd](uml/class.wsd);
* The use case diagram in [uml/use-case.wsd](uml/use-case.wsd), illustrating the main interactions between users (participants and organizers) and the system; and
* A sequence diagram detailing the flow of one selected user story to clarify system behavior and interactions. 

# Implementation 

You are expected to implement six out of the seven user stories. Your implementation must use Python with the Flask framework. Additionally, you are required to incorporate caching into your project. One way to do this is by using the Flask-Caching extension, which adds caching support to Flask applications. To configure a cache timeout of 5 minutes, add the following lines to your **__init__.py** file:

```
# cache setup
from flask_caching import Cache
cache = Cache()
cache.init_app(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})
```

You must organize your project using the following directory structure:

```
src/
uml/
scrum/
tests/
Dockerfile
README.md
requirements.txt
```

# Project Management 

Your team will be evaluated on how closely you followed the Scrum framework and how effectively you collaborated as a Scrum team. Each unit of work (user story) must include a clear effort estimate in story points. Each sprint must have a well-defined goal statement. The team is expected to record notes from daily Scrum meetings, as well as from Sprint Review and Sprint Retrospective meetings at the end of each sprint.

Refer to the Scrum folder for a sprint documentation template. You should create one file per sprint, named using the format sprint#.md, replacing the # with the sprint number (e.g., sprint1.md).

Project progress should be documented at the end of each sprint. Additionally, at the end of the project, you must generate a burndown report using the provided template located at [scrum/Burndown Chart Template.xlsx](scrum/Burndown Chart Template.xlsx).

# Version Control 

You are expected to create a **dev** branch, which should be merged into **main** at the end of each sprint to deliver the new release. Throughout the sprints, the **dev** branch should also show multiple merges from topical branches, demonstrating collaborative development and incremental progress.

# Testing

You are required to implement at least one black box test using Selenium, based on a user story of your choice. You are not expected to write automated tests for the remaining user stories. Instead, you should perform manual testing, documenting your test results using the table provided below.

|User Story|Date|Time|Result|
|--|--|--|--|
|Sign Up|99/99/26|99:99|passed|
|...|...|...|...|

# Deployment 

Create a Docker image to allow the instructor to run your project in a containerized environment. To meet this requirement, include a **Dockerfile** in your repository that enables the instructor to build the image and run the application as a container.

# Self and Team Evaluation 

# Team Evaluation 

Please reflect on both your own contributions and those of your teammates using the descriptions provided for each dimension. You may refer back to these descriptions as you consider each person's role in the project.

* Meaningful Contributions: Consider how often and significantly the person contributed to the project. This includes writing code, testing, researching, documenting, or helping solve problems.
* Value of Contributions: Value goes beyond technical input. It includes contributions in organization, communication, conflict resolution, and other areas that support team success.
* Collaboration: Collaboration ranges from baseline participation-such as responding when asked-to proactive support like initiating discussions and resolving misunderstandings. Collaboration: can range from basic participation—such as responding when asked—to proactive engagement, like initiating discussions and helping resolve misunderstandings.
* Initiative and Responsibility: Initiative means stepping up without needing to be asked. Responsibility includes owning tasks, meeting deadlines, and following through on commitments.
* Communication and Dependability: This includes keeping teammates informed, communicating challenges, and reliably completing assigned tasks.
* Presence and Availability: Reflect on how consistently the person was present and reachable—attending meetings, responding to messages, and participating in team activities. Note that some team members may contribute meaningfully but be less available than expected.
* Trust Building: Trust is essential for team success because it creates the foundation for effective collaboration, communication, and accountability. When team members trust each other, they feel safe sharing ideas, asking questions, and giving honest feedback—without fear of judgment or retaliation.
* Conflict Resolution: Conflict resolution is the process of addressing and resolving disagreements in a constructive and respectful way. It helps team members find common ground, maintain collaboration, and move forward productively.
* Decision-Making: Decision-making is the process of choosing the best course of action among available options to achieve a goal. It provides direction and keeps the team moving forward.

```
Your Name: <Last_First_Name>
```

Rate your collaboration using: 
* 1 (strongly disagree)
* 2 (disagree)
* 3 (neutral)
* 4 (agree) or 
* 5 (strongly agree)

```
[  ] I made meaningful contributions to the project.
[  ] My contributions were valuable to the team’s success.
[  ] I supported collaboration within the team.
[  ] I took initiative and responsibility for my work.
[  ] I communicated effectively and was dependable.
[  ] I was present and available to the team as expected.
[  ] I fostered trust by being reliable, transparent, and respectful in all interactions.
[  ] I helped resolve disagreements constructively, promoting understanding and collaboration.
[  ] I contributed to or led decision-making processes with clarity, fairness, and consideration of team input.
```

```
Teamate's Name: <Last_First_Name>
```

Rate their collaboration using: 
* 1 (strongly disagree)
* 2 (disagree)
* 3 (neutral)
* 4 (agree) or 
* 5 (strongly agree)

```
[  ] The team member made meaningful contributions to the project.
[  ] The team member  contributions were valuable to the team’s success.
[  ] The team member supported collaboration within the team.
[  ] The team member took initiative and responsibility for my work.
[  ] The team member communicated effectively and was dependable.
[  ] The team member was present and available to the team as expected.
[  ] The team member fostered trust by being reliable, transparent, and respectful in all interactions.
[  ] The team member helped resolve disagreements constructively, promoting understanding and collaboration.
[  ] The team member contributed to or led decision-making processes with clarity, fairness, and consideration of team input.
```

```
Teammate's Name: <Last_First_Name>
```

Rate their collaboration using: 
* 1 (strongly disagree)
* 2 (disagree)
* 3 (neutral)
* 4 (agree) or 
* 5 (strongly agree)

```
[  ] The team member made meaningful contributions to the project.
[  ] The team member  contributions were valuable to the team’s success.
[  ] The team member supported collaboration within the team.
[  ] The team member took initiative and responsibility for my work.
[  ] The team member communicated effectively and was dependable.
[  ] The team member was present and available to the team as expected.
[  ] The team member fostered trust by being reliable, transparent, and respectful in all interactions.
[  ] The team member helped resolve disagreements constructively, promoting understanding and collaboration.
[  ] The team member contributed to or led decision-making processes with clarity, fairness, and consideration of team input.
```

# Rubric 

✅ Required Components

```
+8 points per required user story implemented (up to 6) → 8 × 6 = 48 points
+2 for using cache
+5 for testing
+25 for Scrum project management:
    +5 sprint planning
    +5 daily scrum meetings
    +5 sprint reviews
    +5 sprint retrospectives
    +5 burndown chart
+5 for deployment
+15 for team/self-evaluation
````

✅ Deductions

```
−3 if version control is not properly done
````

✅ Bonus

```
+5 bonus points for each additional user story implemented beyond the required 6
````

✅ Total

```
Base total (without deductions or bonuses):
48 + 2 + 5 + 25 + 5 + 15 = 100 points
```