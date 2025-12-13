import os
from PyQt6.QtWidgets import *
from scores_ui import Ui_MainWindow
from score_model import ScoreBook


class ScoreWindow(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scorebook = ScoreBook("scores.csv")
        folder = os.path.dirname(self.scorebook.csv_filename)
        if folder != "" and not os.path.exists(folder):
            # found this on the internet, through https://www.geeksforgeeks.org/python/python-check-if-a-file-or-directory-exists/
            self.show_error("Cannot save: folder for CSV does not exist")
            return

        self.ui.pushButtonCalculate.clicked.connect(self.on_calculate_clicked)
        self.ui.lineEditStudents.textChanged.connect(self.update_score_inputs)

        self.update_score_inputs()

    def show_error(self, message: str) -> None:
        self.ui.labelError.setStyleSheet("color: red;")
        self.ui.labelError.setText(message)
        self.ui.labelStatus.setText("")

    def clear_error(self) -> None:
        self.ui.labelError.setText("")

    def show_status(self, message: str) -> None:
        self.ui.labelStatus.setStyleSheet("color: green;")
        self.ui.labelStatus.setText(message)

    def clear_status(self) -> None:
        self.ui.labelStatus.setText("")

    def update_score_inputs(self) -> None:
        text = self.ui.lineEditStudents.text().strip()

        if text.isdigit():
            n = int(text)
        else:
            n = 0

        self.ui.labelScore1.setVisible(False)
        self.ui.lineEditScore1.setVisible(False)
        self.ui.labelScore2.setVisible(False)
        self.ui.lineEditScore2.setVisible(False)
        self.ui.labelScore3.setVisible(False)
        self.ui.lineEditScore3.setVisible(False)
        self.ui.labelScore4.setVisible(False)
        self.ui.lineEditScore4.setVisible(False)

        if 1 <= n <= 4:
            self.ui.labelScore1.setVisible(True)
            self.ui.lineEditScore1.setVisible(True)
        if 2 <= n <= 4:
            self.ui.labelScore2.setVisible(True)
            self.ui.lineEditScore2.setVisible(True)
        if 3 <= n <= 4:
            self.ui.labelScore3.setVisible(True)
            self.ui.lineEditScore3.setVisible(True)
        if 4 <= n <= 4:
            self.ui.labelScore4.setVisible(True)
            self.ui.lineEditScore4.setVisible(True)

    def on_calculate_clicked(self) -> None:
        self.clear_error()
        self.clear_status()

        name = self.ui.lineEditName.text().strip()
        if name == "":
            self.show_error("Please enter the student's name.")
            return

        attempts_text = self.ui.lineEditStudents.text().strip()
        if attempts_text == "":
            self.show_error("Please enter how many scores you want to submit (1-4).")
            return
        if not attempts_text.isdigit():
            self.show_error("Number of scores must be an integer from 1 to 4.")
            return

        attempts = int(attempts_text)
        if attempts < 1 or attempts > 4:
            self.show_error("Number of scores must be between 1 and 4.")
            return

        score_edits = [
            self.ui.lineEditScore1,
            self.ui.lineEditScore2,
            self.ui.lineEditScore3,
            self.ui.lineEditScore4
        ]

        values = []
        i = 0
        while i < attempts:
            raw = score_edits[i].text().strip()
            if raw == "":
                self.show_error(f"Score {i + 1} is required.")
                return

            try:
                number = float(raw)
            except ValueError:
                self.show_error("Scores must be numbers from 1 to 100.")
                return

            if number < 1 or number > 100:
                self.show_error("Scores must be numbers from 1 to 100.")
                return

            values.append(number)
            i += 1

        self.scorebook.set_name(name)
        self.scorebook.set_scores(values)

        average = self.scorebook.average_score()

        lines = []
        lines.append(f"Name: {name}")
        lines.append(f"Scores submitted: {attempts}")
        lines.append("Scores: " + ", ".join([str(v) for v in values]))
        lines.append(f"Average: {average:.2f}")

        self.ui.textEditOutput.setPlainText("\n".join(lines))

        self.scorebook.save_to_csv()
        self.show_status("Submitted")
