import pytest
from habit import Habit
from db import get_db, add_habit, edit_habit, delete_habit, checkoff_habit, get_all_habits
from analyse import get_habits_by_periodicity, get_longest_streak

class TestHabit:
    def setup_method(self):
        """Setup test database and add test habits."""
        self.db = get_db("test.db")
        cur = self.db.cursor()

        # Clear old test data
        cur.execute("DELETE FROM habit")
        cur.execute("DELETE FROM tracker")
        self.db.commit()

        # Insert predefined habits
        add_habit(self.db, "test_habit_daily", "daily")
        add_habit(self.db, "test_habit_weekly", "weekly")
        add_habit(self.db, "test_habit_monthly", "monthly")

        # Insert check offs
        checkoff_habit(self.db, "test_habit_daily", "2025-01-25")
        checkoff_habit(self.db, "test_habit_daily", "2025-01-26")
        checkoff_habit(self.db, "test_habit_daily", "2025-01-27")
        checkoff_habit(self.db, "test_habit_daily", "2025-01-29")
        checkoff_habit(self.db, "test_habit_weekly", "2025-01-20")
        checkoff_habit(self.db, "test_habit_weekly", "2025-01-27")

    def test_habit_creation(self):
        """Test creating a new habit."""
        habit = Habit("test_habit_new", "daily")
        habit.store(self.db)

        cur = self.db.cursor()
        cur.execute("SELECT * FROM habit WHERE name=?", ("test_habit_new",))
        result = cur.fetchone()

        assert result is not None
        assert result[0] == "test_habit_new"
        assert result[1] == "daily"

    def test_habit_deletion(self):
        """Test deleting a habit removes it from the habit and tracker tables."""
        # First create habit
        add_habit(self.db, "test_habit_daily", "daily")

        # Add a check-off
        checkoff_habit(self.db, "test_habit_daily", "2025-02-25")

        # Delete habit
        delete_habit(self.db, "test_habit_daily")

        # Check if the habit was deleted from table
        cur = self.db.cursor()
        cur.execute("SELECT * FROM habit WHERE name=?", ("test_habit_daily",))
        result_habit = cur.fetchone()
        assert result_habit is None  # Should be "None", since it was deleted

        # Check, if check-offs were deleted, too
        cur.execute("SELECT * FROM tracker WHERE habitName=?", ("test_habit_daily",))
        result_tracker = cur.fetchone()
        assert result_tracker is None  # Should be "None" as well

    def test_edit_habit(self):
        """Test updating a habit's periodicity in the database."""
        add_habit(self.db, "habit_to_edit", "daily")

        # Secure that original periodicity is "daily"
        cur = self.db.cursor()
        cur.execute("SELECT periodicity FROM habit WHERE name = ?", ("habit_to_edit",))
        assert cur.fetchone()[0] == "daily"

        # Change periodicity to "weekly"
        edit_habit(self.db, "habit_to_edit", "weekly")

        # Check, if periodicity was modified
        cur.execute("SELECT periodicity FROM habit WHERE name = ?", ("habit_to_edit",))
        assert cur.fetchone()[0] == "weekly"

    def test_habit_checkoff(self):
        """Test logging a check-off for a habit."""
        checkoff_habit(self.db, "test_habit_daily")

        cur = self.db.cursor()
        cur.execute("SELECT * FROM tracker WHERE habitName=?", ("test_habit_daily",))
        result = cur.fetchall()

        assert len(result) > 0

    def test_get_all_habits(self):
        """Test retrieving all stored habits."""
        habits = get_all_habits(self.db)
        assert "test_habit_daily" in habits
        assert "test_habit_weekly" in habits
        assert "test_habit_monthly" in habits

        print(get_all_habits(self.db))

    def test_get_habits_by_periodicity(self):
        """Test filtering habits by periodicity."""
        daily_habits = get_habits_by_periodicity(self.db, "daily")
        weekly_habits = get_habits_by_periodicity(self.db, "weekly")

        assert "test_habit_daily" in daily_habits
        assert "test_habit_weekly" in weekly_habits
        assert "test_habit_monthly" not in weekly_habits

    def test_longest_streak(self):
        """Test calculating the longest streak of all habits."""
        habit_name, longest_streak_value = get_longest_streak(self.db)
        assert longest_streak_value >= 3  # Expected longest streak for test_habit_daily

        print(longest_streak_value)

    def teardown_method(self):
        """Cleanup the test database after each test."""
        import os
        if os.path.exists("test.db"):
            os.remove("test.db")