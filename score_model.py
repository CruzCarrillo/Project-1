import csv
import os
from typing import List, Union


class Score:
    def __init__(self, value: float) -> None:
        """Create a score with a numeric value."""
        self.value: float = value


class ScoreBook:
    def __init__(self, csv_filename: str) -> None:
        """Create a score book that saves to a CSV file."""
        self.csv_filename: str = csv_filename
        self.scores: List[Score] = []
        self.name: str = ""

    def set_name(self, name: str) -> None:
        """Set the student's name."""
        self.name = name

    def set_scores(self, values: List[float]) -> None:
        """Set scores from a list of numeric values."""
        self.scores = []
        i = 0
        while i < len(values):
            self.scores.append(Score(values[i]))
            i += 1

    def average_score(self) -> float:
        """Return the average of current scores."""
        if len(self.scores) == 0:
            raise ZeroDivisionError("No scores to average.")

        total = 0.0
        i = 0
        while i < len(self.scores):
            total += self.scores[i].value
            i += 1
        return total / len(self.scores)

    def save_to_csv(self) -> None:
        """Save the current record to a CSV file."""
        score_values: List[Union[float, str]] = []
        i = 0
        while i < len(self.scores):
            score_values.append(self.scores[i].value)
            i += 1

        while len(score_values) < 4:
            score_values.append("")

        try:
            avg = self.average_score()
        except ZeroDivisionError:
            avg = 0.0

        try:
            folder = os.path.dirname(self.csv_filename)
            if folder != "" and not os.path.exists(folder):
                # found this on the internet, through https://www.geeksforgeeks.org/python/python-check-if-a-file-or-directory-exists/
                # we may have covered this, but I don't remember
                raise FileNotFoundError(f"Directory does not exist: {folder}")

            with open(self.csv_filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "name",
                    "score_1",
                    "score_2",
                    "score_3",
                    "score_4",
                    "average"
                ])
                writer.writerow([
                    self.name,
                    score_values[0],
                    score_values[1],
                    score_values[2],
                    score_values[3],
                    f"{avg:.2f}"
                ])
        except FileNotFoundError:
            raise
        except PermissionError:
            raise
        except OSError:
            raise
