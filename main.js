const { app, BrowserWindow, globalShortcut } = require('electron');
const path = require('path');

function createWindow() {
    const win = new BrowserWindow({
        width: 1920,
        height: 1080,
        fullscreen: true,
        frame: false,
        kiosk: true, // Lock it down as a dedicated OS interface
        backgroundColor: '#060810',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    win.loadFile('cubix_os.html');

    // Emergency escape: Ctrl+Shift+Q to quit the environment
    globalShortcut.register('Control+Shift+Q', () => {
        app.quit();
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});
