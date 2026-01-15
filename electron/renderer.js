import { auth, db } from './firebase_config.js';
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    onAuthStateChanged
} from "firebase/auth";
import {
    doc,
    setDoc,
    addDoc,
    collection
} from "firebase/firestore";

const { ipcRenderer } = require('electron'); // Still needed for IPC, might need mix of ESM/CommonJS handling or preload usage

// --- UI State Management ---
let isGhostMode = false;
let isLoginMode = true; // Toggle between Login and Signup

// --- Elements ---
const authOverlay = document.getElementById('auth-overlay');
const emailInput = document.getElementById('email-input');
const passwordInput = document.getElementById('password-input');
const authBtn = document.getElementById('auth-btn');
const toggleAuthModeBtn = document.getElementById('toggle-auth-mode');
const authTitle = document.getElementById('auth-title');
const authError = document.getElementById('auth-error');

const appContent = [document.getElementById('transcript-card'), document.getElementById('answer-card')];

// --- Auth Logic ---
authBtn.addEventListener('click', async () => {
    const email = emailInput.value;
    const password = passwordInput.value;
    authError.innerText = "";

    try {
        if (isLoginMode) {
            await signInWithEmailAndPassword(auth, email, password);
        } else {
            // Signup flow
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            // Create User Document with Default Plan
            await setDoc(doc(db, "users", user.uid), {
                email: email,
                planType: "free", // Default plan
                createdAt: new Date()
            });
        }
    } catch (error) {
        authError.innerText = error.message;
    }
});

toggleAuthModeBtn.addEventListener('click', () => {
    isLoginMode = !isLoginMode;
    authTitle.innerText = isLoginMode ? "Crib AI Login" : "Create Account";
    authBtn.innerText = isLoginMode ? "Login" : "Sign Up";
    toggleAuthModeBtn.innerText = isLoginMode ? "Need an account? Sign Up" : "Have an account? Login";
});

// --- Auth State Listener ---
onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in
        authOverlay.style.display = 'none';
        appContent.forEach(el => el.style.display = 'block');
        // Initial Greeting
        document.getElementById('transcript-box').innerHTML = `<i>Welcome, ${user.email}</i><br>Listening...`;

        // Retrieve Token for Backend
        user.getIdToken().then(token => {
            // TODO: Send this token to backend via IPC or HTTP header for validation
            console.log("Auth Token:", token);
        });

    } else {
        // User is signed out
        authOverlay.style.display = 'block';
        appContent.forEach(el => el.style.display = 'none');
    }
});

// --- Feedback Logic ---
const feedbackBtn = document.getElementById('feedback-btn');
feedbackBtn.addEventListener('click', async () => {
    const text = document.getElementById('feedback-text').value;
    if (!text || !auth.currentUser) return;

    try {
        await addDoc(collection(db, "feedback"), {
            uid: auth.currentUser.uid,
            email: auth.currentUser.email,
            message: text,
            timestamp: new Date()
        });
        alert("Feedback sent! Thank you.");
        document.getElementById('feedback-modal').style.display = 'none';
        document.getElementById('feedback-text').value = "";
    } catch (e) {
        console.error("Error sending feedback: ", e);
    }
});

// --- Ghost Mode & UI Utils ---
window.toggleGhostMode = function () {
    isGhostMode = !isGhostMode;
    const container = document.getElementById('app-container');
    const toggleBtn = document.getElementById('ghost-toggle');

    if (isGhostMode) {
        container.classList.add('ghost-mode-active');
        toggleBtn.style.color = '#ff0055';
    } else {
        container.classList.remove('ghost-mode-active');
        toggleBtn.style.color = 'white';
    }
}

// Mouse Event Pass-through (IPC Wrapper)
// Note: Since this is a module, 'window.electron' from preload is available globally
const interactiveElements = document.querySelectorAll('.interactive');
interactiveElements.forEach(el => {
    el.addEventListener('mouseenter', () => {
        if (window.electron) window.electron.setIgnoreMouseEvents(false);
    });
    el.addEventListener('mouseleave', () => {
        if (window.electron) window.electron.setIgnoreMouseEvents(true, { forward: true });
    });
});
