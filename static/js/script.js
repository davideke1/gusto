// Countdown to March 13, 2024
const targetDate = new Date('March 13, 2024 00:00:00').getTime();

function updateCountdown() {
    const currentDate = new Date().getTime();
    const timeDifference = targetDate - currentDate;

    // Calculate days, hours, minutes, and seconds
    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

    // Update clock-like display
    document.getElementById('timer').innerHTML = `
        <div class="clock">
            <div class="time" id="days">${days}</div>
            <div class="label">Days</div>
        </div>
        <div class="clock">
            <div class="time" id="hours">${hours}</div>
            <div class="label">Hours</div>
        </div>
        <div class="clock">
            <div class="time" id="minutes">${minutes}</div>
            <div class="label">Minutes</div>
        </div>
        <div class="clock">
            <div class="time" id="seconds">${seconds}</div>
            <div class="label">Seconds</div>
        </div>
    `;
}

// Update countdown every second
setInterval(updateCountdown, 1000);

// Initial countdown update
updateCountdown();
