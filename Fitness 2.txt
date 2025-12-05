# Fitness App - OOP version with detailed comments

import csv
from datetime import date
from pathlib import Path


# FILE SETUP (unchanged from version 0.1, except cleaned slightly)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

WORKOUT_LOG = DATA_DIR / "workout_log.csv"


def get_today():
    """Returns today's date as a string in YYYY-MM-DD format."""
    return date.today().isoformat()


''' EXERCISE CLASS
This class replaces the dictionary used before.
The class lessons taught: 
- how to build constructors (__init__)
- how to store data in objects
- how to define instance methods'''

class Exercise:
    """Represents a single strength exercise entry (OOP upgrade)."""

    def __init__(self, name, sets, reps, weight):
        # Constructor: initializes the attributes for EACH Exercise object
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

    # Instance method: behavior associated with each exercise object
    def volume(self):
        """Return the training volume for this exercise."""
        return self.sets * self.reps * self.weight

    def to_dict(self, workout_date, workout_total_volume):
        """
        Converts object data into a dictionary specifically for saving to CSV.
        This replaces your original direct dictionary creation.
        """
        return {
            "date": workout_date,
            "exercise": self.name,
            "sets": self.sets,
            "reps": self.reps,
            "weight": self.weight,
            "total_volume": workout_total_volume,
        }

    def __str__(self):
        """
        Allows printing the exercise cleanly.
        This is part of OOP: defining how objects convert to readable text.
        """
        return f"{self.name}: {self.sets} sets x {self.reps} reps @ {self.weight} lbs"



# WORKOUT CLASS

class Workout:
    """
    A Workout 'has' many Exercise objects.
    This demonstrates composition — a key OOP concept taught in class.
    """

    def __init__(self, workout_date):
        # The Workout object stores the date and a list of Exercise objects
        self.date = workout_date
        self.exercises = []  # has-a relationship (Workout HAS Exercises)

    def add_exercise(self, exercise):
        """Add an Exercise object to this workout."""
        self.exercises.append(exercise)

    # RECURSION EXAMPLE

    def _total_volume_recursive(self, index):
        """Recursive helper function to compute total volume."""
        if index < 0:
            return 0  # base case
        return self.exercises[index].volume() + self._total_volume_recursive(index - 1)

    def total_volume(self):
        """Public method calling recursive helper."""
        return self._total_volume_recursive(len(self.exercises) - 1)

    # SAVE THE WORKOUT 
    # The course teaches how to group behavior with data using instance methods.

    def save_to_csv(self, filepath):
        """Save the workout to a CSV file using object data."""
        file_exists = filepath.exists()
        total_volume = self.total_volume()

        with open(filepath, mode="a", newline="") as file:
            fieldnames = ["date", "exercise", "sets", "reps", "weight", "total_volume"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                # Only write header the first time
                writer.writeheader()

            # Each Exercise to convert itself to CSV-compatible dict
            for ex in self.exercises:
                writer.writerow(ex.to_dict(self.date, total_volume))

        print(f"Workout saved to {filepath}! Total Volume: {total_volume} lbs")



# USER INPUT
def build_workout_from_input():
    """
    Builds a full Workout object by repeatedly collecting Exercise data.
    Demonstrates how instance objects are created and added to another class.
    """

    workout = Workout(get_today())  # Create a Workout object

    while True:
        name = input("Enter exercise name (or 'done' to finish): ")
        if name.lower() == "done":
            break

        # Same input validation as original code
        while True:
            try:
                sets = int(input("Sets: "))
                reps = int(input("Reps per set: "))
                weight = float(input("Weight (lbs): "))
                break
            except ValueError:
                print("Invalid input. Enter numeric values.")

        # Creates an Exercise OBJECT instead of a dictionary
        exercise = Exercise(name, sets, reps, weight)
        workout.add_exercise(exercise)
        print("Exercise added. Add another or type 'done' to finish.")

    return workout


# MAIN PROGRAM — Mostly unchanged, but now uses the new classes

def greeting():
    print("Welcome to the Fitness App v0.2 (OOP Edition)!")
    print("Track your workouts and stay fit!")
    print("-" * 40)
    print(f"Date: {get_today()}")


def main():
    greeting()

    # Build a full workout using OOP
    workout = build_workout_from_input()

    if not workout.exercises:
        print("No exercises logged. Exiting.")
        return

    # Save object to CSV
    workout.save_to_csv(WORKOUT_LOG)

    # Print summary using object methods
    print("\nWorkout Summary:")
    print(f"Total Volume: {workout.total_volume()} lbs")
    for ex in workout.exercises:
        print(f"- {ex}")


if __name__ == "__main__":
    main()
