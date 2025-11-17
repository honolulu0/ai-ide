<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <button @click="chooseFolder">\u6253\u5f00\u6587\u4ef6\u5939</button>
        <div v-if="workspaceRoot" class="root-path" :title="workspaceRoot">
          {{ workspaceRoot }}
        </div>
      </div>

      <div class="file-tree" v-if="fileTree.length">
        <ul class="tree-root">
          <FileNodeItem
            v-for="node in fileTree"
            :key="node.path"
            :node="node"
            :current-file="currentFilePath"
            @open-file="openFile"
          />
        </ul>
      </div>

      <button @click="applyInlineEdit" :disabled="!selection">
        AI \u91cd\u5199\u9009\u4e2d\u4ee3\u7801
      </button>
    </aside>

    <main class="editor-wrapper">
      <CodeEditor
        v-model="code"
        :language="language"
        @selectionChange="selection = $event"
      />
    </main>

    <section class="chat-wrapper">
      <ChatPanel
        :current-file-content="code"
        :current-file-path="currentFilePath"
        :selection="selection"
      />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import CodeEditor from './components/CodeEditor.vue'
import ChatPanel from './components/ChatPanel.vue'
import FileNodeItem from './components/FileNodeItem.vue'

const workspaceRoot = ref<string | null>(null)
const fileTree = ref<FileNode[]>([])
const currentFilePath = ref<string | null>(null)
const code = ref<string>('')
const selection = ref<string>('')
const language = ref<string>('python')

async function chooseFolder() {
  const res = await window.api.openFolder()
  if (!res) return
  workspaceRoot.value = res.rootPath
  fileTree.value = res.tree
  currentFilePath.value = null
  code.value = ''
}

async function openFile(path: string) {
  const content = await window.api.readFile(path)
  currentFilePath.value = path
  code.value = content
  language.value = guessLanguageByExt(path)
}

function guessLanguageByExt(path: string): string {
  const ext = path.split('.').pop()?.toLowerCase()
  if (ext === 'py') return 'python'
  if (ext === 'js' || ext === 'cjs' || ext === 'mjs') return 'javascript'
  if (ext === 'ts') return 'typescript'
  if (ext === 'vue') return 'vue'
  if (ext === 'json') return 'json'
  if (ext === 'html') return 'html'
  if (ext === 'css' || ext === 'scss') return 'css'
  return 'plaintext'
}

async function applyInlineEdit() {
  if (!selection.value) return
  const instruction = prompt('\u8bf7\u8f93\u5165\u91cd\u6784\u6307\u4ee4\uff0c\u4f8b\u5982\uff1a\u6539\u6210 async/await \u98ce\u683c') || ' \u4f18\u5316\u8fd9\u6bb5\u4ee3\u7801\u7684\u53ef\u8bfb\u6027'
  const payload = {
    instruction,
    original_code: selection.value,
    file_path: currentFilePath.value,
    language: language.value
  }
  try {
    const res = await axios.post('/api/inline_edit', payload)
    const edited = res.data.edited_code as string
    code.value = code.value.replace(selection.value, edited)
    selection.value = ''
    if (currentFilePath.value) {
      await window.api.saveFile(currentFilePath.value, code.value)
    }
  } catch (e) {
    alert('AI \u91cd\u5199\u5931\u8d25\uff0c\u8bf7\u68c0\u67e5\u540e\u7aef\u6216\u6a21\u578b\u914d\u7f6e')
  }
}
</script>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 260px 1fr 320px;
  height: 100vh;
  overflow: hidden;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Additional styling for file tree, sidebar, etc., can be added later */
</style>
