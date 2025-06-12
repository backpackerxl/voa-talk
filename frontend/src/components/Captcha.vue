<template>
  <div class="container">
    <p>请拖动滑块完成验证</p>

    <div class="captcha-container" v-loading="loading">
      <img :src="bgBase64" class="bg-image" ref="bgImage" />
      <div class="slider" ref="slider"></div>
    </div>

    <transition name="el-zoom-in-top">
      <div v-show="pContainer" class="progress-container">
        <div class="progress-bar" ref="progress"></div>
        <div class="slider-block" ref="sliderBlock"></div>
      </div>
    </transition>

    <el-button type="primary" @click="init" :icon="RefreshRight"
      >刷新验证码</el-button
    >
  </div>
</template>

<script setup>
import { verify, refresh } from "@/api/captcha";
import { onMounted, ref } from "vue";
import { RefreshRight } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
const bgBase64 = ref("");
const slider = ref(null);
const bgImage = ref(null);
const progress = ref(null);
const sliderBlock = ref(null);
const token = ref("");
const loading = ref(false);
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
}

function handleTouchStart(e) {
  e.preventDefault();
  isDragging = true;
  startX = e.touches[0].clientX;
  startLeft = parseInt(sliderBlock.value.style.left) || 0;
  document.addEventListener("touchmove", handleTouchMove, { passive: false });
  document.addEventListener("touchend", endDrag);
}

function drag(e) {
  if (!isDragging) return;
  e.preventDefault();
  updateSliderPosition(e.clientX);
}

function handleTouchMove(e) {
  if (!isDragging) return;
  e.preventDefault();
  updateSliderPosition(e.touches[0].clientX);
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
    });

    if (response.data.refresh) {
      pContainer.value = false;
      ElMessage.success(response.data.msg);
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
  sliderBlock.value.style.left = "2px";
  progress.value.style.width = `0%`;
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
}
onMounted(function () {
  init();
  // 事件监听
  sliderBlock.value.addEventListener("mousedown", startDrag);
  sliderBlock.value.addEventListener("touchstart", handleTouchStart, {
    passive: false,
  });
});
</script>

<style scoped>
.container {
  width: 360px;
  background: white;
  padding: 20px;
  text-align: center;
  box-sizing: border-box;
}

.container p {
  padding: 0px;
  margin: 0px;
}

.captcha-container {
  position: relative;
  margin: 20px 0;
  overflow: hidden;
  width: 320px;
  height: 150px;
  text-align: right;
}
.bg-image {
  object-fit: cover;
}
.slider-track {
  height: 70px;
  background: #f8f9fa;
  border-radius: 8px;
  position: relative;
  margin: 15px 0;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}
.slider {
  position: absolute;
  background-size: 100% 100%;
  left: 0px;
  transition: transform 0.1s;
  z-index: 10;
}

.slider:active {
  cursor: grabbing;
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}
.progress-container {
  height: 30px;
  border-radius: 15px;
  background: #cfd0d1;
  margin-bottom: 20px;
  overflow: hidden;
  position: relative;
}
.progress-container .slider-block {
  width: 40px;
  height: 26px;
  border-radius: 15px;
  background: #fff;
  position: absolute;
  top: 2px;
  left: 2px;
  cursor: grab;
}

.progress-container .progress-bar {
  height: 100%;
  background: #00b458;
  width: 0%;
  border-radius: 15px;
}
</style>