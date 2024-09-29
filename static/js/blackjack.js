// Fetch and display the balance
function fetchBalance() {
    fetch('/get_balance')
        .then(response => response.json())
        .then(data => {
            document.getElementById('balance').textContent = data.balance.toFixed(4);
        });
}

// Update balance after winning or losing
function updateBalance(newBalance) {
    fetch('/update_balance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ balance: newBalance })
    }).then(response => response.json())
      .then(data => {
          document.getElementById('balance').textContent = data.new_balance.toFixed(4);
      });
}

// Example game logic to hit or stand
document.getElementById('place-bet').addEventListener('click', function () {
    // Deduct bet, update balance
    let balance = parseFloat(document.getElementById('balance').textContent);
    let betAmount = 0.01; // Example bet
    let newBalance = balance - betAmount;
    updateBalance(newBalance);
    document.getElementById('status-message').textContent = 'Bet placed, good luck!';
});

window.onload = fetchBalance;
