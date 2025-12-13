import csv

class Score:
    def __init__(self, value: float) -> None:
        self.value = value

class ScoreBook:
    def __init__(self, csv_filename: str) -> None:
        self.csv_filename = csv_filename
        self.scores = []
        self.name = ""

    def set_name(self, name: str) -> None:
        self.name = name

    def set_scores(self, values) -> None:
        self.scores = []
        i = 0
        while i < len(values):
            self.scores.append(Score(values[i]))
            i += 1

    def average_score(self) -> float:
        total = 0.0
        i = 0
        while i < len(self.scores):
            total += self.scores[i].value
            i += 1
        return total / len(self.scores)

    def save_to_csv(self) -> None:
        score_values = []
        i = 0
        while i < len(self.scores):
            score_values.append(self.scores[i].value)
            i += 1

        while len(score_values) < 4:
            score_values.append("")

        avg = self.average_score()

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
