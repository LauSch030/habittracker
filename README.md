# My Habit Tracker App / Project

The primary goal of this project is to design and implement the backend for a habit tracking
app. The application enables users to define, monitor, and analyze
habits to promote personal growth and achieve goals. The functionality to track streaks will enhance motivation of the users. 
Be aware that the app supports both CLI and GUI. 

## Features

- Habit Creation & Management: Track recurring habits with periodicity (daily, weekly, monthly, etc.).
- Check-Off System: Log when you complete a habit.
- Analytics Module: View streaks, analyze habit frequency, and find your longest streak.
- Data Persistence: Uses SQLite to store and manage habit data.
- User Interfaces:
  - CLI (Command Line Interface) with click for power users.
  - GUI (Graphical User Interface) built with Tkinter for an intuitive experience.
- Automated Tests: Ensures functionality through pytest.

## Content of the project folder

- main.py - this is the CLI, built using click. Allows users to create, delete, check off and analyse habits via the command line.
- gui.py - defines the graphic user interface
- habit.py - this is the habit class that is connected to modules and contains the following attributes
- analyse.py - executes analyses of data stored in the db via the habit class
- db.py - contains the logic to access the db
- test_project.py - defines the automatic tests for habit creation, deletion, check off, as well as getting lists of all habits, habits by periodicity, and analysing streaks. 
- requirements.txt - lists all requirements needed (external dependencies)

## Installation

```shell
pip install -r requirements.txt
```
This installs:

- click (for CLI)
- tkinter (for GUI)
- sqlite3 (for database management)
- pytest (for testing)

## Usage

### CLI

```shell
python main.py
```

Available commands 
- python main.py create "habit" "periodicity" - to add a new habit
- python main.py checkoff "habit" - to check-off a habit
- python main.py delete "habit" - to delete a habit
- python main.py edit "habit" new_periodicity - to edit the periodicity of a habit
- python main.py list-habits - show all habits
- python main.py list-by-periodicity periodicity - show all habits with a certain periodicity
- python main.py longest-streak - to show longest overall streak


### GUI

```shell
python gui.py
```

- Add, edit, delete habits with buttons.
- Track check-offs and view analytics.


## Tests

```shell
pytest .
```

Test Coverage:
✔ Habit creation, editing, and deletion
✔ Tracking and check-off functionality
✔ Analytics (streak calculation, periodicity filtering, etc.)

## Future improvements

- Enhanced Analytics: Charts & graphs to visualize progress.
- Cross-Platform Support: Make it web-accessible.
- Custom Habit Periodicity: Allow flexible custom intervals.
