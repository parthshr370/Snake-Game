const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
let gameInterval = null;

document.getElementById("startGameBtn").addEventListener("click", async () => {
    const input = document.getElementById("playerInput").value.trim();
    if (!input) return alert("Please enter your name and skills!");

    try {
        const res = await fetch("/start_game", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ playerInput: input })
        });

        if (!res.ok) throw new Error("Failed to start game");

        if (gameInterval) clearInterval(gameInterval);
        gameInterval = setInterval(fetchGameState, 200);
    } catch (err) {
        console.error(err.message);
    }
});

async function fetchGameState() {
    try {
        const res = await fetch("/game_state");
        if (!res.ok) return;

        const gameState = await res.json();
        drawGame(gameState);
    } catch (error) {
        console.error("Error fetching game state:", error.message);
    }
}

function drawGame(gameState) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    gameState.tokens.forEach(token => {
        ctx.fillStyle = token.color;
        ctx.fillRect(token.x, token.y, 10, 10);
    });
    gameState.snakes.forEach(snake => {
        ctx.fillStyle = snake.color;
        snake.body.forEach(segment => {
            ctx.fillRect(segment.x, segment.y, 10, 10);
        });
    });
}
