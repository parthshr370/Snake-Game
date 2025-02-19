# game_logic.py

import random

# Example board dimensions
BOARD_WIDTH = 60
BOARD_HEIGHT = 40
CELL_SIZE = 10  # how large each cell is in actual pixels

# Define color mapping for each domain for easy representation
DOMAIN_COLORS = {
    "HTML": "blue",
    "CSS": "cyan",
    "JavaScript": "orange",
    "C++": "purple",
    "Java": "green",
    ".NET": "teal",
    "Full Stack": "magenta",
    "ML/DL": "red",
    "Python": "brown",
    "SQL": "navy",
    "NoSQL": "darkblue",
    "MySQL": "gray",
    "Oracle": "darkred",
    "AWS": "gold",
    "Azure": "silver"
}

TOKEN_DOMAINS = list(DOMAIN_COLORS.keys())

class SnakeAgent:
    def __init__(self, domain):
        self.domain = domain
        self.color = DOMAIN_COLORS.get(domain, "black")
        self.body = [{"x": random.randint(0, BOARD_WIDTH-1) * CELL_SIZE,
                      "y": random.randint(0, BOARD_HEIGHT-1) * CELL_SIZE}]
        self.direction = "RIGHT"
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount = 0.9
        self.epsilon = 0.1

    def get_state(self, tokens):
        snake_x = self.body[0]["x"]
        snake_y = self.body[0]["y"]
        relevant_tokens = [t for t in tokens if t["domain"] == self.domain]
        if not relevant_tokens:
            relevant_tokens = tokens
        if not relevant_tokens:
            return (snake_x, snake_y, -1, -1)
        token_x = relevant_tokens[0]["x"]
        token_y = relevant_tokens[0]["y"]
        return (snake_x, snake_y, token_x, token_y)

    def get_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        if state not in self.q_table:
            self.q_table[state] = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        return max(self.q_table[state], key=self.q_table[state].get)

    def update_q(self, old_state, action, reward, new_state):
        if old_state not in self.q_table:
            self.q_table[old_state] = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        if new_state not in self.q_table:
            self.q_table[new_state] = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        old_q = self.q_table[old_state][action]
        next_max = max(self.q_table[new_state].values())
        new_q = old_q + self.learning_rate * (reward + self.discount * next_max - old_q)
        self.q_table[old_state][action] = new_q

    # Example where each move is increased to 20 pixels instead of 10
    def move(self, action, grow=False):
        head_x = self.body[0]["x"]
        head_y = self.body[0]["y"]

        move_increment = 100  # Increased from 10 for faster movement

        if action == "UP":
            head_y -= move_increment
        elif action == "DOWN":
            head_y += move_increment
        elif action == "LEFT":
            head_x -= move_increment
        elif action == "RIGHT":
            head_x += move_increment

        # Wrap around logic for the board edges
        head_x = head_x % (BOARD_WIDTH * CELL_SIZE)
        head_y = head_y % (BOARD_HEIGHT * CELL_SIZE)

        self.body.insert(0, {"x": head_x, "y": head_y})

        if not grow:
            self.body.pop()

class GameEnvironment:
    def __init__(self):
        self.snakes = []
        self.tokens = []
        self.width = BOARD_WIDTH * CELL_SIZE
        self.height = BOARD_HEIGHT * CELL_SIZE

    def init_game(self, player_id, player_name, skills):
        self.snakes = []
        self.tokens = self.generate_tokens()
        for skill in skills:
            self.snakes.append(SnakeAgent(skill))

    def generate_tokens(self, num_tokens=10):
        tokens = []
        for _ in range(num_tokens):
            domain = random.choice(TOKEN_DOMAINS)
            tokens.append({
                "x": random.randint(0, BOARD_WIDTH-1) * CELL_SIZE,
                "y": random.randint(0, BOARD_HEIGHT-1) * CELL_SIZE,
                "domain": domain,
                "color": DOMAIN_COLORS[domain]
            })
        return tokens

    def update(self):
        for snake in self.snakes:
            old_state = snake.get_state(self.tokens)
            action = snake.get_action(old_state)
            grow = False
            reward = 0
            head = {"x": snake.body[0]["x"], "y": snake.body[0]["y"]}
            if action == "UP":
                head["y"] -= CELL_SIZE
            elif action == "DOWN":
                head["y"] += CELL_SIZE
            elif action == "LEFT":
                head["x"] -= CELL_SIZE
            elif action == "RIGHT":
                head["x"] += CELL_SIZE

            head["x"] = head["x"] % (BOARD_WIDTH * CELL_SIZE)
            head["y"] = head["y"] % (BOARD_HEIGHT * CELL_SIZE)

            for token in self.tokens:
                if token["x"] == head["x"] and token["y"] == head["y"]:
                    if token["domain"] == snake.domain:
                        grow = True
                        reward = 10
                        self.tokens.remove(token)
                        self.tokens.append(self.generate_tokens(1)[0])
                        break
                    else:
                        reward = -2
            snake.move(action, grow)
            new_state = snake.get_state(self.tokens)
            snake.update_q(old_state, action, reward, new_state)

    def get_state(self):
        snakes_info = []
        for snake in self.snakes:
            snakes_info.append({
                "domain": snake.domain,
                "color": snake.color,
                "body": snake.body
            })
        return {"snakes": snakes_info, "tokens": self.tokens}
