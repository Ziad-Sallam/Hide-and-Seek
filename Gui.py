import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QMessageBox
)
from PyQt6 import uic
from PayoffMatrix import PayoffMatrix
from GameInterface import GameInterface


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Gui.ui", self)  
        self.setWindowTitle("Hide and Seek Game Theory")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()
        self.reset_game()
        
        
    def init_ui(self):
        self.start_btn.clicked.connect(self.start_game)
        self.reset_btn.clicked.connect(self.reset_game)
        self.sim_btn.clicked.connect(self.simulate_game)
        self.play_btn.clicked.connect(self.play_round)
        self.N.setValue(3)
        self.M.setValue(3)
        self.M.setEnabled(False)
        self.oneD.clicked.connect(self.update_world_type)
        self.twoD.clicked.connect(self.update_world_type)
            

    def reset_game(self):
        self.payoff = None
        self.interface = None
        self.rounds = 0
        self.player_score = 0
        self.computer_score = 0
        self.update_scoreboard()
        self.info_label.setText("Set world size and role, then click Start Game.")
        self.type_table.clear()
        self.matrix_table.clear()
        self.prob_table.clear()
        self.N.setValue(3)
        self.M.setValue(3)

    def start_game(self):
        n = self.N.value()
        m = self.M.value()
   
        role = 0 if self.hider_radio.isChecked() else 1

        self.payoff = PayoffMatrix(n, m) if self.twoD.isChecked() else PayoffMatrix(1, n)
        self.interface = GameInterface(self.payoff, role)
        self.rounds = 0
        self.player_score = 0
        self.computer_score = 0
        self.place_spin.setMaximum(n-1)
        self.update_tables()
        self.update_scoreboard()
        self.info_label.setText(f"Game started! You are the {'Hider' if role==0 else 'Seeker'}.")

    def update_tables(self):
        n = self.payoff.n
        m = self.payoff.m
        size = n * m

        # Update type_table
        self.type_table.clear()
        if n == 1:  # 1D world
            self.type_table.setRowCount(1)
            self.type_table.setColumnCount(m)
            for j in range(m):
                self.type_table.setItem(0, j, QTableWidgetItem(str(self.payoff.location_type[j])))
            self.type_table.setHorizontalHeaderLabels([str(j) for j in range(m)])
            self.type_table.setVerticalHeaderLabels(["Type"])
        else:  # 2D world
            self.type_table.setRowCount(n)
            self.type_table.setColumnCount(m)
            for i in range(n):
                for j in range(m):
                    idx = i * m + j
                    self.type_table.setItem(i, j, QTableWidgetItem(str(self.payoff.location_type[idx])))
            self.type_table.setHorizontalHeaderLabels([str(j) for j in range(m)])
            self.type_table.setVerticalHeaderLabels([str(i) for i in range(n)])

       
        self.matrix_table.clear()
        self.matrix_table.setRowCount(size)
        self.matrix_table.setColumnCount(size)
        for i in range(size):
            for j in range(size):
                self.matrix_table.setItem(i, j, QTableWidgetItem(str(self.payoff.matrix[i][j])))
        self.matrix_table.setHorizontalHeaderLabels([str(i) for i in range(size)])
        self.matrix_table.setVerticalHeaderLabels([str(i) for i in range(size)])

   
        self.prob_table.clear()
        self.prob_table.setRowCount(2)
        self.prob_table.setColumnCount(size)
        probs = self.payoff.probability
        for i in range(size):
            self.prob_table.setItem(0, i, QTableWidgetItem(f"{probs['Hider'][i]:.4f}"))
            self.prob_table.setItem(1, i, QTableWidgetItem(f"{probs['Seeker'][i]:.4f}"))
        self.prob_table.setVerticalHeaderLabels(["Hider", "Seeker"])
        self.prob_table.setHorizontalHeaderLabels([str(i) for i in range(size)])

    def update_world_type(self):
        if self.oneD.isChecked():
            self.N.setEnabled(True)
            self.M.setEnabled(False)
            self.M.setValue(1)
        elif self.twoD.isChecked():
            self.N.setEnabled(True)
            self.M.setEnabled(True)
            self.M.setValue(3)

        # Reset the game state
        self.reset_game()
        self.info_label.setText("Set world size and role, then click Start Game.")

    def play_round(self):
        if not self.interface:
            QMessageBox.warning(self, "Warning", "Start the game first!")
            return
        place = self.place_spin.value()
        self.interface.game(place)
        self.rounds += 1
        self.player_score = self.interface.player_score
        self.computer_score = self.interface.computer_score
        self.update_scoreboard()

    def simulate_game(self):
        if not self.interface:
            QMessageBox.warning(self, "Warning", "Start the game first!")
            return
        seeker_score, hider_score, seeker_choices, hider_choices = self.interface.simulate(100)
        self.info_label.setText(
            f"Simulation complete! Last seeker score: {seeker_score[-1]}, hider score: {hider_score[-1]}"
        )
        self.player_score = self.interface.player_score
        self.computer_score = self.interface.computer_score
        self.update_scoreboard()

    def update_scoreboard(self):
        self.score_label.setText(
            f"Rounds played: {self.rounds} | Player score: {self.player_score} | Computer score: {self.computer_score}"
        )
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())