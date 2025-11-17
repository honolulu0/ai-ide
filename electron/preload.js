const { contextBridge, ipcRenderer } = require('electron')

// Expose a limited API to the renderer process.  This allows the Vue
// front end to interact with the file system without enabling full
// Node integration in the browser context.  The functions return
// promises since IPC handlers are asynchronous.
contextBridge.exposeInMainWorld('api', {
  openFolder: () => ipcRenderer.invoke('dialog:openFolder'),
  readFile: (filePath) => ipcRenderer.invoke('fs:readFile', filePath),
  saveFile: (filePath, content) => ipcRenderer.invoke('fs:saveFile', filePath, content),
})
