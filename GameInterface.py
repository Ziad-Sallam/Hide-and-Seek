import numpy as np

from PayoffMatrix import PayoffMatrix


class GameInterface:
    def __init__(self, payoff_matrix: PayoffMatrix, perspective: int):
        """
        :param payoff_matrix (PayoffMatrix): the game matrix object
        :param perspective: 0 if player chose to hide, 1 if player chose to seek
        """
        self.payoff_matrix = payoff_matrix
        self.perspective = perspective
        self.player_score =0
        self.computer_score = 0
        self.score = 0
        self.computer_choices = []
        self.player_choices = []


    def game(self, place :int):
        """
        :param place: the place the player has chosen
        :return:
        """

        choices = []
        self.player_choices.append(place)
        for i in range(self.payoff_matrix.size):
            choices.append(i)
        if self.perspective == 0:
            values = self.payoff_matrix.probability['Seeker']
        else:
            values = self.payoff_matrix.probability['Hider']

        print(values)

        x = np.random.choice(choices, 1, p=values)[0]
        self.computer_choices.append(x)
        print(x)
        if self.perspective == 0:
            self.score += self.payoff_matrix.matrix[place][x]
            if x == place:
                self.computer_score -= self.payoff_matrix.matrix[place][x]
                self.player_score += self.payoff_matrix.matrix[place][x]
            else:
                self.player_score += self.payoff_matrix.matrix[place][x]
                self.computer_score -= self.payoff_matrix.matrix[place][x]

        else:
            self.score += self.payoff_matrix.matrix[x][place]
            if x == place:
                self.computer_score -= self.payoff_matrix.matrix[x][place]
                self.player_score += self.payoff_matrix.matrix[x][place]
            else:
                self.player_score += self.payoff_matrix.matrix[x][place]
                self.computer_score -= self.payoff_matrix.matrix[x][place]


    def simulate(self,number_of_games):
        choices = []
        for i in range(self.payoff_matrix.size):
            choices.append(i)

        seeker_values = self.payoff_matrix.probability['Seeker']
        hider_values = self.payoff_matrix.probability['Hider']

        seeker_choices = np.random.choice(choices, number_of_games, p=seeker_values)
        hider_choices = np.random.choice(choices, number_of_games, p=hider_values)
        seeker_score = [0]
        hider_score = [0]
        if seeker_choices[0] == hider_choices[0]:
            seeker_score[0] =(self.payoff_matrix.matrix[seeker_choices[0]][hider_choices[0]])*-1
        else:
            hider_score[0] = (self.payoff_matrix.matrix[hider_choices[0]][seeker_choices[0]])

        for i in range(1,number_of_games):
            if hider_choices[i] != seeker_choices[i]:
                hider_score.append(hider_score[i-1] + (self.payoff_matrix.matrix[hider_choices[i]][seeker_choices[i]]))
                seeker_score.append(seeker_score[i-1])
            else:
                seeker_score.append(seeker_score[i-1] + (self.payoff_matrix.matrix[hider_choices[i]][seeker_choices[i]])*-1)
                hider_score.append(hider_score[i-1])

        return seeker_score, hider_score, seeker_choices, hider_choices


mat = PayoffMatrix(2,2)
ss,hs,_,q = GameInterface(mat, 0).simulate(10)
for i in range(mat.size):
    print(mat.matrix[i])
result = mat.probability

print("Optimal strategy for Player A (x):", np.round(result['Hider'], 4))
print("Optimal strategy for Player B (y):", np.round(result['Seeker'], 4))
print("Game value (v):", np.round(result['Game value (v)'], 4))
print()
print("seeker choices: ",_)
print("hider choices: ",q)
print(ss)
print(hs)


