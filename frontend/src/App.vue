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
body {
  background-color: #fff;
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
  background-color: rgb(204, 204, 204, 0.6);
  border-radius: 3px;
}

/* 滚动条滑块悬停状态 */
::-webkit-scrollbar-thumb:hover {
  background-color: rgb(204, 204, 204);
}

.pre-container {
  background: rgb(243, 244, 246);
  border-radius: 6px;
}

.pre-header {
  height: 30px;
  padding: 0 10px;
  color: rgb(121, 122, 123);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.pre-header .pre-button {
  padding: 4px;
  color: rgb(121, 122, 123);
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
  background: rgb(226, 226, 227);
  border-radius: 6px;
  padding: 4px;
}

.pre-header .pre-button i {
  margin-left: 4px;
}
</style>
