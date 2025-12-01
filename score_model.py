import csv

class Score:
    MIN_SCORE = 0
    MAX_SCORE = 100
    # Logic does not account for a MIN_SCORE less than 0. Both MIN_SCORE and MAX_SCORE must be whole numbers.

    def __init__(self, value: int) -> None:
        self.value = value

    def grade(self, best_score: int) -> str: #Logic as given by Lab 2
        if self.value >= best_score - 10:
            return "A"
        if self.value >= best_score - 20:
            return "B"
        if self.value >= best_score - 30:
            return "C"
        if self.value >= best_score - 40:
            return "D"
        return "F"

class GradeBook: #Creates GradeBook class to save scores to CSV
    def __init__(self, csv_filename: str) -> None:
        self.csv_filename = csv_filename
        self.scores = []

    def set_scores(self, values) -> None: #Adds scores as given by user to new list
        self.scores = []
        i = 0
        while i < len(values):
            score_object = Score(values[i])
            self.scores.append(score_object)
            i += 1

    def best_score(self) -> int: #Finds best score in scores
        best = self.scores[0].value
        i = 1
        while i < len(self.scores):
            if self.scores[i].value > best:
                best = self.scores[i].value
            i += 1
        return best

    def test_scores(self, raw: str, expected_count: int) -> None: #Logic for making sure scores inputted are valid
        range_message = (f"Please input a whole number from {Score.MIN_SCORE} to {Score.MAX_SCORE}.")

        parts = raw.split()

        if len(parts) < expected_count:
            raise ValueError(f"You must enter at least {expected_count} score(s).")

        parts = parts[:expected_count]

        values = []
        i = 0
        while i < len(parts):
            p = parts[i].strip()

            if not p.isdigit():
                raise ValueError(range_message)

            number = int(p)

            if number < 0:
                raise ValueError(range_message)

            if number < Score.MIN_SCORE or number > Score.MAX_SCORE:
                raise ValueError(range_message)

            values.append(number)
            i += 1

        self.set_scores(values)

    def save_to_csv(self) -> None:
        best = self.best_score()

        with open(self.csv_filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["student_number", "score", "grade"])

            i = 1
            for score in self.scores:
                writer.writerow([i, score.value, score.grade(best)])
                i += 1
