-- schema.sql
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
