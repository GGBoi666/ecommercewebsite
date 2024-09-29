// poker.js

let playerHand = [];
let communityCards = [];
let pot = 0.0;
let currentBet = 0.0;
let balance = 1.0;

document.getElementById("place-bet").addEventListener("click", function() {
    if (balance >= currentBet) {
        balance -= currentBet;
        pot += currentBet;
        startPokerGame();
    }
});

function startPokerGame() {
    fetch('/poker/start', { method: 'POST', body: JSON.stringify({ bet: currentBet }) })
        .then(response => response.json())
        .then(data => {
            playerHand = data.player_hand;
            communityCards = data.community_cards;
            updatePokerDisplay();
        });
}

function updatePokerDisplay() {
    document.getElementById("player-cards").textContent = playerHand.join(", ");
    document.getElementById("community-cards-display").textContent = communityCards.join(", ");
}

document.getElementById("fold").addEventListener("click", function() {
    fetch('/poker/fold', { method: 'POST' })
        .then(() => {
            resetPokerGame();
        });
});

function resetPokerGame() {
    playerHand = [];
    communityCards = [];
    pot = 0.0;
    updatePokerDisplay();
}
