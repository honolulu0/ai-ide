<template>
  <div class="chat-panel">
    <div class="chat-messages">
      <div
        v-for="(m, idx) in messages"
        :key="idx"
        class="chat-msg"
        :class="m.role"
      >
        <div class="role">{{ m.role === 'user' ? '我' : 'AI' }}</div>
        <div class="content">{{ m.content }}</div>
      </div>
    </div>
    <div class="chat-input">
      <textarea
        v-model="input"
        placeholder="问 AI：比如“帮我重构当前函数”、“这段报错怎么解决？”"
      />
      <button @click="handleSend" :disabled="loading">
        {{ loading ? '思考中…' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'

interface Msg {
  role: 'user' | 'assistant'
  content: string
}

const props = defineProps<{
  currentFileContent: string
  currentFilePath?: string
  selection?: string
}>()

const messages = ref<Msg[]>([])
const input = ref('')
const loading = ref(false)

async function handleSend() {
  if (!input.value.trim()) return
  const userMsg: Msg = { role: 'user', content: input.value.trim() }
  messages.value.push(userMsg)
  const payload = {
    messages: messages.value.map((m) => ({ role: m.role, content: m.content })),
    current_file_content: props.currentFileContent,
    current_file_path: props.currentFilePath,
    selection: props.selection,
  }
  input.value = ''
  loading.value = true
  try {
    const res = await axios.post('/api/chat', payload)
    const reply: Msg = { role: 'assistant', content: res.data.reply }
    messages.value.push(reply)
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '请求失败，请检查后端或网络。',
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-left: 1px solid #eee;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.chat-msg {
  margin-bottom: 8px;
}

.chat-msg .role {
  font-size: 12px;
  color: #888;
}

.chat-msg .content {
  white-space: pre-wrap;
}

.chat-msg.user .content {
  background: #f3f3f3;
}

.chat-msg.assistant .content {
  background: #e8f5ff;
}

.chat-input {
  border-top: 1px solid #eee;
  padding: 8px;
  display: flex;
  gap: 8px;
}

.chat-input textarea {
  flex: 1;
  min-height: 60px;
}
</style>
