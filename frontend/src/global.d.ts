export {}

declare global {
  interface Window {
    api: {
      openFolder: () => Promise<{ rootPath: string; tree: FileNode[] } | null>
      readFile: (filePath: string) => Promise<string>
      saveFile: (filePath: string, content: string) => Promise<boolean>
    }
  }

  interface FileNode {
    name: string
    path: string
    type: 'file' | 'dir'
    children?: FileNode[]
  }
}
