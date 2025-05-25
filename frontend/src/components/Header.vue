<template>
  <div class="chat-header">
    <div class="opt">
      <div class="menu" v-if="!props.menu">
        <svg
          t="1748089203220"
          class="menu-icon"
          viewBox="0 0 1024 1024"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          p-id="8748"
          width="20"
          height="20"
          @click="handleMenu"
        >
          <path
            d="M640 448h128V320h-128v128z m256-384H128a64 64 0 0 0-64 64v704a64 64 0 0 0 64 64h768a64 64 0 0 0 64-64V128a64 64 0 0 0-64-64zM448 768H256a64 64 0 0 1-64-64V256a64 64 0 0 1 64-64h192v576z m384-64a64 64 0 0 1-64 64H576V192h192a64 64 0 0 1 64 64v448z m-192-64h128V512h-128v128z"
            p-id="8749"
          ></path>
        </svg>
      </div>
      <p>
        {{ props.title }}
        <el-icon class="edit-icon" v-if="props.title" @click="editTitle"
          ><EditPen
        /></el-icon>
      </p>
    </div>

    <div class="opt-menu">
      <ThemSwitch />
      <el-dropdown
        @visible-change="handleVisibleChange"
        @command="handleCommand"
        trigger="click"
        placement="bottom-end"
      >
        <!-- <div> -->
        <el-avatar v-if="imageUrl" :src="imageUrl" />
        <el-avatar
          v-else
          src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
        />
        <!-- </div> -->
        <template #dropdown>
          <el-dropdown-menu
            :style="{ pointerEvents: isVisible ? 'auto' : 'none' }"
          >
            <el-dropdown-item command="profile"
              ><i class="fa-solid fa-user"></i>我的主页</el-dropdown-item
            >
            <el-dropdown-item command="logout"
              ><i class="fa-solid fa-right-from-bracket"></i
              >退出登录</el-dropdown-item
            >
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
import { useStore } from "vuex"; // Use Vuex's useStore function
import { defineEmits, computed, ref } from "vue";

let emit = defineEmits(["submit", "open-menu"]);
import { EditPen, Plus } from "@element-plus/icons-vue";
import ThemSwitch from "@/components/ThemSwitch";

const props = defineProps({
  id: Number,
  title: String,
  menu: Boolean,
});

const isVisible = ref(false);

const store = useStore(); // Initialize the store

const imageUrl = computed(() => store.state.app.avatar || null);

function editTitle() {
  emit("submit", props);
}

function handleMenu() {
  emit("open-menu", props);
}

function handleVisibleChange(visible) {
  isVisible.value = visible;
}

const router = useRouter();
// Handle dropdown command
const handleCommand = (command) => {
  if (command === "logout") {
    ElMessageBox.confirm("确定要退出登录吗?", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(() => {
        // Perform logout action
        console.log("用户点击退出");

        // 清除 store 中的 authorization 和 userRole
        store.dispatch("app/setAuthorization", "");
        store.dispatch("app/setUserRole", 0);
        store.dispatch("app/setAvatar", "");

        // 重定向到根路径
        router.push("/");
        // 这里可以添加实际的登出逻辑，比如清除 token 或者重定向到登录页面
      })
      .catch(() => {
        console.log("Logout canceled");
      });
  } else if (command === "profile") {
    router.push("/home/profile");
  }
};
</script>

<style scoped>
.chat-header {
  height: inherit;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--me-body-bg-color);
}

.el-avatar--circle {
  outline: none;
}

.chat-header p {
  color: var(--el-text-color-primary);
  padding: 0;
  margin: 0;
}

.opt {
  display: flex;
  align-items: center;
}

.menu {
  border-right: 1px solid var(--el-text-color-primary);
  padding-right: 8px;
  margin-right: 8px;
  display: flex;
  align-items: center;
}

.menu svg.menu-icon {
  fill: var(--el-text-color-primary);
  cursor: pointer;
}

p .edit-icon {
  opacity: 0;
  cursor: pointer;
}

p:hover .edit-icon {
  opacity: 1;
}

.opt-menu {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 120px;
}
</style>