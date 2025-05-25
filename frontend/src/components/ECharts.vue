<template>
  <div ref="chartRef" class="w-full" :style="{ height: height }"></div>
</template>

<script setup>
import {
  ref,
  onMounted,
  onUnmounted,
  nextTick,
  watch,
  defineExpose,
} from "vue";
import echarts from "@/utils/echarts";
import store from "@/store";

const props = defineProps({
  option: {
    type: Object,
    required: true,
  },
  height: {
    type: String,
    default: "400px",
  },
  autoResize: {
    type: Boolean,
    default: true,
  },
});

const chartRef = ref(null);
let myChart = null;

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return;

  myChart = echarts.init(chartRef.value, store.state.app.them);
  
  myChart.setOption(props.option);

  // 监听窗口大小变化
  if (props.autoResize) {
    window.addEventListener("resize", handleResize);
  }
};

// 处理窗口大小变化
const handleResize = () => {
  myChart?.resize();
};

// 销毁图表
const destroyChart = () => {
  if (myChart) {
    if (props.autoResize) {
      window.removeEventListener("resize", handleResize);
    }
    myChart.dispose();
    myChart = null;
  }
};

// 监听 option 变化
watch(
  () => props.option,
  (newOption) => {
    if (myChart) {
      myChart.setOption(newOption);
    }
  },
  { deep: true }
);

function toggleThem() {
  destroyChart();
  initChart();
}

onMounted(() => {
  nextTick(() => {
    initChart();
  });
});

defineExpose({
  toggleThem: toggleThem,
});

onUnmounted(() => {
  destroyChart();
});
</script>

<style scoped>
div {
  min-height: 200px;
}
</style>
