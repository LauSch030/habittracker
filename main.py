import click
from db import get_db, get_all_habits, checkoff_habit, delete_habit, edit_habit
from habit import Habit
from analyse import calculate_streak, get_habits_by_periodicity, get_longest_streak

@click.group()
def cli():
    """Habit Tracker CLI - Manage your habits via command line."""
    pass

@click.command()
@click.argument("name")
@click.argument("periodicity", type=click.Choice(["daily", "weekly", "monthly", "bi-annually", "annually"], case_sensitive=False))
def create(name, periodicity):
    """Create a new habit."""
    db = get_db()
    habit = Habit(name, periodicity)
    habit.store(db)
    db.close()
    click.echo(f"✅ Habit '{name}' with periodicity '{periodicity}' added!")

@click.command()
@click.argument("name")
def delete(name):
    """Delete a habit from the database."""
    db = get_db()
    delete_habit(db, name)
    db.close()
    click.echo(f"✅ Habit '{name}' deleted!")

    db.close()

@click.command()
@click.argument("name")
@click.argument("new_periodicity", type=click.Choice(["daily", "weekly", "monthly", "bi-annually", "annually"], case_sensitive=False))
def edit(name, new_periodicity):
    """Update the periodicity of a habit."""
    db = get_db()
    edit_habit(db, name, new_periodicity)
    db.close()
    click.echo(f"✅ Habit '{name}' updated to periodicity '{new_periodicity}'.")

@click.command()
@click.argument("name")
@click.option("--date", default=None, help="Date of completion (YYYY-MM-DD). Defaults to today.")
def checkoff(name, date):
    """Log a completion for a habit (check-off)."""
    db = get_db()

    if not date:
        from datetime import date as dt
        date = dt.today().isoformat()

    checkoff_habit(db, name, date)
    db.close()
    click.echo(f"✅ Check-off logged for habit '{name}' on {date}.")


@click.command()
def list_habits():
    """List all currently tracked habits."""
    db = get_db()
    habits = get_all_habits(db)
    db.close()

    if habits:
        click.echo("📋 Your tracked habits:")
        for habit in habits:
            click.echo(f"- {habit}")
    else:
        click.echo("⚠️ No habits found.")

@click.command()
@click.argument("periodicity",
                type=click.Choice(["daily", "weekly", "monthly", "bi-annually", "annually"], case_sensitive=False))
def list_by_periodicity(periodicity):
    """List all habits with a specific periodicity."""
    db = get_db()
    habits = get_habits_by_periodicity(db, periodicity)
    db.close()
    if habits:
        click.echo(f"📆 Habits with periodicity '{periodicity}':")
        for habit in habits:
            click.echo(f"- {habit}")
    else:
        click.echo(f"⚠️ No habits found for periodicity '{periodicity}'.")


@click.command()
def longest_streak():
    """Show the habit with the longest streak."""
    db = get_db()
    best_habit, max_streak = get_longest_streak(db)
    db.close()
    if best_habit:
        click.echo(f"🏆 Longest streak: '{best_habit}' with {max_streak} days!")
    else:
        click.echo("⚠️ No habit streaks found.")


cli.add_command(create)
cli.add_command(delete)
cli.add_command(checkoff)
cli.add_command(edit)
cli.add_command(list_habits)
cli.add_command(list_by_periodicity)
cli.add_command(longest_streak)

if __name__ == "__main__":
    cli()
