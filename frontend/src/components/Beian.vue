<template>
  <footer class="footer">
    <p class="beian">
      <a target="_blank" href="https://beian.miit.gov.cn"
        >蜀ICP备2025143448号-1</a
      >
    </p>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.beian {
  position: fixed;
  bottom: 6px;
  left: 0;
  right: 0;
  text-align: center;
  padding: 0;
  margin: 0;
  z-index: 100;
  font-size: 14px;
}

.beian a {
  font-size: 14px;
  color: var(--me-report-text-color);
  text-decoration: none;
}
</style>