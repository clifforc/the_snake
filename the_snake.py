from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

WHITE_COLOR = (255, 255, 255)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Base class from which other game objects are inherited."""
    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self, surface):
        """Blank method for drawing an object on the playing field."""
        pass


class Apple(GameObject):
    """Class describing the apple and actions with it."""
    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.body_color = body_color

    def randomize_position(self):
        """Set random apple position."""
        self.position = ((randint(0, GRID_WIDTH-1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT-1) * GRID_SIZE))

    def draw(self, surface):
        """Draw apple"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Class describing the snake and its behavior."""
    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.body_color = body_color
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Update snake direction"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Update snake position on the game field"""
        head_position = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (head_position[0] + dx * GRID_SIZE,
                             head_position[1] + dy * GRID_SIZE)
        if new_head_position[0] < 0:
            new_head_position = (GRID_WIDTH * GRID_SIZE, new_head_position[1])
        elif new_head_position[0] >= GRID_WIDTH * GRID_SIZE:
            new_head_position = (0, new_head_position[1])
        if new_head_position[1] < 0:
            new_head_position = (new_head_position[0], GRID_HEIGHT * GRID_SIZE)
        elif new_head_position[1] >= GRID_HEIGHT * GRID_SIZE:
            new_head_position = (new_head_position[0], 0)
        if new_head_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Draw snake."""
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def check_apple_collision(self, apple):
        """Check snake collision with apple."""
        if self.get_head_position() == apple.position:
            self.length += 1
            apple.randomize_position()
            if apple.position in self.positions:
                apple.randomize_position()

    def get_head_position(self):
        """Get snake head position."""
        return self.positions[0]

    def reset(self):
        """Resets game to initial state with snake random direction."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Function that process user input."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def display_score(game_object):
    """Display score at top left corner."""
    font = pygame.font.Font(None, 30)
    text = font.render(f'SCORE: {game_object}', True,
                       WHITE_COLOR)
    text_rect = text.get_rect()
    text_rect.topleft = (0, 0)
    screen.blit(text, text_rect)


def main():
    apple = Apple()
    snake = Snake()
    apple.randomize_position()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.check_apple_collision(apple)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        display_score(snake.length - 1)
        pygame.display.update()


if __name__ == '__main__':
    main()
