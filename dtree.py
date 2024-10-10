import random
from typing import List, Tuple
from models import GameState
from game import Snake

class DecisionTree:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    def make_decision(self, game_state: GameState) -> Tuple[int, int]:
        head = game_state.snake[0]
        apples = self._find_apples(game_state.field)
        
        if apples:
            closest_apple = min(apples, key=lambda a: self._manhattan_distance(head, a))
            return self._move_towards(head, closest_apple, game_state)
        else:
            return self._random_safe_move(head, game_state)

    def _find_apples(self, field: List[List[int]]) -> List[Tuple[int, int]]:
        return [(y, x) for y in range(self.height) for x in range(self.width) if field[y][x] == 5]

    def _manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _move_towards(self, head: Tuple[int, int], target: Tuple[int, int], game_state: GameState) -> Tuple[int, int]:
        possible_moves = self._get_safe_moves(head, game_state)
        if not possible_moves:
            return random.choice(self.directions)

        best_move = min(possible_moves, key=lambda m: self._manhattan_distance(
            ((head[0] + m[0]) % self.height, (head[1] + m[1]) % self.width),
            target
        ))
        return best_move

    def _random_safe_move(self, head: Tuple[int, int], game_state: GameState) -> Tuple[int, int]:
        safe_moves = self._get_safe_moves(head, game_state)
        return random.choice(safe_moves) if safe_moves else random.choice(self.directions)

    def _get_safe_moves(self, head: Tuple[int, int], game_state: GameState) -> List[Tuple[int, int]]:
        return [
            direction for direction in self.directions
            if self._is_safe_move(head, direction, game_state)
        ]

    def _is_safe_move(self, head: Tuple[int, int], direction: Tuple[int, int], game_state: GameState) -> bool:
        new_y = (head[0] + direction[0]) % self.height
        new_x = (head[1] + direction[1]) % self.width
        return game_state.field[new_y][new_x] not in [1, 2]  # Not body or head

# # Пример использования:
# import time
# from game import visualize_game
# snake = Snake(width=20, height=20, n_apples=2, die_border=False)
# decision_tree = DecisionTree(
#     snake.get_game_state().size[0],
#     snake.get_game_state().size[1],
# )

# from pprint import pprint
# while not snake.game_over:
#     new_direction = decision_tree.make_decision(
#         snake.get_game_state()
#     )
#     snake.move(new_direction)
#     game_state = snake.get_game_state()

#     visualize_game(snake.get_game_state()).show()
#     time.sleep(1)
    
# print("Game Over!")