from db import get_db, get_habit_checkoffs, get_all_habits
from datetime import datetime, timedelta

def get_habits_by_periodicity(db, periodicity):
    """
    Returns a list of all habits that match the given periodicity.
    :param db: Database connection object.
    :param periodicity: Periodicity to filter by.
    :return: List of habit names that match the periodicity.
    """
    try:
        cur = db.cursor()
        cur.execute("SELECT name FROM habit WHERE periodicity = ?", (periodicity,))
        habits = [row[0] for row in cur.fetchall()]
        return habits
    except Exception as e:  # Catch potential database errors
        print(f"Error getting habits: {e}")  # Print error for debugging
        return []

def get_longest_streak(db):
    """
    Finds the habit with the longest streak among all tracked habits.
    :param db: Database connection object.
    :return: tuple: (habit_name, longest streak)
    """
    try:
        cur = db.cursor()
        cur.execute("SELECT name, periodicity FROM habit")  # Get periodicity here
        habits = cur.fetchall()

        max_streak = 0
        best_habit = None

        for habit_name, periodicity in habits:  # Unpack the tuple directly
            streak = calculate_streak(db, habit_name, periodicity)  # Pass periodicity to the function
            if streak > max_streak:
                max_streak = streak
                best_habit = habit_name

        return best_habit, max_streak
    except Exception as e:
        print(f"Error getting longest streak: {e}")
        return None, 0

def calculate_streak(db, habit, periodicity):
    """
    Calculates the longest streak for a given habit, respecting its periodicity.
    :param db: Database connection object.
    :param habit: Name of the habit.
    :param periodicity: Periodicity of the habit (daily, weekly, etc.).
    :return: Longest streak for the habit.
    """
    try:
        data = get_habit_checkoffs(db, habit)
        if not data:
            return 0  # No data means no streak.

        dates = sorted([datetime.strptime(entry[0], "%Y-%m-%d") for entry in data])

        gap_mapping = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(weeks=4),  # Approximation
            "bi-annually": timedelta(weeks=26),
            "annually": timedelta(weeks=52),
        }
        expected_gap = gap_mapping.get(periodicity.lower(), timedelta(days=1))

        streak = max_streak = 1
        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] == expected_gap:
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 1

        return max(max_streak, streak)
    except Exception as e:
        print(f"Error calculating streak for {habit}: {e}")
        return 0