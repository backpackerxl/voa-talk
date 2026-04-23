<template>
  <el-skeleton :loading="openLoading" animated>
    <template #template>
      <div :style="{ height: height + 20 + 'px' }">
        <el-skeleton-item variant="text" style="width: 90%; height: 28px; margin-left: 5%; margin-top: 10px" />
        <el-skeleton-item variant="text" style="width: 90%; height: 28px; margin-left: 5%; margin-top: 10px" />
        <el-skeleton-item variant="text" style="width: 90%; height: 28px; margin-left: 5%; margin-top: 10px" />
      </div>
    </template>
    <template #default>
      <div class="infinite-list-wrapper">
        <RightClickMenu ref="rightClickMenu" :menu-items="menuItems">
          <el-scrollbar @end-reached="load" :height="height">
            <ul class="list">
              <li v-for="(chat, index) in tableData" :key="index" :class="chat.talk_id === talkIdOn ? 'list-item active' : 'list-item'
                " @click="openChatHis($event, chat)" :data-index="index" @contextmenu.prevent="openMenu($event, chat)">
                <el-tooltip class="box-item" effect="light" :content="chat.talk_name" placement="right"
                  :disabled="!shouldShowTooltip(index) || !showHis" :show-arrow="false">
                  <template #content>
                    {{ chat.talk_name }}
                  </template>
                  <div class="content">
                    <span :ref="(el) => handleRef(el, index)" class="text-truncate"><i
                        class="fa-regular fa-comments"></i>{{
                          chat.talk_name }}</span>
                    <el-dropdown v-if="showHis" trigger="click" @visible-change="handleVisibleChange"
                      placement="bottom-end" :show-arrow="false">
                      <span class="el-dropdown-link">
                        <i ref="trigger" :data-index="index" class="fa-solid fa-ellipsis"></i>
                      </span>
                      <template #dropdown>
                        <el-dropdown-menu :style="{ pointerEvents: isVisible ? 'auto' : 'none' }">
                          <el-dropdown-item @click="handleEditMsg(chat)"><i
                              class="fa-regular fa-pen-to-square"></i>重命名</el-dropdown-item>
                          <el-dropdown-item class="delete" @click="handleDeleteMsg(chat)"><i
                              class="fa-solid fa-trash"></i>删除</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </el-tooltip>
              </li>
            </ul>
          </el-scrollbar>
        </RightClickMenu>
        <div class="last-msg" v-loading="loading"></div>
      </div>
    </template>
  </el-skeleton>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from "vue";
import router from "@/router";
import { useRoute } from "vue-router";
import RightClickMenu from "@/components/RightClickMenu.vue";
import { debounce } from "@/utils/tools";

const routePath = useRoute();

const props = defineProps({
  chat: {
    type: Object,
    default: null,
  },
  offsetHeight: {
    type: Number,
    default: 0,
  },
});

const totalHeight = ref(window.innerHeight);

const height = computed(() => {
  const h = totalHeight.value - props.offsetHeight - 20;
  if (h > 800) {
    return 800;
  }
  return h;
});

// 监听方法
const onResize = () => {
  totalHeight.value = window.innerHeight;
}

// 定义自定义事件
const emits = defineEmits(["change-data"]);

import { aiChatList } from "@/api/aiChat";
// using es modules
import device from "current-device";

const count = ref(0);
const totalCount = ref(0);
const tableData = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const contentRefs = ref([]);
const isVisible = ref(false);
const moreIcon = ref(null);
const talkIdOn = ref(-1);
const openLoading = ref(false);
const showHis = ref(!device.mobile());

const rightClickMenu = ref(null);

const menuItems = ref([
  {
    icon: "fa-regular fa-pen-to-square",
    label: "重命名",
    classList: [],
    action: (data) => {
      handleEditMsg(data);
    },
  },
  {
    icon: "fa-solid fa-trash",
    label: "删除",
    classList: ["delete"],
    action: (data) => {
      handleDeleteMsg(data);
    },
  },
]);

function openMenu(event, chat) {
  rightClickMenu.value && rightClickMenu.value.handleContextMenu(event, chat);
}

function handleVisibleChange(visible) {
  isVisible.value = visible;
  moreIcon.value.classList.add("show");
  if (!visible) {
    moreIcon.value.classList.remove("show");
    moreIcon.value.focus(); // 将焦点移回触发元素
  }
}

const handleRef = (el, index) => {
  if (el) {
    contentRefs.value[index] = el;
  }
};

function shouldShowTooltip(index) {
  const contentRef = contentRefs.value[index];
  if (contentRef) {
    return contentRef.scrollWidth > contentRef.clientWidth;
  }
  return false;
}

