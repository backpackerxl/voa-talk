<template>
  <div class="chat-header">
    <div class="opt">
      <div class="menu" v-if="!props.menu">
        <svg t="1748089203220" class="menu-icon" viewBox="0 0 1024 1024" version="1.1"
          xmlns="http://www.w3.org/2000/svg" p-id="8748" width="20" height="20" @click="handleMenu">
          <path
            d="M640 448h128V320h-128v128z m256-384H128a64 64 0 0 0-64 64v704a64 64 0 0 0 64 64h768a64 64 0 0 0 64-64V128a64 64 0 0 0-64-64zM448 768H256a64 64 0 0 1-64-64V256a64 64 0 0 1 64-64h192v576z m384-64a64 64 0 0 1-64 64H576V192h192a64 64 0 0 1 64 64v448z m-192-64h128V512h-128v128z"
            p-id="8749"></path>
        </svg>
      </div>
      <div class="title-text">
        <p :class="!props.menu ? 'has' : 'no'">
          {{ props.title }}
        </p>
        <el-icon class="edit-icon" v-if="props.title" @click="editTitle">
          <EditPen />
        </el-icon>
      </div>
    </div>
  </div>
</template>

<script setup>
let emit = defineEmits(["submit", "open-menu"]);
import { EditPen } from "@element-plus/icons-vue";

const props = defineProps({
  id: Number,
  title: String,
  menu: Boolean,
});

function editTitle() {
  emit("submit", props);
}

function handleMenu() {
  emit("open-menu", props);
}

</script>

<style scoped>
.chat-header {
  height: inherit;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--me-body-bg-color);
  padding: 0 15px;
}

.title-text {
  display: flex;
  align-items: center;
}

.title-text .edit-icon {
  opacity: 0;
  margin-left: 4px;
  cursor: pointer;
}

.title-text:hover .edit-icon {
  opacity: 1;
}

.chat-header p.no {
  border-left: 0;
}

.chat-header p.has {
  border-left: 1px solid var(--el-text-color-primary);
}

.chat-header p {
  border-left: 1px solid var(--el-text-color-primary);
  max-width: 280px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--el-text-color-primary);
  padding: 0;
  padding-left: 6px;
  margin: 0;
}

.opt {
  display: flex;
  align-items: center;
}

.menu {
  margin-right: 6px;
  display: flex;
  align-items: center;
}

.menu svg.menu-icon {
  fill: var(--el-text-color-primary);
  cursor: pointer;
  transition: all .2s;
}

@media (max-width: 768px) {
  .chat-header p {
    max-width: 220px;
  }
}
</style>