<template>
  <el-container>
    <el-aside width="240px">
      <h2 class="mb">AiChat</h2>
      <div class="new-chat">
        <el-button
          class="open-chat"
          type="primary"
          size="large"
          :icon="Plus"
          @click="openNewChat"
          >开启新对话</el-button
        >
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        :router="true"
      >
        <el-menu-item
          v-for="(menuData, index) in menuData"
          :key="index"
          :index="menuData.url"
          class="menu-item"
        >
          <i :class="menuData.icon"></i>
          <span style="margin-left: 15px">{{ menuData.label }}</span>
        </el-menu-item>
      </el-menu>
      <div class="history-chat">
        <ChatList :chat="chatObj" @change-data="handleChatData" />
      </div>
    </el-aside>
    <el-container>
      <el-header
        ><Header :title="chatTitle" :id="chatId" @submit="submitEditMsg"
      /></el-header>
      <el-main class="main"><router-view /></el-main>
    </el-container>
  </el-container>
  <el-dialog
    v-model="centerDialogVisible"
    title="删除对话"
    width="400"
    align-center
  >
    <span>确定删除，对话内容将不可恢复</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteUserOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
    v-model="editDialogVisible"
    title="编辑对话名称"
    width="400"
    align-center
  >
    <el-input size="large" v-model="chatTitleValue" />
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="editMsgOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { onMounted, nextTick, ref, computed, watch } from "vue"; // Ensure computed is imported
import { useStore } from "vuex"; // Use Vuex's useStore function
import Header from "@/components/Header"; // 引入组件
import ChatList from "@/components/ChatList"; // 引入组件
import { queryTalkName } from "@/api/aiChat";

import { Plus } from "@element-plus/icons-vue";
import router from "@/router";
import { useRoute } from "vue-router";

const routePath = useRoute();

const activeMenu = ref(routePath.path);
const centerDialogVisible = ref(false);
const editDialogVisible = ref(false);
const chatTitle = ref("");
const chatTitleValue = ref("");
const chatId = ref(-1);
const store = useStore(); // Initialize the store
const chatObj = ref(null);

watch(
  () => routePath,
  async (newRoute, oldRoute) => {
    activeMenu.value = newRoute.path;
    if (!newRoute.params.id && newRoute.path !== "/home/chat") {
      chatTitle.value = "";
      chatId.value = -1;
      chatObj.value = {
        talk_id: chatId.value,
        talk_name: chatTitle.value,
        type: "open",
      };
    }
  },
  { deep: true }
);

function handleChatData(data) {
  switch (data.type) {
    case "update":
      handleEditMsg(data);
      break;
    case "delete":
      handleDeleteMsg(data);
      break;
    default:
      chatId.value = data.chatId;
      chatTitle.value = data.chatTitle;
      break;
  }
}

const menuData = ref([]);

// 计算属性：判断用户是否是管理员
const userRole = computed(() => store.state.app.userRole || null);
const sliderData = computed(() => store.state.app.sliderData || null);

watch(
  () => sliderData,
  (newSliderData, oldSliderData) => {
    if (newSliderData.value && chatId.value === -1) {
      chatObj.value = {
        ...newSliderData.value,
        type: "new",
      };
      chatTitle.value = newSliderData.value.talk_name;
      chatId.value = newSliderData.value.talk_id;
      if (routePath.path === "/home/chat") {
        routePath.params.id = chatId.value;
      }
      history.pushState({}, "", location.href + "/" + chatId.value);
    }
  },
  { deep: true }
);

// console.log("superAdmin", userRole.value);

const isSuperAdmin = computed(() => userRole.value === 1);

if (isSuperAdmin.value) {
  menuData.value = [
    {
      url: "/home/model",
      label: "模型配置",
      icon: "fa-solid fa-robot",
    },
    {
      url: "/home/user",
      label: "用户管理",
      icon: "fa-solid fa-user-plus",
    },
    ...menuData.value,
  ];
}

async function deleteUserOk() {
  chatObj.value = {
    talk_id: chatId.value,
    talk_name: chatTitleValue.value,
    type: "delete",
  };
  console.log(chatObj.value);
  centerDialogVisible.value = false;
  if (chatId.value === +routePath.params.id) {
    chatTitle.value = "新对话";
    chatId.value = -1;
    router.replace("/home/chat");
  }
}

function handleDeleteMsg(row) {
  centerDialogVisible.value = true;
  console.log(row);
  chatId.value = row.chatId;
  chatTitleValue.value = row.chatTitle;
}

function openNewChat() {
  chatTitle.value = "新对话";
  chatId.value = -1;
  chatObj.value = {
    talk_id: chatId.value,
    talk_name: chatTitle.value,
    type: "open",
  };
  router.replace("/home/chat");
}

async function editMsgOk() {
  chatObj.value = {
    talk_id: chatId.value,
    talk_name: chatTitleValue.value,
    type: "update",
  };
  if (chatId.value === +routePath.params.id) {
    chatTitle.value = chatTitleValue.value;
  }
  editDialogVisible.value = false;
}

function handleEditMsg(row) {
  editDialogVisible.value = true;
  chatTitleValue.value = row.chatTitle;
  chatId.value = row.chatId;
}

function submitEditMsg(row) {
  editDialogVisible.value = true;
  chatTitleValue.value = row.title;
  chatId.value = row.id;
}

onMounted(() => {
  chatId.value = Number(routePath.params.id);
  nextTick(() => {
    if (chatId.value && chatId.value !== -1) {
      queryTalkName({ talk_id: chatId.value })
        .then((data) => {
          chatTitle.value = data.data || "";
        })
        .catch((err) => {
          console.log(err);
        });
    }
  });
});
</script>

<style scoped>
.el-aside {
  position: fixed;
  top: 0px;
  height: 100vh;
}

.menu-icon {
  width: 18px;
  margin-right: 10px;
}

.mb {
  font-size: 18px;
  color: rgb(0, 0, 0, 0.8);
  margin-left: 20px;
  margin-top: 20px;
}

.menu-item {
  display: flex;
  align-items: center;
}

.menu-item el-icon {
  margin-right: 8px; /* 图标和文字之间的间距 */
}

.menu-item span {
  flex: 1;
}

.main {
  display: flex;
  justify-content: center;
  margin-left: 240px;
  padding: 0;
  overflow: hidden;
}

.new-chat {
  padding: 10px 20px;
  box-sizing: border-box;
}

.open-chat {
  background: rgb(103, 103, 105, 0.8);
  border: none;
  box-shadow: none;
  width: 100%;
}

.open-chat:hover {
  background: rgb(103, 103, 105);
}

.el-menu {
  height: 200px;
  overflow: auto;
}

.history-chat {
  width: 240px;
  position: absolute;
  bottom: 10px;
}
</style>
