const { app, BrowserWindow, globalShortcut, ipcMain, screen } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  mainWindow = new BrowserWindow({
    width: width,
    height: height,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    hasShadow: false,
    resizable: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // STEALTH MODE: Critical for hiding from screen sharing (Zoom/Teams)
  // On Windows, this sets WDA_EXCLUDEFROMCAPTURE
  mainWindow.setContentProtection(true);

  // Allow clicks to pass through the window by default
  // The frontend can toggle this when hovering over interactive elements
  mainWindow.setIgnoreMouseEvents(true, { forward: true });

  // Load the React app
  // In development, this would be localhost:3000
  // In production, it would be the build file
  const startUrl = process.env.ELECTRON_START_URL || `file://${path.join(__dirname, '../build/index.html')}`;
  mainWindow.loadURL(startUrl);

  mainWindow.on('closed', function () {
    mainWindow = null;
  });

  // Panic Mode: Global Hotkey to kill/hide the app
  globalShortcut.register('CommandOrControl+Shift+X', () => {
    console.log('PANIC MODE ACTIVATED');
    if (mainWindow) {
        // Option 1: Destroy immediately
        app.quit(); 
        
        // Option 2 (Alternative): Hide window
        // mainWindow.hide();
    }
  });

  // IPC: Toggle mouse events (click-through vs clickable)
  ipcMain.on('set-ignore-mouse-events', (event, ignore, options) => {
    const win = BrowserWindow.fromWebContents(event.sender);
    win.setIgnoreMouseEvents(ignore, options);
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('will-quit', () => {
  // Unregister all shortcuts
  globalShortcut.unregisterAll();
});
