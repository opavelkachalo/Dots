import pygame
from src import game
from src.game import GameTable

FPS = 60
WIDTH = 700
HEIGHT = 650

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DOTS")

clock = pygame.time.Clock()

gameIcon = pygame.image.load(r"src\resources\icon.png")
pygame.display.set_icon(gameIcon)

gameTable = GameTable()

gameEnd = game.End(screen)


def main():
    game_running = True

    while game_running:
        pygame.display.update()

        gameTable.draw(screen)

        if gameTable.turn == -1:
            gameEnd.end(gameTable)
        elif gameTable.turn == -2:
            gameEnd.end(gameTable, result="tie")

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                game_running = False
            elif i.type == pygame.KEYDOWN:
                if gameTable.turn != -1:
                    if i.key == pygame.K_LEFT:
                        gameTable.move(direction="left")
                    elif i.key == pygame.K_RIGHT:
                        gameTable.move(direction="right")
                    elif i.key == pygame.K_RETURN or i.key == pygame.K_DOWN:
                        gameTable.fall()
                if i.key == pygame.K_r:
                    gameTable.restart(gameEnd)

        clock.tick(FPS)


if __name__ == "__main__":
    main()
