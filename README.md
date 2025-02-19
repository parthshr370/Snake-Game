# Snake-Game
Snake Game AI Assignment 1

# Snake-Game

## Overview

The **Skill-Based Snake Game** is an interactive web application that combines the classic snake game with an AI-driven twist. The game is developed using Flask for the backend, JavaScript and HTML/CSS for the frontend, and SQLite for data storage. Each player controls a snake associated with specific skills, and the AI agent adapts its behavior using Q-learning based on player-selected skills.

---

## Features

- Skill-based snake customization.
- Real-time game updates using Flask and JavaScript.
- AI-powered snake movement with Q-learning for dynamic gameplay.
- Persistent player data storage using SQLite.
- Interactive web interface with responsive canvas rendering.

---

## Project Structure

```
Snake-Game/
├── app.py                # Flask application server
├── game_logic.py         # Game logic and AI behavior
├── schema.sql            # Database schema definitions
├── static/
│   ├── script.js         # Frontend JavaScript for game rendering
│   └── styles.css        # CSS for styling the web interface
├── templates/
│   └── index.html        # HTML template for the main webpage
└── README.md             # Project documentation (this file)
```

---

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Snake-Game
   ```

2. **Install dependencies:**
   ```bash
   pip install Flask
   ```

3. **Initialize the database:**
   ```bash
   python app.py
   ```
   The database will be automatically initialized when the server starts.

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the game:**
   Open your web browser and go to `http://127.0.0.1:5000/`.

---

## How to Play

1. Enter your name and skills in the input field using the format:
   ```
   Name: skill1, skill2, skill3
   ```
   Example:
   ```
   Alice: HTML, Java, MySQL
   ```

2. Click the **Start Game** button.

3. Watch as the snake(s) representing your skills navigate the board, collecting tokens matching their domains.

4. The game runs continuously with AI agents adapting their strategies using Q-learning.

---

## Core Components

### 1. `app.py`
- **Routes:**
  - `/`: Serves the main game page.
  - `/start_game`: Starts a new game session, stores player data.
  - `/game_state`: Returns the current game state in JSON format.

- **Database:**
  - Uses `players.db` with tables `players` and `game_progress` defined in `schema.sql`.

- **Game Loop:**
  - Runs in a separate thread, continuously updating the game state every 200ms.

### 2. `game_logic.py`
- **SnakeAgent Class:**
  - Handles snake movement, Q-learning logic, and interaction with tokens.

- **GameEnvironment Class:**
  - Manages the entire game environment, including initializing snakes, generating tokens, and updating game state.

- **Q-Learning Algorithm:**
  - Reinforcement learning approach where snakes learn optimal paths based on rewards for collecting matching skill tokens.

### 3. Frontend (`static/script.js`, `templates/index.html`, `static/styles.css`)
- **HTML:** Provides the game layout and input forms.
- **CSS:** Styles the game interface.
- **JavaScript:** Fetches game state from the backend and renders the game board and snake movements on an HTML5 canvas.

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    skills TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS game_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    domain TEXT NOT NULL,
    tokens_collected INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(id)
);
```

---

## AI Logic (Q-Learning)

- **State Representation:**
  - Snake's head position and nearest token coordinates.

- **Actions:**
  - Movement directions: `UP`, `DOWN`, `LEFT`, `RIGHT`.

- **Rewards:**
  - +10 for collecting a matching skill token.
  - -2 for collecting a non-matching token.

- **Q-Value Updates:**
  - Updates based on the Bellman equation to reinforce optimal actions.

---

## Customization

- **Add New Skills:**
  - Update `DOMAIN_COLORS` in `game_logic.py` with new skill and color mappings.

- **Adjust Game Speed:**
  - Modify the `time.sleep(0.2)` value in `run_game_loop()` function in `app.py`.

- **Board Dimensions:**
  - Update `BOARD_WIDTH`, `BOARD_HEIGHT`, and `CELL_SIZE` in `game_logic.py`.

---

## Future Improvements

- Implement multiplayer support with real-time interaction.
- Add a scoring leaderboard based on collected tokens.
- Improve AI behavior using advanced reinforcement learning algorithms.
- Enhance UI with animations and responsive design for mobile compatibility.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- Flask documentation
- Reinforcement learning tutorials
- Classic Snake game implementations

