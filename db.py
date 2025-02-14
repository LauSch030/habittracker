import sqlite3
from datetime import date

def get_db(name="main.db"):
    """
    Creates and returns a connection to the SQLite database.
    If the database does not exist, it will be created.
    :param name: Name of the database file. Defaults to "main.db".
    :return: Database connection object.
    """
    db = sqlite3.connect(name)
    create_tables(db)
    insert_default_data(db) # Insert default habits
    return db

def create_tables(db):
    """
    Creates the necessary tables for tracking habits and their check-ins.

    Tables:
        - habit: Stores habit names and their periodicity.
        - tracker: Logs the dates when a habit is completed.

    :param db: Database connection object.
    """
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
    name TEXT PRIMARY KEY,
    periodicity TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracker(
    date TEXT,
    habitName TEXT,
    FOREIGN KEY (habitName) REFERENCES habit(name))""")

    db.commit()

def add_habit(db, name, periodicity):
    """
    Adds a new habit to the database if it does not already exist.

    :param db:Database connection object.
    :param name: Name of the habit.
    :param periodicity: Frequency of the habit (e.g., "daily", "weekly").
    :return: none
    """
    cur = db.cursor()

    # Check if habit already exists.
    cur.execute("SELECT name FROM habit WHERE name=?", (name,))
    existing_habit = cur.fetchone()

    if existing_habit:
        print(f"⚠️ Habit '{name}' exists already!")
    else:
        cur.execute("INSERT INTO habit VALUES (?, ?)", (name, periodicity))
        db.commit()


def delete_habit(db, name):
    """
    Deletes a habit from the database along with its check-offs.

    :param db: Database connection object.
    :param name: Name of the habit to delete.
    """
    cur = db.cursor()

    # Check, if habit exists
    cur.execute("SELECT name FROM habit WHERE name=?", (name,))
    existing_habit = cur.fetchone()

    if existing_habit:
        # Delete habit from all tables (habit and tracker)
        cur.execute("DELETE FROM habit WHERE name=?", (name,))
        cur.execute("DELETE FROM tracker WHERE habitName=?", (name,))
        db.commit()
        print(f"✅ Habit '{name}' deleted successfully!")
    else:
        print(f"⚠️ Habit '{name}' does not exist.")

def edit_habit(db, name, new_periodicity):
    """
    Updates the periodicity of an existing habit.
    :param db: Database connection object.
    :param name: Name of the habit.
    :param new_periodicity: The new periodicity value.
    """
    cur = db.cursor()

    # Check if habit exists
    cur.execute("SELECT * FROM habit WHERE name=?", (name,))
    if not cur.fetchone():
        print(f"⚠️ Habit '{name}' not found!")
        return False

    # Update periodicity
    cur.execute("UPDATE habit SET periodicity=? WHERE name=?", (new_periodicity, name))
    db.commit()
    return True


def checkoff_habit(db, name, event_date=None):
    """
    Logs a habit completion (check-off) in the database.
    :param db: Database connection object.
    :param name: Name of the habit being checked off.
    :param event_date: Date of completion (YYYY-MM-DD). Defaults to today.
    :return: none
    """
    cur = db.cursor()

    if not event_date:
        event_date = str(date.today())

    cur.execute("INSERT INTO tracker (date, habitName) VALUES (?, ?)", (event_date, name))
    db.commit()

def get_all_habits(db):
    """
    Returns a list of all currently tracked habits.
    :param db: Database connection object.
    :return: list: A list of habit names.
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habit")
    return [row[0] for row in cur.fetchall()]

def get_habit_checkoffs(db, name):
    """
    Retrieves all check-off records for a given habit.
    :param db: Database connection object.
    :param name: Name of the habit.
    :return: A list of tuples with (date, habitName).
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE habitName=?", (name,))
    return cur.fetchall()


def insert_default_data(db):
    """
    Inserts default habits and check-offs if they are not already present.

    :param db: Database connection object.
    """
    cur = db.cursor()

    # Default habits
    default_habits = [
        ("Yoga", "daily"),
        ("Groceries", "weekly"),
        ("Deep-clean apartment", "monthly"),
        ("Clean windows", "bi-annually"),
        ("Create my vision board", "annually"),
    ]

    # Check if habits already exist
    for name, periodicity in default_habits:
        cur.execute("SELECT name FROM habit WHERE name=?", (name,))
        if not cur.fetchone():
            cur.execute("INSERT INTO habit VALUES (?, ?)", (name, periodicity))

    # Default check-offs
    default_checkoffs = [
        ("Yoga", ["2024-04-01", "2024-04-02", "2024-04-03", "2024-04-05", "2024-04-06", "2024-04-08"]),  # Almost daily
        ("Groceries", ["2024-03-10", "2024-03-17", "2024-03-24", "2024-03-31"]),  # Weekly
        ("Deep-clean apartment", ["2024-02-15"]),  # Once
        # "Clean windows" & "Create my vision board" have no check-offs yet
    ]

    for habit, dates in default_checkoffs:
        for date in dates:
            cur.execute("INSERT INTO tracker (date, habitName) VALUES (?, ?)", (date, habit))

    db.commit()
    print("✅ Default habits and check-offs added (if not already present).")
