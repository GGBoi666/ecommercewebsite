// Animate balance update (increase or decrease smoothly)
function animateBalance(newBalance) {
    const btcClickResultElement = document.getElementById("btc-click-result"); // Balance under click BTC
    const stickyBalanceElement = document.getElementById("sticky-btc-balance"); // Balance in sticky bar

    const currentClickBalance = parseFloat(btcClickResultElement.textContent.replace('₿', '').replace(' BTC', ''));
    const currentStickyBalance = parseFloat(stickyBalanceElement.textContent.replace('₿', '').replace(' BTC', ''));
    const targetBalance = parseFloat(newBalance);

    if (!btcClickResultElement || !stickyBalanceElement) {
        console.error("Balance element not found");
        return;
    }

    let currentStep = 0;
    const animationDuration = 1000; // 1 second for animation
    const stepTime = 50; // Balance update step in ms
    const totalSteps = Math.round(animationDuration / stepTime);
    const increment = (targetBalance - currentClickBalance) / totalSteps;

    const updateBalance = () => {
        if (currentStep <= totalSteps) {
            const newStepBalance = (currentClickBalance + (increment * currentStep)).toFixed(8);
            btcClickResultElement.textContent = `₿${newStepBalance} BTC`;
            stickyBalanceElement.textContent = `₿${newStepBalance} BTC`; // Update sticky bar balance as well
            currentStep++;
            setTimeout(updateBalance, stepTime);
        } else {
            btcClickResultElement.textContent = `₿${targetBalance.toFixed(8)} BTC`;
            stickyBalanceElement.textContent = `₿${targetBalance.toFixed(8)} BTC`; // Final update for sticky bar
        }
    };

    updateBalance();
}

// General function to handle game results and button reset with animation
function handleGameResult(buttonId, resultId, resultText, success) {
    const resultElement = document.getElementById(resultId);
    const buttonElement = document.getElementById(buttonId);

    resultElement.textContent = resultText;
    buttonElement.disabled = true;

    if (success) {
        resultElement.style.color = '#39d353'; // Success color (green)
        resultElement.classList.add('winning-animation'); // Add animation class
    } else {
        resultElement.style.color = '#ff3333'; // Failure color (red)
    }

    setTimeout(() => {
        buttonElement.disabled = false;
        resultElement.textContent = ""; // Clear result after 2 seconds
        resultElement.classList.remove('winning-animation'); // Remove animation class
    }, 2000);
}

// BTC Clicker Game
document.getElementById("click-btc-button").addEventListener("click", function() {
    fetch('/gambling/click_btc', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        animateBalance(data.new_balance); // Use animated balance update
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Clicker Upgrade
document.getElementById("upgrade-clicker-button").addEventListener("click", function() {
    fetch('/gambling/upgrade_clicker', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            animateBalance(data.new_balance); // Use animated balance update
            document.getElementById("clicker-level").textContent = data.new_level;
        } else {
            document.getElementById("upgrade-result").textContent = data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Dice Game
document.getElementById("roll-dice-button").addEventListener("click", function() {
    const betAmount = document.getElementById('bet-amount').value || 0.001; 
    fetch('/gambling/roll_dice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bet_amount: betAmount })
    })
    .then(response => response.json())
    .then(data => {
        const resultText = `Rolled: ${data.result}, ${data.success ? `You Won ₿${data.winnings}` : 'You Lost!'}`;
        handleGameResult("roll-dice-button", "dice-result", resultText, data.success);
        if (data.success) {
            animateBalance(data.new_balance); // Update balance if successful
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Slot Machine Game
document.getElementById("play-slot-button").addEventListener("click", function() {
    fetch('/gambling/play_slot', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        document.getElementById("slot1").textContent = data.result[0];
        document.getElementById("slot2").textContent = data.result[1];
        document.getElementById("slot3").textContent = data.result[2];
        const resultText = data.success ? `You Won: ₿${data.winnings}` : 'Try Again!';
        handleGameResult("play-slot-button", "slot-result", resultText, data.success);
        if (data.success) {
            animateBalance(data.new_balance); // Update balance if successful
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Coin Flip Game
document.getElementById("flip-coin-button").addEventListener("click", function() {
    const choice = document.getElementById("coin-flip-choice").value;
    const betAmount = document.getElementById('coin-bet-amount').value || 0.001; 
    fetch('/gambling/coin_flip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice, bet_amount: betAmount })
    })
    .then(response => response.json())
    .then(data => {
        const resultText = data.success ? `You Won ₿${data.winnings}!` : 'You Lost!';
        handleGameResult("flip-coin-button", "coin-flip-result", resultText, data.success);
        if (data.success) {
            animateBalance(data.new_balance); // Update balance if successful
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Roulette Game
document.getElementById("play-roulette-button").addEventListener("click", function() {
    const choice = document.getElementById("roulette-choice").value;
    const betAmount = document.getElementById('roulette-bet-amount').value || 0.001; 
    fetch('/gambling/roulette', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choice, bet_amount: betAmount })
    })
    .then(response => response.json())
    .then(data => {
        const resultText = data.success ? `You Won ₿${data.winnings}!` : 'You Lost!';
        handleGameResult("play-roulette-button", "roulette-result", resultText, data.success);
        if (data.success) {
            animateBalance(data.new_balance); // Update balance if successful
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
