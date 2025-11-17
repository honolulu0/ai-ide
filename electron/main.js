const { app, BrowserWindow, dialog, ipcMain } = require('electron')
const path = require('path')
const fs = require('fs')
const { spawn } = require('child_process')

let mainWindow = null
let backendProcess = null

// Determine whether we are in development mode based on how Electron is packaged
const isDev = !app.isPackaged

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  })
  if (isDev) {
    // During development load the Vite dev server
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    // In production load the built front end
    mainWindow.loadFile(path.join(__dirname, '../frontend/dist/index.html'))
  }
}

function startPythonBackend() {
  // Optionally start the backend automatically.  Commented out by default
  backendProcess = spawn(
    'python',
    ['-m', 'uvicorn', 'ai-ide.backend.main:app', '--port', '8000'],
    {
      cwd: path.join(__dirname, '..'),
      shell: true,
    },
  )
  backendProcess.stdout.on('data', (data) => {
    console.log('[backend]', data.toString())
  })
  backendProcess.stderr.on('data', (data) => {
    console.error('[backend error]', data.toString())
  })
  backendProcess.on('close', (code) => {
    console.log('Backend exited with code', code)
  })
}

app.whenReady().then(() => {
  // Optionally start the backend here
  // startPythonBackend()
  createWindow()
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    if (backendProcess) {
      backendProcess.kill()
    }
    app.quit()
  }
})

// Helper to recursively read a directory and return a tree structure
function readDirectoryRecursive(dirPath) {
  const entries = fs.readdirSync(dirPath, { withFileTypes: true })
  return entries.map((entry) => {
    const fullPath = path.join(dirPath, entry.name)
    if (entry.isDirectory()) {
      return {
        name: entry.name,
        path: fullPath,
        type: 'dir',
        children: readDirectoryRecursive(fullPath),
      }
    } else {
      return {
        name: entry.name,
        path: fullPath,
        type: 'file',
      }
    }
  })
}

ipcMain.handle('dialog:openFolder', async () => {
  const result = await dialog.showOpenDialog({ properties: ['openDirectory'] })
  if (result.canceled || !result.filePaths.length) return null
  const rootPath = result.filePaths[0]
  const tree = readDirectoryRecursive(rootPath)
  return { rootPath, tree }
})

ipcMain.handle('fs:readFile', async (event, filePath) => {
  return fs.promises.readFile(filePath, 'utf-8')
})

ipcMain.handle('fs:saveFile', async (event, filePath, content) => {
  await fs.promises.writeFile(filePath, content, 'utf-8')
  return true
})
