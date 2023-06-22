# Python Event Management
**Project Description:**

This project is a timetable management system that allows users to create, update, delete, and print timetables. The system supports scheduling events during the work hours of 9am-5pm, and events must have no overlap in their duration. Users can also print a list of all the events scheduled on a selected day of the week in chronological order. The system also supports storing (saving and loading) the timetable data on a file with a provided filename.

**Functional Requirements:**

-   The program must provide a text-based prompt or a menu so that a user can interactively perform various actions to manage the timetable, until deciding to quit.
-   User inputs must be validated (e.g., wrong data type, out of range, or not among the provided options) and asked again with proper error messages if invalid.
-   A user must be able to create, update, and delete a scheduled event. An event must have a title, when it starts and ends, and optionally where it is held. Identifying an event for updating or deleting it should be based on the start time of the event.
-   The timetable must at least support scheduling events during the work hours of 9am-5pm.
-   Scheduling an event must support at least hour level granularity (11am, 3pm, etc.).
-   Events must have no overlap in their duration. When creating or updating an event, the start and end time must be checked against other events to ensure there is no overlap. If a user tries to schedule an event that overlaps with another event, an error message should be displayed and ask the user to reschedule the event.
-   A user must be able to print the timetable which gives an overview of the schedule for the whole week. This should include as much details as possible, but may abbreviate (eg, long title or location) or omit certain details (e.g., end time or location) of each event as needed to make them fit into a table formatting.
-   A user must be able to print a list of all the events scheduled on a selected day of the week in chronological order. This should provide full details of each event (without any abbreviation or details omitted) on the selected day.
-   A user must be able to store (save and load) the timetable data on a file with provided filename.

**Non-Functional Requirements:**

-   The system must be user-friendly and easy to use.
-   The system must be efficient and able to handle large timetables.
-   The system must be reliable and should not crash or lose data.
-   The system must be secure and protect user data from unauthorized access.





