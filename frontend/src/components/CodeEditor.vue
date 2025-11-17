<template>
  <div class="editor-container" ref="editorEl"></div>
</template>

<script setup lang="ts">
import * as monaco from 'monaco-editor'
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps<{
  modelValue: string
  language?: string
}>()

const emits = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'selectionChange', code: string): void
}>()

const editorEl = ref<HTMLElement | null>(null)
let editor: monaco.editor.IStandaloneCodeEditor | null = null

onMounted(() => {
  if (!editorEl.value) return

  editor = monaco.editor.create(editorEl.value, {
    value: props.modelValue,
    language: props.language || 'javascript',
    automaticLayout: true,
    minimap: { enabled: true },
    fontSize: 14,
  })

  editor.onDidChangeModelContent(() => {
    emits('update:modelValue', editor!.getValue())
  })

  editor.onDidChangeCursorSelection(() => {
    const model = editor!.getModel()
    const selection = editor!.getSelection()
    if (!model || !selection) return
    const selectedText = model.getValueInRange(selection)
    emits('selectionChange', selectedText)
  })
})

watch(
  () => props.modelValue,
  (val) => {
    if (editor && val !== editor.getValue()) {
      editor.setValue(val)
    }
  }
)

onBeforeUnmount(() => {
  editor?.dispose()
})
</script>

<style scoped>
.editor-container {
  width: 100%;
  height: 100%;
}
</style>
