import tkinter as tk
from tkinter import messagebox, ttk
from db import get_db, get_all_habits, checkoff_habit, delete_habit, edit_habit
from habit import Habit
from analyse import calculate_streak, get_habits_by_periodicity, get_longest_streak

class HabitTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit tracker")

        # Name of the habit, input field
        tk.Label(root, text="Habit name:").grid(row=0, column=0)
        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=0, column=1)

        # Periodicity (Dropdown)
        tk.Label(root, text="Periodicity:").grid(row=1, column=0)
        self.periodicity_options = ["daily", "weekly", "monthly", "bi-annually", "annually"]
        self.entry_period = ttk.Combobox(root, values=self.periodicity_options, state="readonly")
        self.entry_period.grid(row=1, column=1)
        self.entry_period.current(0)  # Set a standard value

        # Buttons for habit management
        tk.Button(root, text="Add habit", command=self.add_habit).grid(row=2, column=0, columnspan=2)
        tk.Button(root, text="Delete habit", command=self.delete_habit, fg="red").grid(row=3, column=0, columnspan=2)
        tk.Button(root, text="Edit Habit", command=self.edit_habit).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Track habit", command=self.track_habit).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Analyse Habit", command=self.analyse_habit).grid(row=6, column=0, columnspan=2)

        # Buttons for analytics
        tk.Button(root, text="Show All Habits", command=self.show_all_habits).grid(row=5, column=0, columnspan=2)
        tk.Button(root, text="Show Habits by Periodicity", command=self.show_habits_by_periodicity).grid(row=6, column=0, columnspan=2)
        tk.Button(root, text="Show Longest Streak", command=self.show_longest_streak).grid(row=7, column=0, columnspan=2)

        # List of habits
        self.habit_listbox = tk.Listbox(root, width=50)
        self.habit_listbox.grid(row=8, column=0, columnspan=2)
        self.load_habits()

    def add_habit(self):
        """Add a habit to the database and update the UI."""
        name = self.entry_name.get()
        periodicity = self.entry_period.get()
        if name:
            db = get_db()
            habit = Habit(name, periodicity)
            habit.store(db)
            db.close()
            messagebox.showinfo("Success", f"Habit '{name}' with periodicity '{periodicity}' added!")
            self.entry_name.delete(0, tk.END)  # Clear entry cell.
            self.load_habits()  # Update list.
        else:
            messagebox.showerror("Error", "Please enter a Habit name!")

    def delete_habit(self):
        """Delete a selected habit from the database and update UI."""
        selected_item = self.habit_listbox.curselection()
        if selected_item:
            habit_name = self.habit_listbox.get(selected_item).split(" - ")[0]  # Extract habit name.
            db = get_db()
            cur = db.cursor()
            cur.execute("DELETE FROM habit WHERE name=?", (habit_name,))
            cur.execute("DELETE FROM tracker WHERE habitName=?", (habit_name,))
            db.commit()
            db.close()
            messagebox.showinfo("Deleted", f"Habit '{habit_name}' deleted!")
            self.load_habits()  # Update list
        else:
            messagebox.showerror("Error", "Please select a habit to delete!")

    def edit_habit(self):
        """Edit the periodicity of a selected habit."""
        selected_item = self.habit_listbox.curselection()
        if selected_item:
            habit_name = self.habit_listbox.get(selected_item).split(" - ")[0]
            new_periodicity = self.entry_period.get()

            if not new_periodicity:
                messagebox.showerror("Error", "Please select a new periodicity!")
                return

            db = get_db()
            edit_habit(db, habit_name, new_periodicity)  # Call the edit function
            db.close()

            messagebox.showinfo("Updated", f"'{habit_name}' updated to periodicity: {new_periodicity}")
            self.load_habits()
        else:
            messagebox.showerror("Error", "Please select a habit to edit!")

    def track_habit(self):
        """Track a habit check-off and update UI."""
        selected_item = self.habit_listbox.curselection()
        if selected_item:
            habit_name = self.habit_listbox.get(selected_item).split(" - ")[0]
            db = get_db()
            checkoff_habit(db, habit_name)
            db.close()
            messagebox.showinfo("Tracked", f"Check-off for '{habit_name}' recorded!")
        else:
            messagebox.showerror("Error", "Please select a habit to track!")

    def load_habits(self):
        """Load all habits and display in listbox."""
        self.habit_listbox.delete(0, tk.END)
        db = get_db()
        habits = get_all_habits(db)
        db.close()
        for habit in habits:
            self.habit_listbox.insert(tk.END, f"{habit}")

    def analyse_habit(self):
        """Show streak analysis for the selected habit."""
        selected_item = self.habit_listbox.curselection()
        if selected_item:
            habit_name = self.habit_listbox.get(selected_item).split(" - ")[0]  # Extract name
            db = get_db()
            streak = calculate_streak(db, habit_name)
            db.close()
            messagebox.showinfo("Habit Analysis", f"🔥 Longest streak for '{habit_name}': {streak} days.")
        else:
            messagebox.showerror("Error", "Please select a habit to analyse!")

    def show_all_habits(self):
        """Show all tracked habits in a message box."""
        db = get_db()
        habits = get_all_habits(db)
        db.close()
        habit_list = "\n".join(habits) if habits else "No habits found."
        messagebox.showinfo("All Habits", habit_list)

    def show_habits_by_periodicity(self):
        """Show habits filtered by periodicity."""
        periodicity = self.entry_period.get()
        db = get_db()
        habits = get_habits_by_periodicity(db, periodicity)
        db.close()
        habit_list = "\n".join(habits) if habits else f"No {periodicity} habits found."
        messagebox.showinfo(f"Habits ({periodicity})", habit_list)

    def show_longest_streak(self):
        """Show the longest streak among all habits."""
        db = get_db()
        longest_streak = get_longest_streak(db)
        db.close()
        messagebox.showinfo("Longest Streak", f"🔥 Longest streak: {longest_streak} days.")


if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.mainloop()
