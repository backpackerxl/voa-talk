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
@font-face {
  font-family: "KaushanScript-Regular";
  src: url("@assets/fonts/KaushanScript-Regular.otf") format("opentype");
  font-weight: normal;
  font-style: normal;
}

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
  width: 6px;
  /* 垂直滚动条宽度 */
  height: 6px;
  /* 水平滚动条高度 */
}

/* 滚动条轨道 */
::-webkit-scrollbar-track {
  background-color: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: transparent;
}

/* 滚动条滑块 */
:hover::-webkit-scrollbar-thumb,
:active::-webkit-scrollbar-thumb,
:focus::-webkit-scrollbar-thumb {
  background-color: var(--el-color-info-light-7);
  border-radius: 3px;
}

/* 滚动条滑块悬停状态 */
::-webkit-scrollbar-thumb:hover {
  background-color: var(--el-color-info-light-5);
}

.katex {
  font-size: 1.4em !important;
  transform: scale(0.9);
  transform-origin: center;
}

@media (max-width: 768px) {

  /* 滚动条整体样式 */
  ::-webkit-scrollbar {
    width: 4px;
    /* 垂直滚动条宽度 */
    height: 4px;
    /* 水平滚动条高度 */
  }

  .katex-display,
  .katex-html>.base {
    transform: scale(0.84);
  }
}

.katex-display>.katex>.katex-html {
  overflow-x: auto;
  overflow-y: hidden;
}

.pre-container {
  border-radius: 6px;
  background: var(--me-bg-color);
  margin: 12px 0;
  transition: all 0.1s;
}

.pre-container .mermaid {
  min-height: 330px;
  cursor: grab;
}

.pre-container .mermaid.dragging {
  cursor: grabbing;
}

.pre-container .mermaid svg {
  min-height: 330px;
  user-select: none;
}

.pre-container .mermaid-code {
  padding: 1em;
}

.pre-header-container {
  position: sticky;
  top: -1px;
  background-color: var(--me-body-bg-color);
}

.pre-header-block {
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
  background-color: var(--me-bg-color);
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

.pre-header-tools i {
  margin-right: 4px;
  padding: 4px;
}

.pre-header-tools i:last-child {
  margin-right: 0;
}

.pre-header .pre-button:hover,
.pre-header-tools i:hover {
  background: rgb(117, 116, 116, 0.2);
  border-radius: 6px;
  padding: 4px;
}

.pre-header .pre-button i {
  margin-left: 4px;
}

.code-container i.fa-xmark {
  color: var(--me-report-text-color);
  font-size: 22px;
  padding: 2px 6px;
}

.code-container .code-container-header {
  height: 60px;
  padding: 5px;
  text-align: right;
  padding: 0 15px;
  line-height: 60px;
  border-bottom: 1px solid var(--me-switch-bg-color);
  box-shadow: 0 2px 4px 0 var(--me-box-shadow);
}

.code-container i.fa-xmark:hover {
  background: rgb(117, 116, 116, 0.2);
  border-radius: 6px;
  padding: 4px 6px;
}

.code-container {
  width: 100vw;
  height: 100vh;
  background: var(--me-body-bg-color);
  box-sizing: border-box;
  box-shadow: 0 6px 10px 0 var(--me-box-shadow);
}

.code-container iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>
