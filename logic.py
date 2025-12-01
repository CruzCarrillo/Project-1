import sys
from PyQt6.QtWidgets import *
from scores_ui import Ui_MainWindow
from score_model import GradeBook

class ScoreWindow(QMainWindow): #ui logic
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.gradebook = GradeBook("scores.csv")

        self.ui.pushButtonCalculate.clicked.connect(self.on_calculate_clicked)

    def show_error(self, message: str) -> None: #ui displaying errors
        self.ui.textEditOutput.setPlainText(message)
        self.statusBar().showMessage(message)

    def on_calculate_clicked(self) -> None:
        num_text = self.ui.lineEditStudents.text().strip()
        if num_text == "":
            self.show_error("Please enter the total number of students.") #for blank input
            return
        if not num_text.isdigit():
            self.show_error("Number of students must be an integer.") #for NaN input
            return
        num_students = int(num_text)
        if num_students <= 0:
            self.show_error("Number of students must be positive.") #for negative or 0 input
            return
        scores_text = self.ui.lineEditScores.text().strip()
        if scores_text == "":
            self.show_error("Please enter the student score(s).") #displays error in ui
            return

        try: #only have one exception
            self.gradebook.test_scores(scores_text, num_students)
        except ValueError as e:
            self.show_error(str(e))
            return

        best = self.gradebook.best_score()

        lines = []
        i = 1
        for score in self.gradebook.scores: #finds best score
            grade = score.grade(best)
            line = f"Student {i} score is {score.value} and grade is {grade}"
            lines.append(line)
            i += 1

        output = "\n".join(lines) #displays the final output in ui
        self.ui.textEditOutput.setPlainText(output)

        self.gradebook.save_to_csv()
        self.statusBar().showMessage("Saved to scores.csv")