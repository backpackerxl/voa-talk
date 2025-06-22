<template>
  <div class="scorll-bottom">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="46"
      height="46"
      fill="none"
      viewBox="0 0 46 46"
      class="loading-border"
      v-if="changeIcon"
    >
      <path
        fill="currentColor"
        d="M1 23C1 10.85 10.85 1 23 1s22 9.85 22 22-9.85 22-22 22S1 35.15 1 23"
      ></path>
      <circle
        cx="23"
        cy="23"
        r="22.3"
        stroke="var(--el-color-primary)"
        stroke-opacity="0.1"
        stroke-width="1.5"
      ></circle>
      <path
        stroke="url(#partial_border_svg__a)"
        stroke-width="1.5"
        d="M45 23c0-12.15-9.85-22-22-22"
      ></path>
      <defs>
        <linearGradient
          id="partial_border_svg__a"
          x1="23"
          x2="49.163"
          y1="1"
          y2="8.171"
          gradientUnits="userSpaceOnUse"
        >
          <stop stop-color="var(--el-color-primary)" stop-opacity="0"></stop>
          <stop
            offset="0.502"
            stop-color="var(--el-color-primary)"
            stop-opacity="0.6"
          ></stop>
          <stop
            offset="1"
            stop-color="var(--el-color-primary)"
            stop-opacity="0"
          ></stop>
        </linearGradient>
      </defs>
    </svg>
    <el-icon><ArrowDown /></el-icon>
  </div>
</template>

<script setup>
import { ArrowDown } from "@element-plus/icons-vue";

const props = defineProps({
  changeIcon: Boolean,
});
</script>

<style scoped>
.scorll-bottom {
  width: 45px;
  height: 45px;
  border-radius: 25px;
  background-color: var(--me-body-bg-color);
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.12);
  color: var(--el-color-primary);
  position: absolute;
  left: 50%;
  top: -60px;
  z-index: 10;
  font-size: 20px;
  line-height: 50px;
  text-align: center;
  transform: translateX(-50%);
  cursor: pointer;
}

.scorll-bottom .loading-border {
  animation: rotate-SpmXy3 1.3s linear infinite;
  color: #fff;
  color: var(--static-white-transparent-1, #fff);
  height: 100%;
  left: 0;
  position: absolute;
  top: 0;
  width: 100%;
  z-index: -1;
}

@keyframes rotate-SpmXy3 {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(1turn);
  }
}
</style>