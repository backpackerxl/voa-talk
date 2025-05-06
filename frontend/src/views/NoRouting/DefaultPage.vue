<template>
    <div class="default-page">
      <h1>页面未找到</h1>
      <p>很抱歉，您尝试访问的页面不存在。</p>
      <router-link to="/">返回首页</router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DefaultPage',
  };
  </script>
  
  <style scoped>
  .default-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    text-align: center;
  }
  
  .default-page h1 {
    margin-bottom: 20px;
  }
  
  .default-page p {
    margin-bottom: 20px;
  }
  </style>
  