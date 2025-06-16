<template>
  <div class="container">
    <div
      :class="successTag ? 'captcha-container success' : 'captcha-container'"
      v-loading="loading"
    >
      <img :src="bgBase64" class="bg-image" ref="bgImage" />
      <div class="slider" ref="slider"></div>
    </div>
    <transition name="el-zoom-in-top">
      <div v-show="pContainer" class="progress-container">
        <div class="progress-bar" ref="progress"></div>
        <div class="slider-block" ref="sliderBlock">
          <el-icon><DArrowRight /></el-icon>
        </div>
      </div>
    </transition>
    <el-button type="primary" @click="init" :icon="RefreshRight"
      >刷新验证码</el-button
    >
  </div>
</template>

<script setup>
import { verify, refresh } from "@/api/captcha";
import { nextTick, ref } from "vue";
import { RefreshRight, DArrowRight } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

let emit = defineEmits(["verify"]);

const bgBase64 = ref("");
let trace = ref([]);
const slider = ref(null);
const bgImage = ref(null);
const progress = ref(null);
const sliderBlock = ref(null);
const sliderBlockX = ref(0);
const token = ref("");
const loading = ref(false);
const successTag = ref(false);
const pContainer = ref(false);

const maxLeft = 280;
let isDragging = false;
let startX = 0;
let startLeft = 0;

function startDrag(e) {
  e.preventDefault();
  isDragging = true;
  startX = e.clientX;
  startLeft = parseInt(sliderBlock.value.style.left) || 0;
  document.addEventListener("mousemove", drag);
  document.addEventListener("mouseup", endDrag);
  sliderBlock.value.style.cursor = "grabbing";
  trace.value = [
    {
      x: slider.value.getBoundingClientRect().left - sliderBlockX.value + 2,
      t: Date.now(),
    },
  ];
}

function handleTouchStart(e) {
  e.preventDefault();
  isDragging = true;
  startX = e.touches[0].clientX;
  startLeft = parseInt(sliderBlock.value.style.left) || 0;
  document.addEventListener("touchmove", handleTouchMove, { passive: false });
  document.addEventListener("touchend", endDrag);
  trace.value = [
    {
      x: slider.value.getBoundingClientRect().left - sliderBlockX.value + 2,
      t: Date.now(),
    },
  ];
}

function drag(e) {
  if (!isDragging) return;
  e.preventDefault();
  updateSliderPosition(e.clientX);
  trace.value.push({
    x: slider.value.getBoundingClientRect().left - sliderBlockX.value,
    t: Date.now(),
  });
}

function handleTouchMove(e) {
  if (!isDragging) return;
  e.preventDefault();
  updateSliderPosition(e.touches[0].clientX);
  trace.value.push({
    x: slider.value.getBoundingClientRect().left - sliderBlockX.value,
    t: Date.now(),
  });
}

function updateSliderPosition(currentX) {
  const dx = currentX - startX;
  const newLeft = Math.max(0, Math.min(startLeft + dx, maxLeft));
  slider.value.style.left = `${newLeft}px`;
  const per = (newLeft / maxLeft) * 100;
  if (per === 100) {
    sliderBlock.value.style.left = `${newLeft - 2}px`;
  } else {
    sliderBlock.value.style.left = `${newLeft + 2}px`;
  }
  progress.value.style.width = `${per}%`;
}

function endDrag() {
  if (!isDragging) return;

  isDragging = false;
  document.removeEventListener("mousemove", drag);
  document.removeEventListener("touchmove", handleTouchMove);
  document.removeEventListener("mouseup", endDrag);
  document.removeEventListener("touchend", endDrag);

  sliderBlock.value.style.cursor = "grab";
  verifyPosition();
}

async function verifyPosition() {
  try {
    const response = await verify({
      token: token.value,
      x: parseInt(slider.value.style.left) - 60 || 0,
      trace: trace.value,
    });

    if (response.data.refresh) {
      pContainer.value = false;
      successTag.value = true;
      setTimeout(function () {
        emit("verify", {
          tag: true,
          token: token.value,
        });
        successTag.value = false;
      }, 800);
    } else {
      init();
      ElMessage.error(response.data.msg);
    }
  } catch (err) {
    slider.value.style.left = "0px";
    sliderBlock.value.style.left = "2px";
    progress.value.style.width = `0%`;
  }
}

async function init() {
  pContainer.value = false;
  if (sliderBlock.value) {
    sliderBlock.value.style.left = "2px";
  }
  if (progress.value) {
    progress.value.style.width = `0%`;
  }
  loading.value = true;
  const obj = await refresh();
  bgBase64.value = "data:image/png;base64," + obj.data.bg_base64;
  token.value = obj.data.token;
  if (slider.value) {
    slider.value.style.background = `url('data:image/png;base64,${obj.data.slider_base64}') no-repeat`;
    slider.value.style.top = `${obj.data.gap_y}px`;
    slider.value.style.left = `0px`;
    slider.value.style.width = `${obj.data.slider_width}px`;
    slider.value.style.height = `${obj.data.slider_height}px`;
  }
  loading.value = false;
  pContainer.value = true;
  trace.value = [];
  nextTick(function () {
    sliderBlockX.value = sliderBlock.value.getBoundingClientRect().left || 0;
  });
}

nextTick(function () {
  init();
  // 事件监听
  if (sliderBlock.value) {
    sliderBlock.value.addEventListener("mousedown", startDrag);
    sliderBlock.value.addEventListener("touchstart", handleTouchStart, {
      passive: false,
    });
  }
});

defineExpose({
  init,
});
</script>

<style scoped>
.container {
  width: 360px;
  background: var(--el-bg-color-overlay);
  padding: 20px;
  text-align: center;
  box-sizing: border-box;
}

.captcha-container {
  position: relative;
  margin: 20px 0;
  overflow: hidden;
  width: 320px;
  height: 150px;
  text-align: right;
}

.captcha-container.success {
  position: relative;
}

.captcha-container.success::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: var(--el-overlay-color-lighter);
  z-index: 9;
}

.captcha-container.success::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 32px;
  height: 32px;
  background: url("@/assets/images/success.svg") no-repeat center / contain;
  z-index: 10;
}

.bg-image {
  object-fit: cover;
}

.slider {
  position: absolute;
  background-size: 100% 100%;
  left: 0px;
  transition: transform 0.1s;
  z-index: 5;
}

.progress-container {
  height: 30px;
  border-radius: 15px;
  background: var(--me-switch-bg-color);
  margin-bottom: 20px;
  overflow: hidden;
  position: relative;
}
.progress-container .slider-block {
  width: 40px;
  height: 26px;
  border-radius: 15px;
  background: var(--me-body-bg-color);
  position: absolute;
  top: 2px;
  left: 2px;
  cursor: grab;
  font-size: 16px;
  color: var(--el-color-info);
  line-height: 30px;
}

.progress-container .progress-bar {
  height: 100%;
  background: var(--el-color-primary);
  width: 0%;
  border-radius: 15px;
}
</style>