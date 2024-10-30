import subprocess
import sys
import random
import pygame

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])


class GameObject:
    def __init__(self, screen_width, screen_height):
        self.position = (screen_width // 2, screen_height // 2)
        self.body_color = None

    def draw(self, surface):
        raise NotImplementedError("Метод draw должен быть переопределён в дочерних классах.")

class Snake:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        self.length = 1
        self.positions = [(screen_width // 2, screen_height // 2)]
        self.direction = (cell_size, 0)
        self.next_direction = None
        self.body_color = (0, 255, 0)

    def update_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction or self.length == 1:
            self.next_direction = new_direction

    def move(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        new_head = (
            (self.positions[0][0] + self.direction[0]) % SCREEN_WIDTH,
            (self.positions[0][1] + self.direction[1]) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        for segment in self.positions:
            pygame.draw.rect(
                surface,
                self.body_color,
                (segment[0], segment[1], self.cell_size, self.cell_size)
            )

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (self.cell_size, 0)

class Apple:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        self.position = (0, 0)
        self.body_color = (255, 0, 0)
        self.randomize_position(screen_width, screen_height)

    def randomize_position(self, screen_width, screen_height):
        self.position = (
            random.randint(0, (screen_width - self.cell_size) // self.cell_size) * self.cell_size,
            random.randint(0, (screen_height - self.cell_size) // self.cell_size) * self.cell_size
        )

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.body_color,
            (self.position[0], self.position[1], self.cell_size, self.cell_size)
        )
def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.update_direction((0, -snake.cell_size))
            elif event.key == pygame.K_s:
                snake.update_direction((0, snake.cell_size))
            elif event.key == pygame.K_a:
                snake.update_direction((-snake.cell_size, 0))
            elif event.key == pygame.K_d:
                snake.update_direction((snake.cell_size, 0))
# Настройки игры
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")

snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

clock = pygame.time.Clock()

while True:
    handle_keys(snake)
    snake.move()

    # Проверка на поедание яблока
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Проверка на столкновение змейки с самой собой
    if len(snake.positions) != len(set(snake.positions)):
        snake.reset()

    # Отрисовка
    screen.fill((0, 0, 0))
    snake.draw(screen)
    apple.draw(screen)
    pygame.display.update()

    # Ограничение FPS
    clock.tick(10)