import os
from typing import List

from PyQt6.QtWidgets import QApplication, QMainWindow
from scores_ui import Ui_MainWindow
from score_model import ScoreBook


class ScoreWindow(QMainWindow):
    def __init__(self) -> None:
        """Create the main application window."""
        QMainWindow.__init__(self)

        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scorebook: ScoreBook = ScoreBook("scores.csv")

        self.ui.pushButtonCalculate.clicked.connect(self.on_calculate_clicked)
        self.ui.lineEditStudents.textChanged.connect(self.update_score_inputs)

        self.update_score_inputs()

    def show_error(self, message: str) -> None:
        """Display an error message."""
        self.ui.labelError.setText(message)
        self.ui.labelStatus.setText("")

    def clear_error(self) -> None:
        """Clear any error message."""
        self.ui.labelError.setText("")

    def show_status(self, message: str) -> None:
        """Display a status message."""
        self.ui.labelStatus.setText(message)

    def clear_status(self) -> None:
        """Clear any status message."""
        self.ui.labelStatus.setText("")

    def update_score_inputs(self) -> None:
        """Show or hide score inputs based on the number entered."""
        try:
            text = self.ui.lineEditStudents.text().strip()
        except Exception:
            self.show_error("Unexpected input error.")
            return

        if text.isdigit():
            try:
                n = int(text)
            except ValueError:
                n = 0
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
        """Validate inputs, display results, and save to csv."""
        self.clear_error()
        self.clear_status()

        try:
            name = self.ui.lineEditName.text().strip()
        except Exception:
            self.show_error("Unexpected input error.")
            return

        if name == "":
            self.show_error("Please enter the student's name.")
            return

        try:
            attempts_text = self.ui.lineEditStudents.text().strip()
        except Exception:
            self.show_error("Unexpected input error.")
            return

        if attempts_text == "":
            self.show_error("Please enter how many scores you want to submit (1-4).")
            return
        if not attempts_text.isdigit():
            self.show_error("Number of scores must be an integer from 1 to 4.")
            return

        try:
            attempts = int(attempts_text)
        except ValueError:
            self.show_error("Number of scores must be an integer from 1 to 4.")
            return

        if attempts < 1 or attempts > 4:
            self.show_error("Number of scores must be between 1 and 4.")
            return

        score_edits = [
            self.ui.lineEditScore1,
            self.ui.lineEditScore2,
            self.ui.lineEditScore3,
            self.ui.lineEditScore4
        ]

        values: List[float] = []
        i = 0
        while i < attempts:
            try:
                raw = score_edits[i].text().strip()
            except Exception:
                self.show_error("Unexpected input error.")
                return

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

        try:
            average = self.scorebook.average_score()
        except ZeroDivisionError:
            self.show_error("Cannot compute average with no scores.")
            return

        lines: List[str] = []
        lines.append(f"Name: {name}")
        lines.append(f"Scores submitted: {attempts}")
        lines.append("Scores: " + ", ".join([str(v) for v in values]))
        lines.append(f"Average: {average:.2f}")

        try:
            self.ui.textEditOutput.setPlainText("\n".join(lines))
        except Exception:
            self.show_error("Unexpected output error.")
            return

        try:
            folder = os.path.dirname(self.scorebook.csv_filename)
            if folder != "" and not os.path.exists(folder):
                # found this on the internet, through https://www.geeksforgeeks.org/python/python-check-if-a-file-or-directory-exists/
                self.show_error("Cannot save: folder for CSV does not exist.")
                return

            self.scorebook.save_to_csv()
        except FileNotFoundError:
            self.show_error("Cannot save: file or folder was not found.")
            return
        except PermissionError:
            self.show_error("Cannot save: permission denied.")
            return
        except OSError:
            self.show_error("Cannot save: an OS error occurred.")
            return

        self.show_status("Submitted")
