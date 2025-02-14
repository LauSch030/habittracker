from db import add_habit, checkoff_habit, delete_habit, edit_habit

class Habit:

    def __init__(self, name: str, periodicity: str):
        """
        A class to represent a habit that a user wants to track.
        :param name: name of the habit
        :param periodicity: periodicity of the habit (e.g. daily, weekly,..)
        """
        self.name = name
        self.periodicity = periodicity

    def __str__(self):
        """
        Runs a string representation, showing its name. Useful for debugging and logging.
        :return: Habit and periodicity
        """
        return f"{self.name}: {self.periodicity}"

    def store(self, db):
        """
        Database functionality to store a habit.
        :param db: Database connection object.
        """
        add_habit(db, self.name, self.periodicity)

    def delete(self,db):
        """
        Deletes a Habit.
        :param db: Database connection object.
        """
        delete_habit(db, self.name, self.periodicity)