function openChatHis(event, row) {
  if (event.target.tagName === "I") {
    if (moreIcon.value) {
      moreIcon.value.classList.remove("show");
    }
    moreIcon.value = event.target;
    return;
  }
  talkIdOn.value = row.talk_id;
  emits("change-data", {
    chatTitle: row.talk_name,
    chatId: row.talk_id,
    type: "change",
  });
  router.replace("/home/chat/" + row.talk_id);
  document.documentElement.querySelector("title").innerText =
    row.talk_name || "VoaTalk 你的Ai助手";
}

const getAiChatList = async (animated) => {
  openLoading.value = animated;
  let obj = await aiChatList({
    pageSize: pageSize.value,
    pageIndex: currentPage.value,
  });
  tableData.value = tableData.value.concat(obj.data.records);
  totalCount.value = obj.data.total_count;
  loading.value = false;
  openLoading.value = false;
};

const load = (direction) => {
  if (direction === 'bottom') {
    loading.value = true;
    count.value += pageSize.value;
    currentPage.value++;
    getAiChatList(false);
  }
};

watch(
  () => props.chat,
  (newChat, oldChat) => {
    switch (newChat.type) {
      case "update":
        editMsgOk({ talk_id: newChat.talk_id, talk_name: newChat.talk_name });
        break;
      case "delete":
        deleteUserOk({
          talk_id: newChat.talk_id,
          talk_name: newChat.talk_name,
        });
        break;
      case "open":
        talkIdOn.value = newChat.talk_id;
        break;
      case "new":
        delete newChat.type;
        tableData.value = [newChat, ...tableData.value];
        talkIdOn.value = newChat.talk_id;
        break;
      default:
        break;
    }
  }
);

watch(
  () => routePath,
  async (newRoute, oldRoute) => {
    if (newRoute.params.id) {
      talkIdOn.value = +newRoute.params.id;
    }
  },
  { deep: true }
);

async function deleteUserOk(chat) {
  tableData.value = tableData.value.filter(
    (item) => item.talk_id !== chat.talk_id
  );
}

function handleDeleteMsg(row) {
  emits("change-data", {
    chatTitle: row.talk_name,
    chatId: row.talk_id,
    type: "delete",
  });
}

async function editMsgOk(chat) {
  tableData.value.forEach((item) => {
    if (item.talk_id === chat.talk_id) {
      item.talk_name = chat.talk_name;
    }
  });
}

function handleEditMsg(row) {
  emits("change-data", {
    chatTitle: row.talk_name,
    chatId: row.talk_id,
    type: "update",
  });
}

onMounted(function () {
  talkIdOn.value = +routePath.params.id;
  getAiChatList(true);
  window.addEventListener("resize", debounce(onResize));
});

onUnmounted(function () {
  window.removeEventListener("resize", debounce(onResize));
});
</script>

<style>
.infinite-list-wrapper {
  height: inherit;
  padding: 0 5px;
}

.infinite-list-wrapper .list {
  padding: 0;
  margin: 0;
  list-style: none;
  font-size: 14px;
}

.infinite-list-wrapper .list-item {
  height: 40px;
  color: var(--el-text-color-primary);
  user-select: none;
}

.infinite-list-wrapper .list-item:hover,
.infinite-list-wrapper .list-item.active {
  background: var(--el-color-info-light-8);
  cursor: pointer;
  border-radius: 14px;
}

.list-item .content i.fa-ellipsis {
  display: none;
}

.list-item .content i.fa-ellipsis.show,
.list-item .content:hover i.fa-ellipsis,
.list-item.active .content i.fa-ellipsis {
  display: block;
}

.list-item .content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: inherit;
  padding: 0 10px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-touch-callout: none;
}

.list-item .content .text-truncate {
  width: 170px;
  padding: 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
}

.el-dropdown-menu {
  padding: 6px;
}

.el-dropdown-menu__item {
  border-radius: 6px;
}

.delete {
  --el-dropdown-menuItem-hover-fill: rgb(255, 59, 48, 0.1);
  --el-dropdown-menuItem-hover-color: rgb(255, 59, 48);
  --el-text-color-regular: rgb(255, 59, 48);
}

.content .text-truncate i.fa-comments {
  margin-right: 8px;
}

.infinite-list-wrapper .list-item+.list-item {
  margin-top: 1px;
}

.last-msg {
  height: 20px;
  width: 20px;
  --el-loading-spinner-size: 18px;
}

:deep(.el-loading-mask) {
  background-color: transparent !important;
}

:deep(.el-loading-spinner .path) {
  stroke-width: 4 !important;
}

.context-menu-item.delete {
  color: rgb(255, 59, 48) !important;
}

.context-menu-item.delete:hover {
  background-color: rgb(255, 59, 48, 0.1) !important;
  color: rgb(255, 59, 48) !important;
}
</style>