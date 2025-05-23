<template>
  <el-container class="me-container">
    <el-aside width="240px">
      <h2 class="mb">VoaTalk</h2>
      <div class="new-chat">
        <el-button
          class="open-chat"
          type="primary"
          size="large"
          @click="openNewChat"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            width="97"
            height="99.33775329589844"
            viewBox="0 0 97 99.33775329589844"
            fill="none"
            class="logo"
          >
            <g filter="url(#filter_3_22)">
              <path
                fill="rgba(255, 255, 255, 1)"
                d="M22.3333 16.0013L74.6667 16.0013C84.7919 16.0013 93 24.2095 93 34.3347L93 67.668C93 77.7932 84.7919 86.0013 74.6667 86.0013L22.3333 86.0013C12.2081 86.0013 4 77.7932 4 67.668L4 34.3347C4 24.2095 12.2081 16.0013 22.3333 16.0013ZM22.3333 26.0013C17.731 26.0013 14 29.7323 14 34.3347L14 67.668C14 72.2704 17.731 76.0013 22.3333 76.0013L74.6667 76.0013C79.269 76.0013 83 72.2704 83 67.668L83 34.3347C83 29.7323 79.269 26.0013 74.6667 26.0013L22.3333 26.0013Z"
              ></path>
            </g>
            <path
              fill="rgba(255, 255, 255, 1)"
              d="M61.3015 17.6882L66.4318 3.59278L75.8288 7.01298L70.6985 21.1084L61.3015 17.6882ZM75.8288 7.01298C74.8843 9.60787 72.0151 10.9458 69.4202 10.0013C66.8253 9.05688 65.4874 6.18767 66.4318 3.59278C67.3763 0.997892 70.2455 -0.340044 72.8404 0.604418C75.4353 1.54888 76.7732 4.41809 75.8288 7.01298Z"
            ></path>
            <path
              fill="rgba(255, 255, 255, 1)"
              d="M33.6985 3.29124L38.8288 17.3866L29.4318 20.8068L24.3015 6.71144L33.6985 3.29124ZM24.3015 6.71144C23.3571 4.11655 24.695 1.24734 27.2899 0.30288C29.8848 -0.641582 32.754 0.696353 33.6985 3.29124C34.6429 5.88613 33.305 8.75534 30.7101 9.69981C28.1152 10.6443 25.246 9.30633 24.3015 6.71144Z"
            ></path>
            <path
              stroke="rgba(255, 255, 255, 1)"
              stroke-width="10"
              stroke-linecap="round"
              d="M40.6018 50.5092L29 41.0013"
            ></path>
            <path
              stroke="rgba(255, 255, 255, 1)"
              stroke-width="10"
              stroke-linecap="round"
              d="M27 57.837L40.3519 51.0013"
            ></path>
            <path
              stroke="rgba(255, 255, 255, 1)"
              stroke-width="10"
              stroke-linecap="round"
              d="M66 43.0013L66 59.0013"
            ></path>
            <path
              stroke="rgba(255, 255, 255, 1)"
              stroke-width="10"
              stroke-linecap="round"
              d="M28 94.3378L67.9994 94.1135"
            ></path>
            <defs>
              <filter
                id="filter_3_22"
                x="0"
                y="14.0013427734375"
                width="97"
                height="78"
                filterUnits="userSpaceOnUse"
                color-interpolation-filters="sRGB"
              >
                <feFlood flood-opacity="0" result="feFloodId_3_22" />
                <feColorMatrix
                  in="SourceAlpha"
                  type="matrix"
                  values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                  result="hardAlpha_3_22"
                />
                <feOffset dx="0" dy="2" />
                <feGaussianBlur stdDeviation="2" />
                <feComposite in2="hardAlpha_3_22" operator="out" />
                <feColorMatrix
                  type="matrix"
                  values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"
                />
                <feBlend
                  mode="normal"
                  in2="feFloodId_3_22"
                  result="dropShadow_1_3_22"
                />
                <feBlend
                  mode="normal"
                  in="SourceGraphic"
                  in2="dropShadow_1_3_22"
                  result="shape_3_22"
                />
              </filter>
            </defs>
          </svg>
          开启新对话</el-button
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
      <el-main id="chatView" class="chat-view"><router-view /></el-main>
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
    // 跳过初始触发
    if (oldSliderData === undefined) return;
    if (newSliderData.value) {
      chatObj.value = newSliderData.value;
      chatTitle.value = newSliderData.value.talk_name;
      chatId.value = newSliderData.value.talk_id;
      if (routePath.path === "/home/chat" || routePath.path === "/home/chat/") {
        routePath.params.id = chatId.value;
        const currentPath = location.pathname;
        let expectedPath = null;
        if (currentPath.endsWith("/")) {
          expectedPath = `${currentPath}${chatId.value}`;
        } else {
          expectedPath = `${currentPath}/${chatId.value}`;
        }

        // 避免重复添加相同的 ID
        if (
          currentPath !== expectedPath &&
          !currentPath.endsWith(`/${chatId.value}`)
        ) {
          history.pushState({}, "", expectedPath);
        }
      }
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
  // console.log(chatObj.value);
  centerDialogVisible.value = false;
  if (chatId.value === +routePath.params.id) {
    chatTitle.value = "新对话";
    chatId.value = -1;
    router.replace("/home/chat");
  }
}

function handleDeleteMsg(row) {
  centerDialogVisible.value = true;
  // console.log(row);
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
  document.documentElement.querySelector("title").innerText =
    chatTitle.value || "VoaTalk 你的Ai助手";
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
          if (chatTitle.value && chatTitle.value !== "") {
            document.documentElement.querySelector("title").innerText =
              chatTitle.value || "VoaTalk 你的Ai助手";
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  });
});
</script>

<style scoped>
.me-container {
  display: flex;
}

.el-aside {
  background-color: var(--el-bg-color);
}

.menu-icon {
  width: 18px;
  margin-right: 10px;
}

.mb {
  font-size: 18px;
  color: var(--el-text-color-primary);
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

.el-main {
  flex: none !important;
  padding: 0px !important;
}

.el-container {
  width: 100%;
}

.new-chat {
  padding: 10px 20px;
  box-sizing: border-box;
}

.open-chat {
  border: none;
  box-shadow: none;
  width: 100%;
}

.new-chat svg.logo {
  width: 16px;
  height: 16px;
  margin-right: 4px;
}

.el-menu {
  height: 200px;
  overflow: auto;
}
</style>
