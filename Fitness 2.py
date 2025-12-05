# Fitness app v0.3 - Working towards a GUI w/ menu

import csv
from datetime import date
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

# FILE SETUP
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
WORKOUT_LOG = DATA_DIR / "workout_log.csv"


def get_today():
    """Returns today's date as a string in YYYY-MM-DD format."""
    return date.today().isoformat()


# EXERCISE CLASS
class Exercise:
    """Represents a single strength exercise entry (OOP upgrade)."""

    def __init__(self, name, sets, reps, weight):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

    def volume(self):
        """Return the training volume for this exercise."""
        return self.sets * self.reps * self.weight

    def to_dict(self, workout_date, workout_total_volume):
        """Convert to dict for saving to CSV."""
        return {
            "date": workout_date,
            "exercise": self.name,
            "sets": self.sets,
            "reps": self.reps,
            "weight": self.weight,
            "total_volume": workout_total_volume,
        }

    def __str__(self):
        """String representation for listbox / summary."""
        return f"{self.name}: {self.sets} sets x {self.reps} reps @ {self.weight} lbs"


# WORKOUT CLASS

class Workout:
    """A Workout 'has' many Exercise objects (composition)."""

    def __init__(self, workout_date):
        self.date = workout_date
        self.exercises = []

    def add_exercise(self, exercise):
        """Add an Exercise object to this workout."""
        self.exercises.append(exercise)

    def _total_volume_recursive(self, index):
        """Recursive helper function to compute total volume."""
        if index < 0:
            return 0
        return self.exercises[index].volume() + self._total_volume_recursive(index - 1)

    def total_volume(self):
        """Public method calling recursive helper."""
        return self._total_volume_recursive(len(self.exercises) - 1)

    def save_to_csv(self, filepath):
        """Save the workout to a CSV file using object data."""
        file_exists = filepath.exists()
        total_volume = self.total_volume()

        with open(filepath, mode="a", newline="") as file:
            fieldnames = ["date", "exercise", "sets", "reps", "weight", "total_volume"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for ex in self.exercises:
                writer.writerow(ex.to_dict(self.date, total_volume))

        print(f"Workout saved to {filepath}! Total Volume: {total_volume} lbs")


# GUI FRONTEND

class WorkoutAppGUI:
    """Using tkinter to build a GUI for the fitness app."""

    # NOTE: now takes root as parameter
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness App V0.3")

        # current workout model
        self.workout = Workout(get_today())

        # build GUI
        self._build_menu()
        self._build_main_ui()
        self.update_summary()

    # MENU BAR 
    def _build_menu(self):
        menubar = tk.Menu(self.root)

        # file menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Workout", command=self.new_workout)
        file_menu.add_command(label="Save Workout", command=self.save_workout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    # MAIN UI 
    def _build_main_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # labels
        tk.Label(frame, text="Exercise Name:").grid(row=0, column=0, sticky="e")
        tk.Label(frame, text="Sets:").grid(row=1, column=0, sticky="e")   # fixed Label typo
        tk.Label(frame, text="Reps:").grid(row=2, column=0, sticky="e")
        tk.Label(frame, text="Weight (lbs):").grid(row=3, column=0, sticky="e")

        # entry widgets
        self.name_var = tk.StringVar()
        self.sets_var = tk.StringVar()
        self.reps_var = tk.StringVar()
        self.weight_var = tk.StringVar()

        tk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=2)
        tk.Entry(frame, textvariable=self.sets_var).grid(row=1, column=1, padx=5, pady=2)
        tk.Entry(frame, textvariable=self.reps_var).grid(row=2, column=1, padx=5, pady=2)
        tk.Entry(frame, textvariable=self.weight_var).grid(row=3, column=1, padx=5, pady=2)

        # button
        add_btn = tk.Button(frame, text="Add Exercise", command=self.add_exercise)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # listbox for exercise display
        tk.Label(frame, text="Exercises:").grid(
            row=5, column=0, columnspan=2, sticky="w", pady=(10, 0)
        )
        self.exercise_listbox = tk.Listbox(frame, width=50, height=8)
        self.exercise_listbox.grid(row=6, column=0, columnspan=2, pady=5, sticky="we")

        # summary
        self.summary_label = tk.Label(
            frame,
            text="Total Volume: 0 lbs",
            font=("Times New Roman", 12, "bold"),
        )
        self.summary_label.grid(row=7, column=0, columnspan=2, pady=(10, 0))

    # BUTTON / MENU FUNCTIONS 
    def add_exercise(self):
        """Read fields, validate, create Exercise object, add to workout."""
        name = self.name_var.get()
        sets = self.sets_var.get()
        reps = self.reps_var.get()
        weight = self.weight_var.get()

        if not name:
            messagebox.showerror("Input Error", "Exercise name is required.")
            return

        try:
            sets = int(sets)
            reps = int(reps)
            weight = float(weight)
        except ValueError:
            messagebox.showerror(
                "Input Error", "Sets, Reps, and Weight must be numeric."
            )
            return

        ex = Exercise(name, sets, reps, weight)
        self.workout.add_exercise(ex)
        self.exercise_listbox.insert(tk.END, str(ex))

        self.clear_inputs()
        self.update_summary()

    def clear_inputs(self):
        """Reset data fields."""
        self.name_var.set("")
        self.sets_var.set("")
        self.reps_var.set("")
        self.weight_var.set("")

    def update_summary(self):
        """Update total volume label."""
        total = self.workout.total_volume()
        self.summary_label.config(text=f"Total Volume: {total} lbs")

    def new_workout(self):
        """Start a new workout (menu: File → New Workout)."""
        if self.workout.exercises:
            confirm = messagebox.askyesno(
                "New Workout",
                "Start a new workout? Unsaved data will be lost.",
            )
            if not confirm:
                return

        self.workout = Workout(get_today())
        self.exercise_listbox.delete(0, tk.END)
        self.update_summary()
        self.clear_inputs()

    def save_workout(self):
        """Save workout to CSV."""
        if not self.workout.exercises:
            messagebox.showinfo("Save Workout", "No exercises to save.")
            return

        self.workout.save_to_csv(WORKOUT_LOG)
        messagebox.showinfo("Save Workout", "Workout saved successfully!")

    def show_about(self):
        """Show About dialog."""
        messagebox.showinfo(
            "About",
            "Fitness App V0.3\nTrack your workouts with a GUI!\nDeveloped with Python & Tkinter.",
        )


# MAIN ENTRY POINT

def main():
    root = tk.Tk()
    app = WorkoutAppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
