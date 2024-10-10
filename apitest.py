from ast import Dict
from typing import Any, Optional, Dict, Union
import httpx
from pprint import pprint
import time
import json

from io import BytesIO
from PIL import Image

from game import visualize_game
from main import move
from models import GameState

from dtree import DecisionTree

baseurl = "http://localhost:8000/"

# Create a single client instance
client = httpx.Client(base_url=baseurl, headers={'Content-Type': 'application/json'})

def get_req(route: str = "", params: Optional[Dict] = None):
    response = client.get(route, params=params)
    return response.json()

def post_req(route: str, payload: Dict):
    response = client.post(route, json=payload)
    return response.json()

"""
GET:
/state -> Dict
/image -> b64encoded Image

POST:
/create_game (
    game_params: Dict = {width: int, height: int, n_apples: int, die_border: bool}
) -> Dict

/move (direction: Tuple[int, int]) -> Dict

"""

import base64

start_gamestate = post_req(
    "create_game",
    payload={
        "width": 5,
        "height": 5,
        "n_apples": 1,
        "die_border": False
    }
).get("game_state")

w, h = start_gamestate.get("size")
decision_tree = DecisionTree(w, h)

gameover = start_gamestate.get("game_over")
while not gameover:
    state_data = get_req("state").get("game_state")
    state: GameState = GameState(
        size=tuple(state_data.get("size")),
        field=state_data.get("field"),
        snake=state_data.get("snake"),
        score=state_data.get("score"),
        game_over=state_data.get("game_over")
    )
    visualize_game(state).show()

    movement = decision_tree.make_decision(state)

    response = client.post("move", json={"direction": movement})

    print("One turn ended succesfully.", state.game_over)
    gameover = state.game_over

    time.sleep(0.5)

client.close()
