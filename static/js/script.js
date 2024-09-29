// Handle BTC Clicker Game
document.getElementById("click-btc-button").addEventListener("click", function () {
    fetch("/gambling/click_btc", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("btc-earned").textContent = "₿" + data.new_balance + " BTC";
        });
});

// Slot Machine Game
document.getElementById("play-slot-button").addEventListener("click", function () {
    fetch("/gambling/play_slot", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("slot1").textContent = data.result[0];
            document.getElementById("slot2").textContent = data.result[1];
            document.getElementById("slot3").textContent = data.result[2];
            document.getElementById("slot-result").textContent = data.success
                ? "You won " + data.winnings + " BTC!"
                : "Try Again!";
        });
});

// Dice Game
document.getElementById("roll-dice-button").addEventListener("click", function () {
    fetch("/gambling/roll_dice", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            document.getElementById("dice-animation").textContent = "🎲" + data.result;
            document.getElementById("dice-result").textContent = data.success
                ? "You won " + data.winnings + " BTC!"
                : "You lost!";
        });
});
