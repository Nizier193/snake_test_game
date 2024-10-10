import stat
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from game import Snake, visualize_game
from models import CreateGameModel, DirectionSnakeModel

import base64
from io import BytesIO

import time

app = FastAPI()
game = None

@app.get("/")
async def root():
    st = time.time()
    return JSONResponse(
        content={"message": "Welcome to the Snake Game Emulator!"}
    )

@app.post("/create_game")
async def create_game(game_params: CreateGameModel) -> JSONResponse:
    global game

    params = game_params

    game = Snake(
        width=params.width,
        height=params.height,
        n_apples=params.n_apples,
        die_border=params.die_border
    )
    state = game.get_game_state().to_dict()

    return JSONResponse(
        content = {
            "message": "Game created succesfully.",
            "game_state": state
        },
        status_code = 200
    )

@app.post("/delete_game")
async def delete():
    global game

    game = None
    return JSONResponse(
        content={
            "message": "Deleted Game",
        },
        status_code=200
    )

@app.post("/move")
async def move(direction: DirectionSnakeModel):
    global game

    if not game:
        return JSONResponse(
            content={
                "message": "Game is not created yet.",
            },
            status_code=400
        )

    game.move(direction.direction)
    state = game.get_game_state().to_dict()

    return JSONResponse(
        content = {
            "message": "Succesful movement",
            "action": direction.direction,
            "game_state": state
        },
        status_code = 200
    )

@app.get("/state")
async def get_state():
    global game

    if not game:
        return JSONResponse(
            content={
                "message": "Game is not created yet.",
            },
            status_code=400
        )

    state = game.get_game_state().to_dict()

    return JSONResponse(
        content={
            "message": "Succesfully retrieved game state.",
            "game_state": state
        },
        status_code=200
    )

@app.get("/image")
async def get_image(cell_size: int = 20):
    global game

    if not game:
        return JSONResponse(
            content={
                "message": "Game is not created yet.",
            },
            status_code=400
        )
    
    image = visualize_game(
        game.get_game_state(), 
        cell_size=cell_size
    )

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    image_str = base64.b64encode(
        buffer.getvalue()
    ).decode('utf-8')

    return JSONResponse(
        content={
            "message": "Succesfully retrieved b64 encoded image.",
            "image": image_str
        },
        status_code=200
    )
