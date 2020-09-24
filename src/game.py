import pygame

pygame.init()

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHT_YELLOW = (255, 255, 204)
MARGIN_HOR = 105
MARGIN_VER = 100
FONT = pygame.font.Font(r"src\resources\fonts\Ranchers-Regular.ttf", 30)


class GameTable:
    def __init__(self, size_h=490, size_v=490, radius=25):
        self.size_h = size_h
        self.size_v = size_v
        self.radius = radius
        # self.dots_data field stores any changes to game table. Value 0 represents empty dot, value 1 represents point
        # of player 1 and value 2 represents point of player 2. At the beginning, game table is empty
        self.dots_data = [[0 for _ in range(6)] for _ in range(6)]
        # self.coordinates list contains coordinates of dots' center
        self.coordinates = [[(0, 0) for _ in range(6)] for _ in range(6)]
        v = MARGIN_VER
        for i in range(len(self.coordinates)):
            h = MARGIN_HOR
            v += self.size_v / 7
            for j in range(len(self.coordinates[i])):
                h += self.size_h / 7
                self.coordinates[i][j] = (int(h), int(v))
        # self.turn field stores players' turn (1 for player1, 2 for player2 and -1 when someone wins, -2 when its tie)
        self.turn = 1
        # coordinates of game chip
        self.playing_coord_ver = 65
        self.playing_coord_hor = MARGIN_HOR + int(self.size_h / 7)
        self.winner = 0

    def draw(self, screen, color=LIGHT_YELLOW):
        """Prints a gaming table"""
        screen.fill(BLACK)
        pygame.draw.rect(screen, color, (MARGIN_HOR, MARGIN_VER, self.size_v, self.size_h))
        for i in range(len(self.dots_data)):
            for j in range(len(self.dots_data[i])):
                if self.dots_data[i][j] == 0:
                    # playing cell is empty
                    pygame.draw.circle(screen, BLACK, self.coordinates[i][j], self.radius)
                elif self.dots_data[i][j] == 1:
                    # chip of player 1 in playing cell
                    pygame.draw.circle(screen, RED, self.coordinates[i][j], self.radius)
                elif self.dots_data[i][j] == 2:
                    # chip of player 2 in playing cell
                    pygame.draw.circle(screen, BLUE, self.coordinates[i][j], self.radius)

        # if game table is filled and no one won, it's tie
        if self.dots_data[0].count(0) == 0:
            self.turn = -2
            return

        if self.turn == 1:
            pygame.draw.circle(screen, RED, (self.playing_coord_hor, self.playing_coord_ver), self.radius)
        elif self.turn == 2:
            pygame.draw.circle(screen, BLUE, (self.playing_coord_hor, self.playing_coord_ver), self.radius)
        self.game_turn(screen)

    def move(self, direction):
        """Function for event of pressing left or right buttons.
        Moves game chip on horizontal axis"""

        if direction == "left" and self.playing_coord_hor > MARGIN_HOR + int(self.size_h / 7):
            self.playing_coord_hor -= int(self.size_h / 7)
        elif direction == "right" and self.playing_coord_hor < MARGIN_HOR + int(self.size_h / 7) * 6:
            self.playing_coord_hor += int(self.size_h / 7)

    def fall(self):
        """Function for event of pressing down or return buttons.
        Drops game chip into playing board"""

        # horizontal and vertical index
        ind_h = int((self.playing_coord_hor - MARGIN_HOR) / (self.size_h / 7)) - 1
        ind_v = 0

        # you can't place game chip when column is filled
        if self.dots_data[ind_v][ind_h] != 0:
            return
        # filling chips from bottom
        while self.dots_data[ind_v][ind_h] == 0:
            ind_v += 1
            if ind_v == 6:
                break

        # filling playing cell with chip of each player (1 for player1, 2 for player2)
        self.dots_data[ind_v - 1][ind_h] = self.turn

        # checking if four chips are standing in a row or in a column or on a diagonal
        if self.is_covered():
            # game ends
            self.winner = self.turn
            self.turn = -1
            return
        # changing player's turn
        self.turn = 1 if self.turn == 2 else 2

    def is_covered(self):
        """Checks if there four game chips of one color in a row or in a column or on a diagonal"""
        for i in range(5, -1, -1):

            # on rows (3 - 5) algorithm checks rows, columns, diagonals
            if 3 <= i <= 5:

                for j in range(6):
                    # algorithm checks columns on all j indexes
                    col = [self.dots_data[i][j], self.dots_data[i - 1][j], self.dots_data[i - 2][j],
                           self.dots_data[i - 3][j]]

                    # column
                    if len(set(col)) == 1 and set(col) != {0}:
                        return True

                    if 0 <= j <= 2:
                        # algorithm checks rows and right diagonals on j indexes from 0 to 2
                        row = self.dots_data[i][j:j + 4]
                        right_diag = [self.dots_data[i][j], self.dots_data[i - 1][j + 1], self.dots_data[i - 2][j + 2],
                                      self.dots_data[i - 3][j + 3]]

                        # row / right diagonal
                        if (len(set(row)) == 1 and set(row) != {0})\
                                or (len(set(right_diag)) == 1 and set(right_diag) != {0}):
                            return True

                    elif j >= 3:
                        # algorithm checks left diagonals on j indexes from 3 to 5
                        left_diag = [self.dots_data[i][j], self.dots_data[i - 1][j - 1], self.dots_data[i - 2][j - 2],
                                     self.dots_data[i - 3][j - 3]]

                        # left diagonal
                        if (len(set(left_diag)) == 1) and set(left_diag) != {0}:
                            return True

            # on rows (0 - 2) algorithm checks only rows
            elif i <= 2:
                for j in range(3):
                    # on j indexes from 0 to 2
                    row = self.dots_data[i][j:j + 4]
                    # row
                    if len(set(row)) == 1 and set(row) != {0}:
                        return True

        return False

    def restart(self, game_end):
        """Restarts the game"""
        self.dots_data = [[0 for _ in range(6)] for _ in range(6)]
        self.turn = 1
        self.winner = 0
        self.playing_coord_ver = 65
        self.playing_coord_hor = MARGIN_HOR + int(self.size_h / 7)
        game_end.__init__(game_end.screen)

    def game_turn(self, screen):
        if self.turn == 1:
            text = FONT.render(f"P l a y e r  {self.turn} ' s  t u r n", 1, RED)
            screen.blit(text, (175, 600))
        elif self.turn == 2:
            text = FONT.render(f"P l a y e r  {self.turn} ' s  t u r n", 1, BLUE)
            screen.blit(text, (315, 600))
        else:
            return


class End:
    def __init__(self, screen):
        self.screen = screen
        self.surface = pygame.Surface((300, 100))
        self.surface.fill(WHITE)
        self.surface.set_alpha(220)

    def end(self, game_table, result="victory"):
        if result == "victory":
            final_word = FONT.render(f"P l a y e r   {game_table.winner}   w i n s", 1, BLACK)
        else:
            final_word = FONT.render(f"F r i e n d s h i p   w i n s", 1, BLACK)
        self.screen.blit(self.surface, (200, 270))
        self.surface.blit(final_word, (50, 30))
