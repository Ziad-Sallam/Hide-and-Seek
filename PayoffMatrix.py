import random
import numpy as np

from StrategyFinder import solve_zero_sum_game

class PayoffMatrix:
    def __init__(self,n: int,m: int) -> None:
        """
        initialize the payoff matrix

        :param n: number of rows
        :param m: number of columns

        """
        self.size = n*m
        self.n = n
        self.m = m
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.location_type = [0]*self.size
        self.initialize()

    def initialize(self) -> None:
        for i in range(self.size):
            self.location_type[i] = random.randint(1,3)

        for i in range(self.size):
            for j in range(self.size):
                ri, ci = self.to2d(i)
                rj, cj = self.to2d(j)
                self.matrix[i][j] = 1

                if self.location_type[i] == 2:
                    self.matrix[i][j] = 2

                if i == j :
                    self.matrix[i][j] = -1
                    if self.location_type[i] == 3:
                        self.matrix[i][j] = -3

        for i in range(self.size):
            row, col = self.to2d(i)
            done = [[False for _ in range(self.size)] for _ in range(self.size)]

            dx = [0,0,-1,1]
            dy = [1,-1,0,0]

            for j in range(len(dx)):
                if 0 <= row + dx[j] < self.n and 0 <= col + dy[j] < self.m and done[i][self.to1d(row+dx[j],col+dy[j])] == False:
                    done[i][self.to1d(row+dx[j],col+dy[j])] = True
                    self.matrix[i][self.to1d(row+dx[j],col+dy[j])] *=0.5
            dx = [0, 0, -2, 2]
            dy = [2, -2, 0, 0]

            for j in range(len(dx)):
                if 0 <= row + dx[j] < self.n and 0 <= col + dy[j] < self.m and done[i][self.to1d(row + dx[j], col + dy[j])] == False:
                    done[i][self.to1d(row + dx[j], col + dy[j])] = True
                    self.matrix[i][self.to1d(row + dx[j], col + dy[j])] *= 0.75

        self.probability = solve_zero_sum_game(self.matrix)


    def to2d(self,ind:int) -> tuple:
        return ind // self.m, ind % self.m

    def to1d(self,i: int, j: int) -> int:
        return (i) * self.m + j

if __name__ == "__main__":
    x = PayoffMatrix(2,3)
    print(x.location_type)
    for i in x.matrix:
        print(i)

    print("---------------------------------------------------------")
    result = x.probability

    print("Optimal strategy for Player A (x):", np.round(result['Hider'], 4))
    print("Optimal strategy for Player B (y):", np.round(result['Seeker'], 4))
    print("Game value (v):", np.round(result['Game value (v)'], 4))

