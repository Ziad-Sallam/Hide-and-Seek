import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QButtonGroup, QPushButton
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
        self.oneD.clicked.connect(self.update_world_type)
        self.twoD.clicked.connect(self.update_world_type)
        self.next_round_btn.clicked.connect(self.prepare_next_round)

        self.N.setValue(3)
        self.M.setValue(3)
        self.M.setEnabled(False)
        self.oneD.clicked.connect(self.update_world_type)
        self.twoD.clicked.connect(self.update_world_type)

        self.dim_group = QButtonGroup(self)
        self.dim_group.addButton(self.oneD)
        self.dim_group.addButton(self.twoD)
        self.role_group = QButtonGroup(self)
        self.role_group.addButton(self.hider_radio)
        self.role_group.addButton(self.seeker_radio)
        self.oneD.setChecked(True)
        self.hider_radio.setChecked(True)
        self.next_round_btn.setEnabled(False)
        self.update_world_type()

    def reset_game(self):
        self.payoff = None
        self.interface = None
        self.rounds = 0
        self.player_score = 0
        self.computer_score = 0
        self.update_scoreboard()
        self.info_label.setText("Set world size and role, then click Start Game.")
        self.matrix_table.clear()
        self.prob_table.clear()
        self.place_table.clear()
        self.N.setValue(3)
        self.M.setValue(3)
        self.next_round_btn.setEnabled(False)

    def start_game(self):
        n = self.N.value()
        m = self.M.value()
        role = 0 if self.hider_radio.isChecked() else 1

        self.payoff = PayoffMatrix(n, m) if self.twoD.isChecked() else PayoffMatrix(1, n)
        self.interface = GameInterface(self.payoff, role)
        self.rounds = 0
        self.player_score = 0
        self.computer_score = 0
        self.update_tables()
        self.update_scoreboard()
        self.info_label.setText(f"Game started! You are the {'Hider' if role==0 else 'Seeker'}.")
        self.prepare_place_table()
        self.next_round_btn.setEnabled(False)

    def update_tables(self):
        n = self.payoff.n
        m = self.payoff.m
        size = n * m
       
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

        # Place table for selection
        self.prepare_place_table()

    def prepare_place_table(self):
        n = self.payoff.n
        m = self.payoff.m
        self.place_table.clear()
        self.place_table.setRowCount(n)
        self.place_table.setColumnCount(m)
        self.button_refs = {}  # Store buttons for color reset
        for i in range(n):
            for j in range(m):
                idx = i * m + j
                btn = QPushButton(f"{idx}")
                self.set_button_color(btn, self.payoff.location_type[idx])
                btn.clicked.connect(lambda _, idx=idx: self.place_selected(idx))
                self.place_table.setCellWidget(i, j, btn)
                self.button_refs[idx] = btn
        self.place_table.setHorizontalHeaderLabels([str(j) for j in range(m)])
        self.place_table.setVerticalHeaderLabels([str(i) for i in range(n)])

    def place_selected(self, idx):
        if not self.interface:
            QMessageBox.warning(self, "Warning", "Start the game first!")
            return
        # Play the round
        self.interface.game(idx)
        self.rounds += 1
        self.player_score = self.interface.player_score
        self.computer_score = self.interface.computer_score
        player_choice = self.interface.player_choices[-1]
        computer_choice = self.interface.computer_choices[-1]
        self.info_label.setText(
            f"Your selection: {player_choice} | Computer selection: {computer_choice}"
        )
        self.update_scoreboard()
        # Disable all buttons until next round
        for btn in self.button_refs.values():
            btn.setEnabled(False)
        # Highlight choices
        self.highlight_choices(player_choice, computer_choice)
        self.next_round_btn.setEnabled(True)

    def prepare_next_round(self):
        # Reset all buttons to their original color and enable
        self.reset_button_colors()
        for btn in self.button_refs.values():
            btn.setEnabled(True)
        self.info_label.setText("Choose your place for the next round.")
        self.next_round_btn.setEnabled(False)
        
    def set_button_color(self, btn, type_value):
        # Set color based on type
        if type_value == 1:
            btn.setStyleSheet("background-color: blue; color: white;")
        elif type_value == 2:
            btn.setStyleSheet("background-color: green; color: white;")
        elif type_value == 3:
            btn.setStyleSheet("background-color: red; color: white;")
        else:
            btn.setStyleSheet("")

    def highlight_choices(self, player_idx, computer_idx):
        # Mark both yellow if different, black if same
        if player_idx == computer_idx:
            self.button_refs[player_idx].setStyleSheet("background-color: black; color: white;")
        else:
            self.button_refs[player_idx].setStyleSheet("background-color: yellow; color: black;")
            self.button_refs[computer_idx].setStyleSheet("background-color: yellow; color: black;")

    def reset_button_colors(self):
        # Reset all buttons to their original color
        for idx, btn in self.button_refs.items():
            self.set_button_color(btn, self.payoff.location_type[idx])    

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