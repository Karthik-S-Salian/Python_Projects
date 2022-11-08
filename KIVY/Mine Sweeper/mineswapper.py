import random


class Minesweeper:

    def __init__(self, size: int, no_bombs: int = -1, no_bomb_dist=3) -> None:
        self.no_bomb_dist = no_bomb_dist
        self._init_board(size, no_bombs)

    def _init_board(self, size: int, no_bombs: int):
        self.dig_count=0
        self.size = size
        self.no_bombs = no_bombs
        self.board = [[[0, 0] for _ in range(size)] for _ in range(size)]

    def _generate_board(self, first_dig: tuple):
        # spawn bomb and assign value at same time
        # no bomb spawn with at sqaure no_bomb_dist - first_dig + no_bomb_dist zone
        # called after first dig
        # matrix contain tuple(has_dug/flaged,neigh_bombs_count/bomb_color) dug=1 , flaged =2 not_dug = 0

        bombs_planted = 0
        while (bombs_planted <= self.no_bombs):
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

            if self.board[x][y][1] < 0:
                continue
            elif ((first_dig[0] - self.no_bomb_dist < x < first_dig[0] + self.no_bomb_dist) and \
                  (first_dig[1] - self.no_bomb_dist < y < first_dig[1] + self.no_bomb_dist)):
                continue
            else:
                bombs_planted += 1
                for i in range(max(0, x - 1), min(self.size - 1, x + 2)):
                    for j in range(max(0, y - 1), min(self.size - 1, y + 2)):
                        if self.board[i][j][1] < 0:
                            continue
                        self.board[i][j][1] += 1
            self.board[x][y][1] = random.randint(-5, -1)

        self._dig(first_dig)

    def set_flag(self,loc):
        row, col = loc
        if self.board[row][col][0]:
            return False
        else:
            self.board[row][col][0]=2
            return True


    def _dig(self, loc):
        # dig at that location!
        # return True if successful dig, False if bomb dug
        # a couple of scenarios to consider:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors!
        row, col = loc

        if self.board[row][col][1] < 0:
            return False
        elif self.board[row][col][1] > 0:
            return True
        self.dig_count+=1
        for r in range(max(0, row - 1), min(self.size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.size - 1, col + 1) + 1):
                if self.board[row][col][0]:
                    continue  # don't dig where you've already dug/flaged
                self._dig((r, c))

        # if our initial dig didn't hit a bomb, we *shouldn't* hit a bomb here
        return True

    def is_game_won(self, dig_loc):
        # max dig = size*size -no_bombs

        # return (game_state , board_matrix)
        pass

    def __str__(self):
        txt = ""
        for i in self.board:
            for j in i:
                txt += " " + str(j)
            txt += "\n"
        return txt


if __name__ == "__main__":
    m = Minesweeper(10, 10)
    m._generate_board((5, 5))
    print(m)
