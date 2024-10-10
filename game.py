import random
from typing import List, Dict, Tuple
from PIL import Image, ImageDraw
from .models import GameState

class Objects:
    apple = 5
    head = 2
    body = 1
    empty = 0

class Snake:
    def __init__(self, width: int, height: int, n_apples: int, die_border: bool):
        self.width = width
        self.height = height
        self.n_apples = n_apples
        self.die_border = die_border
        self.field = [[Objects.empty for _ in range(width)] for _ in range(height)]
        self.snake = [(height // 2, width // 2)]
        self.direction = (0, 1)  # Начальное направление - вправо
        self.score = 0
        self.game_over = False
        
        self._place_snake()
        self._place_apples()

    def _place_snake(self):
        head_y, head_x = self.snake[0]
        self.field[head_y][head_x] = Objects.head

    def _place_apples(self):
        apples_placed = 0
        while apples_placed < self.n_apples:
            y, x = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
            if self.field[y][x] == Objects.empty:
                self.field[y][x] = Objects.apple
                apples_placed += 1

    def move(self, new_direction: Tuple[int, int]):
        if self.game_over:
            return

        self.direction = new_direction
        new_head = self._get_new_head_position()

        if self._is_collision(new_head):
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        y, x = new_head

        if self.field[y][x] == Objects.apple:
            self.score += 1
            self._place_apples()
        else:
            tail = self.snake.pop()
            self.field[tail[0]][tail[1]] = Objects.empty

        self.field[y][x] = Objects.head
        if len(self.snake) > 1:
            y, x = self.snake[1]
            self.field[y][x] = Objects.body

    def _get_new_head_position(self) -> Tuple[int, int]:
        head_y, head_x = self.snake[0]
        dy, dx = self.direction
        new_y, new_x = head_y + dy, head_x + dx

        if not self.die_border:
            new_y %= self.height
            new_x %= self.width

        return new_y, new_x

    def _is_collision(self, position: Tuple[int, int]) -> bool:
        y, x = position
        if self.die_border and (y < 0 or y >= self.height or x < 0 or x >= self.width):
            return True
        return self.field[y][x] in [Objects.body, Objects.head]

    def get_game_state(self) -> GameState:
        return GameState(
            size=(self.width, self.height),
            field=self.field,
            snake=self.snake,
            score=self.score,
            game_over=self.game_over
        )
    
def visualize_game(game_state: GameState, cell_size: int = 20) -> Image.Image:
    width, height = game_state.size
    width_px = width * cell_size
    height_px = height * cell_size
    image = Image.new('RGB', (width_px, height_px), color='white')
    draw = ImageDraw.Draw(image)

    for y, row in enumerate(game_state.field):
        for x, cell in enumerate(row):
            color = 'white'
            if cell == Objects.empty:
                continue
            elif cell == Objects.apple:
                color = 'red'
            elif cell == Objects.head:
                color = 'green'
            elif cell == Objects.body:
                color = 'lightgreen'

            draw.rectangle(
                [x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size],
                fill=color,
                outline='black'
            )

    return image
