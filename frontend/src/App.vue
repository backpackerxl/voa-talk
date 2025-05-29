<template>
  <router-view />
</template>

<script setup>
import store from "@/store";
import { onMounted } from "vue";
import "@/assets/css/me-main-color.css";
import { handleThem } from "@/utils/tools";

onMounted(function () {
  const item = JSON.parse(store.state.app.them);
  handleThem(item);
  let colorObj = store.state.app.mainColor;
  if (colorObj) {
    let tag = JSON.parse(colorObj).tag;
    if (tag) {
      document.documentElement.classList.add(tag);
    }
  }
});
</script>
<style>
* {
  -webkit-tap-highlight-color: transparent;
}

html {
  overflow: hidden;
}

body {
  background-color: var(--me-body-bg-color);
  margin: 0;
}

/* 滚动条整体样式 */
::-webkit-scrollbar {
  width: 6px; /* 垂直滚动条宽度 */
  height: 6px; /* 水平滚动条高度 */
}

/* 滚动条轨道 */
::-webkit-scrollbar-track {
  background-color: transparent;
}

/* 滚动条滑块 */
::-webkit-scrollbar-thumb {
  background-color: var(--el-color-info-light-7);
  border-radius: 3px;
}

/* 滚动条滑块悬停状态 */
::-webkit-scrollbar-thumb:hover {
  background-color: var(--el-color-info-light-5);
}

@media (max-width: 768px) {
  /* 滚动条整体样式 */
  ::-webkit-scrollbar {
    width: 4px; /* 垂直滚动条宽度 */
    height: 4px; /* 水平滚动条高度 */
  }
}

.pre-container {
  border-radius: 6px;
  background: var(--me-bg-color);
  border: 1px solid var(--borderColor-default);
  margin: 12px 0;
}

.pre-header {
  height: 32px;
  padding: 0 10px;
  color: var(--me-report-text-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.pre-header .pre-button {
  padding: 4px;
  color: var(--me-report-text-color);
  outline: none;
  border: none;
  background: transparent;
  font-size: 14px;
}

.pre-header i.copy-icon {
  padding: 4px;
}

.pre-header .pre-button:hover,
.pre-header i.copy-icon:hover {
  background: rgb(117, 116, 116, 0.2);
  border-radius: 6px;
  padding: 4px;
}

.pre-header .pre-button i {
  margin-left: 4px;
}
</style>
