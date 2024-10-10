from pydantic import BaseModel
from typing import List, Dict, Tuple

class CreateGameModel(BaseModel):
    width: int = 50
    height: int = 50
    n_apples: int = 1
    die_border: bool = False

class DirectionSnakeModel(BaseModel):
    direction: Tuple[int, int]

class GameState():
    def __init__(
        self,
        size: Tuple[int, int],
        field: List[List], # 2D field
        snake: List[Tuple[int, int]],
        score: int,
        game_over: bool,
    ):
        self.size = size
        self.field = field # 2D field
        self.snake = snake
        self.score = score
        self.game_over = game_over

    def to_dict(self):
        return {
            "size": self.size,
            "field": self.field,
            "snake": self.snake,
            "score": self.score, 
            "game_over": self.game_over
        }