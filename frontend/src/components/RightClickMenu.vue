<template>
  <div class="context-menu-container">
    <div ref="slotContainer">
      <slot></slot>
    </div>

    <div v-if="visible" class="context-menu" :style="menuStyle" @click.stop>
      <div
        v-for="(item, index) in menuItems"
        :key="index"
        :class="
          item.classList.length == 0
            ? 'context-menu-item'
            : `context-menu-item ${item.classList.join(' ')}`
        "
        @click="handleClick(item)"
      >
        <i :class="item.icon"></i>
        {{ item.label }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";

const props = defineProps({
  menuItems: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(
        (item) =>
          typeof item.label === "string" &&
          typeof item.icon === "string" &&
          typeof item.classList === "object" &&
          typeof item.action === "function"
      );
    },
  },
  menuWidth: {
    type: Number,
    default: 150,
  },
  itemHeight: {
    type: Number,
    default: 32,
  },
});

// 引用插槽容器元素
const slotContainer = ref(null);

// 响应式状态
const visible = ref(false);
const x = ref(0);
const y = ref(0);
const adjustedX = ref(0);
const adjustedY = ref(0);
const containerRect = ref({});
const windowHeight = ref(window.innerHeight);
const currentData = ref(null);

// 计算属性
const menuStyle = computed(() => ({
  top: `${adjustedY.value}px`,
  left: `${adjustedX.value}px`,
  minWidth: `${props.menuWidth}px`,
}));

const menuHeight = computed(() => props.menuItems.length * props.itemHeight);

// 更新容器尺寸信息
const updateContainerRect = () => {
  if (slotContainer.value) {
    containerRect.value = slotContainer.value.getBoundingClientRect();
  }
};

// 方法
const handleContextMenu = (e, data = null) => {
  updateContainerRect();
  openMenu(e, data);
};

let currrData = null;

const openMenu = (e, data = null) => {
  x.value = e.clientX;
  y.value = e.clientY;
  adjustMenuPosition(x.value, y.value);
  visible.value = true;
  currentData.value = data;

  // 点击其他地方关闭菜单
  const closeMenu = () => {
    visible.value = false;
    document.removeEventListener("click", closeMenu);
  };

  document.addEventListener("click", closeMenu);
};

const adjustMenuPosition = (x, y) => {
  // 基于插槽容器的位置进行边界检测
  const container = containerRect.value;

  // 检查右侧边界（相对于容器）
  if (x + props.menuWidth > container.right) {
    // 尝试将菜单显示在左侧
    const leftSpace = x - container.left;
    if (leftSpace >= props.menuWidth) {
      adjustedX.value = x - props.menuWidth;
    } else {
      // 左右空间都不足，优先显示在右侧，可能会超出容器
      adjustedX.value = x;
    }
  } else {
    adjustedX.value = x;
  }

  // 检查底部边界
  if (y + menuHeight.value > windowHeight.value) {
    adjustedY.value = y - menuHeight.value;
  } else {
    adjustedY.value = y;
  }

  // 确保不会超出容器边界
  adjustedX.value = Math.max(
    container.left,
    Math.min(adjustedX.value, container.right - props.menuWidth)
  );
  adjustedY.value = Math.max(
    container.top,
    Math.min(adjustedY.value, container.bottom - menuHeight.value)
  );
};

const handleClick = (item) => {
  visible.value = false;
  item.action(currentData.value);
};

// 生命周期钩子
onMounted(() => {
  updateContainerRect();

  // 监听窗口大小变化
  const handleResize = () => {
    updateContainerRect();
  };

  window.addEventListener("resize", handleResize);

  // 组件卸载时移除监听器
  onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
  });
});

// 暴露方法供外部使用
defineExpose({
  handleContextMenu,
});
</script>

<style scoped>
.context-menu-container {
  position: relative;
}

.context-menu {
  position: fixed;
  background-color: var(--el-bg-color-overlay);
  border-radius: var(--el-border-radius-base);
  box-shadow: var(--el-box-shadow-light);
  z-index: 1000;
  min-width: 120px;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid var(--me-table-th-color);
}

.context-menu-item {
  color: var(--me-report-text-color);
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  border-bottom: 1px solid var(--me-table-th-color);
}

.context-menu-item:last-child {
  border-bottom: 0px;
}

.context-menu-item:hover {
  background-color: var(--el-color-primary-light-9);
  border-radius: 6px;
  color: var(--el-color-primary);
}
</style>