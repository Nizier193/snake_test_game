# Эмулятор API игры Змейка

Это API эмулятора игры Змейка на основе FastAPI. Он позволяет создавать, управлять и визуализировать игру Змейка через различные конечные точки.

## Конечные точки

### 1. Корневая конечная точка

- **URL:** `/`
- **Метод:** GET
- **Описание:** Приветственное сообщение для эмулятора игры Змейка.
- **Вывод:**
  ```json
  {
    "message": "Добро пожаловать в эмулятор игры Змейка!"
  }
  ```

### 2. Создать игру

- **URL:** `/create_game`
- **Метод:** POST
- **Описание:** Создает новую игру Змейка с указанными параметрами.
- **Входные данные:**
  ```json
  {
    "width": int,
    "height": int,
    "n_apples": int,
    "die_border": bool
  }
  ```
- **Вывод:**
  ```json
  {
    "message": "Игра успешно создана.",
    "game_state": {
      // Подробности состояния игры
    }
  }
  ```

### 3. Удалить игру

- **URL:** `/delete_game`
- **Метод:** POST
- **Описание:** Удаляет текущую игру.
- **Вывод:**
  ```json
  {
    "message": "Игра удалена"
  }
  ```

### 4. Двигать Змейку

- **URL:** `/move`
- **Метод:** POST
- **Описание:** Двигает змейку в указанном направлении.
- **Входные данные:**
  ```json
  {
    "direction": string
  }
  ```
- **Вывод:**
  ```json
  {
    "message": "Движение успешно",
    "action": string,
    "game_state": {
      // Обновленные детали состояния игры
    }
  }
  ```

### 5. Получить состояние игры

- **URL:** `/state`
- **Метод:** GET
- **Описание:** Получает текущее состояние игры.
- **Вывод:**
  ```json
  {
    "message": "Состояние игры успешно получено.",
    "game_state": {
      // Текущие детали состояния игры
    }
  }
  ```

### 6. Получить изображение игры

- **URL:** `/image`
- **Метод:** GET
- **Описание:** Генерирует и возвращает изображение текущего состояния игры в формате base64.
- **Параметры запроса:**
  - `cell_size`: int (по умолчанию: 20)
- **Вывод:**
  ```json
  {
    "message": "Изображение в формате b64 успешно получено.",
    "image": "base64_encoded_string"
  }
  ```

## Обработка ошибок

Большинство конечных точек вернут код состояния 400 с сообщением об ошибке, если игра еще не создана:

## Example

Here's a Python example demonstrating how to use the Snake Game Emulator API:

```python
import requests
import json
import base64
from PIL import Image
import io

BASE_URL = "http://localhost:8000"

def create_game():
    response = requests.post(f"{BASE_URL}/create_game", json={
        "width": 10,
        "height": 10,
        "n_apples": 1,
        "die_border": True
    })
    return response.json()

def move_snake(direction):
    response = requests.post(f"{BASE_URL}/move", json={"direction": direction})
    return response.json()

def get_game_state():
    response = requests.get(f"{BASE_URL}/state")
    return response.json()

def get_game_image():
    response = requests.get(f"{BASE_URL}/image")
    image_data = base64.b64decode(response.json()["image"])
    image = Image.open(io.BytesIO(image_data))
    return image

# Create a new game
print(json.dumps(create_game(), indent=2))

# Play the game
for direction in ["right", "down", "left", "up"]:
    print(f"\nMoving {direction}:")
    print(json.dumps(move_snake(direction), indent=2))

# Get the final game state
print("\nFinal game state:")
print(json.dumps(get_game_state(), indent=2))

# Display the game image
image = get_game_image()
image.show()
```
