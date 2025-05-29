<template>
  <div class="context-menu-container">
    <slot></slot>

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

<script>
export default {
  name: "RightClickMenu",

  props: {
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
  },

  data() {
    return {
      visible: false,
      x: 0,
      y: 0,
      adjustedX: 0,
      adjustedY: 0,
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      currentData: null, // 存储当前右键点击的数据
    };
  },

  computed: {
    menuStyle() {
      return {
        top: `${this.adjustedY}px`,
        left: `${this.adjustedX}px`,
        minWidth: `${this.menuWidth}px`,
      };
    },

    menuHeight() {
      return this.menuItems.length * this.itemHeight;
    },
  },

  methods: {
    openMenu(e, data = null) {
      this.x = e.clientX;
      this.y = e.clientY;
      this.adjustMenuPosition(this.x, this.y);
      this.visible = true;
      this.currentData = data; // 存储传递的数据

      // 点击其他地方关闭菜单
      const closeMenu = () => {
        this.visible = false;
        document.removeEventListener("click", closeMenu);
      };

      document.addEventListener("click", closeMenu);
    },
    adjustMenuPosition(x, y) {
      // 检查右侧边界
      if (x + this.menuWidth > this.windowWidth) {
        this.adjustedX = x - this.menuWidth;
      } else {
        this.adjustedX = x;
      }

      // 检查底部边界
      if (y + this.menuHeight > this.windowHeight) {
        this.adjustedY = y - this.menuHeight;
      } else {
        this.adjustedY = y;
      }

      // 确保不会超出左边界和上边界
      this.adjustedX = Math.max(0, this.adjustedX);
      this.adjustedY = Math.max(0, this.adjustedY);
    },

    handleClick(item) {
      this.visible = false;
      item.action(this.currentData);
    },
  },
};
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