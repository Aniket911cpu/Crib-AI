const { ipcRenderer } = require('electron');

let isGhostMode = false;

// Toggle Ghost Mode
function toggleGhostMode() {
    isGhostMode = !isGhostMode;
    const container = document.getElementById('app-container');
    const toggleBtn = document.getElementById('ghost-toggle');

    if (isGhostMode) {
        container.classList.add('ghost-mode-active');
        toggleBtn.style.color = '#ff0055'; // Red for active
        // Also tell Main process to perhaps reduce clickability further if needed
    } else {
        container.classList.remove('ghost-mode-active');
        toggleBtn.style.color = 'white';
    }
}

// Mouse Event Pass-through Logic
// If mouse enters a '.interactive' element, we enable mouse clicks (ignoreMouseEvents = false)
// Otherwise, we let clicks pass through (ignoreMouseEvents = true)

const interactiveElements = document.querySelectorAll('.interactive');

interactiveElements.forEach(el => {
    el.addEventListener('mouseenter', () => {
        window.electron.setIgnoreMouseEvents(false);
    });
    el.addEventListener('mouseleave', () => {
        window.electron.setIgnoreMouseEvents(true, { forward: true });
    });
});

// Mock Data Updates (Demo)
setInterval(() => {
    // Simulate WPM fluctuation
    const wpm = Math.floor(Math.random() * (160 - 100) + 100);
    document.getElementById('wpm-value').innerText = wpm;

    const indicator = document.getElementById('wpm-indicator');
    if (wpm > 150) {
        indicator.style.backgroundColor = 'red'; // Too fast!
    } else {
        indicator.style.backgroundColor = '#00ff00'; // Good
    }
}, 2000);
