import random
import time
import pygame
from pygame.locals import *


SIZE = 25
# BACKGROUND_COLOR = (110, 110, 5)


class Apple:
    def __init__(self, parent_screen) -> None:
        self.image = pygame.image.load(
            "C:/Users/DELL/OneDrive/Desktop/sourcesofpyp/snakesources/st,small,507x507-pad,600x600,f8f8f8.u2 (1).jpg").convert()
        self.parent_screen = parent_screen
        self.x, self.y = SIZE*3, SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 38)*SIZE
        self.y = random.randint(0, 30)*SIZE


class Snake:
    def __init__(self, parent_screen, length) -> None:
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load(
            "C:/Users/DELL/OneDrive/Desktop/sourcesofpyp/snakesources/th (4) (1).jpeg").convert()
        self.x, self.y = [SIZE]*length, [SIZE]*length
        self.dir = "right"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        if self.dir != "right":
            self.dir = "left"

    def move_right(self):
        if self.dir != "left":
            self.dir = "right"

    def move_up(self):
        if self.dir != "down":
            self.dir = "up"

    def move_down(self):
        if self.dir != "up":
            self.dir = "down"

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.dir == "up":
            self.y[0] -= SIZE
        if self.dir == "down":
            self.y[0] += SIZE
        if self.dir == "left":
            self.x[0] -= SIZE
        if self.dir == "right":
            self.x[0] += SIZE
        self.draw()

    def draw(self):
        # self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        pygame.mixer.init()
        self.play_background()
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def play_background(self):
        pygame.mixer.music.load(
            "C:/Users/DELL/OneDrive/Desktop/sourcesofpyp/snakesources/Sakura-Girl-Motivation-chosic.com_.mp3")
        pygame.mixer.music.play()

    def play_sound(self, snd):
        sound = pygame.mixer.Sound(
            f"{snd}")
        pygame.mixer.Sound.play(sound)

    def background(self):
        bck = pygame.image.load(
            "C:/Users/DELL/OneDrive/Desktop/sourcesofpyp/snakesources/th.jpg")
        self.surface.blit(bck, (2, 2))

    def play(self):
        self.background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        # colliding with apple
        if self.is_collosion(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound(
                "C:/Users/DELL/OneDrive/Desktop/sourcesofpyp/snakesources/new-notification-on-your-device-138695.mp3")
            self.snake.increase_length()
            self.apple.move()
        # colloiding with itself
        for i in range(3, self.snake.length):
            if self.is_collosion(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound(
                    "C:/Users/DELL/OneDrive/Desktop/sourcesofpyp/snakesources/cartoon-comical-warbly-crash-190023.mp3")
                raise "Game Over"
        if self.snake.x[0] >= 1000 or self.snake.y[0] >= 800 or self.snake.x[0] <= 0 or self.snake.y[0] <= 0:
            self.play_sound(
                "C:/Users/DELL/OneDrive/Desktop/sourcesofpyp/snakesources/cartoon-comical-warbly-crash-190023.mp3")
            raise "Game Over"

    def is_collosion(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1 < y2+SIZE:
                return True
        return False

    def show_game_over(self):
        # self.surface.fill(BACKGROUND_COLOR)
        self.background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(
            f"Game is Over.Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(
            f"To play again press Enter.To exit press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()
        # time.sleep(0.5)

    def reset(self):
        self.snake = Snake(self.surface, 1)
        # self.snake.draw()
        self.apple = Apple(self.surface)
        # self.apple.draw()

    def run(self):
        flag = True
        pause = False
        while flag:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        flag = False
                    if event.key == K_RETURN:

                        pygame.mixer.music.unpause()
                        # pygame.mixer.Sound.stop()
                        pause = False
                    if not pause:
                        if event.key == K_UP or event.key == K_KP8:
                            self.snake.move_up()
                        if event.key == K_DOWN or event.key == K_KP2:
                            self.snake.move_down()
                        if event.key == K_LEFT or event.key == K_KP4:
                            self.snake.move_left()
                        if event.key == K_RIGHT or event.key == K_KP6:
                            self.snake.move_right()
                elif event.type == QUIT:
                    flag = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            if self.snake.length <= 10:
                time.sleep(0.4)
            elif self.snake.length <= 20:
                time.sleep(0.3)
            elif self.snake.length <= 30:
                time.sleep(0.2)
            else:
                time.sleep(0.1)


if __name__ == "__main__":
    game = Game()
    game.run()
