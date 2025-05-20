<template>
  <div>
    <router-view />
  </div>
</template>

<script>
//注册组件
export default {
  name: "App",
};
</script>
<style>
:root {
  --el-color-primary: rgb(0, 181, 173) !important;
  --el-color-primary-light-3: rgb(0, 181, 173, 0.7) !important;
  --el-color-primary-light-5: rgb(0, 181, 173, 0.5) !important;
  --el-color-primary-light-7: rgb(0, 181, 173, 0.3) !important;
  --el-color-primary-light-8: rgb(0, 181, 173, 0.2) !important;
  --el-color-primary-light-9: rgb(0, 181, 173, 0.1) !important;
  --el-color-primary-dark-2: rgb(0, 181, 173) !important;
}

body {
  background-color: var(--el-fill-color);
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

.pre-container {
  border-radius: 10px;
  background: var(--el-border-color);
}

.pre-header {
  height: 30px;
  padding: 0 10px;
  color: var(--el-text-color-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.pre-header .pre-button {
  padding: 4px;
  color: var(--el-text-color-primary);
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
