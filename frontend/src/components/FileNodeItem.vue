<template>
  <li>
    <div class="node-row" :class="{ active: isActive }" @click="onClickNode">
      <span v-if="node.type === 'dir'">► {{ node.name }}</span>
      <span v-else>{{ node.name }}</span>
    </div>
    <ul v-if="node.type === 'dir' && node.children?.length" class="children">
      <FileNodeItem
        v-for="child in node.children"
        :key="child.path"
        :node="child"
        :current-file="currentFile"
        @open-file="emit('open-file', $event)"
      />
    </ul>
  </li>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  node: FileNode
  currentFile: string | null
}>()

const emit = defineEmits<{
  (e: 'open-file', path: string): void
}>()

const isActive = computed(() => props.currentFile === props.node.path)

function onClickNode() {
  if (props.node.type === 'file') {
    emit('open-file', props.node.path)
  }
}
</script>

<style scoped>
.node-row {
  padding: 2px 6px;
  cursor: pointer;
  border-radius: 3px;
  font-size: 13px;
}

.node-row:hover {
  background: #f3f3f3;
}

.node-row.active {
  background: #e3f2fd;
}

.children {
  margin-left: 12px;
  padding-left: 0;
  list-style: none;
}
</style>
