<template>
  <div class="header-container">
    <p>历史对话</p>
    <div class="his-icon">
      <el-tooltip
        class="box-item"
        effect="light"
        content="查看全部"
        placement="top-start"
      >
        <el-icon style="cursor: pointer" @click="openChatHisList"
          ><i class="fa-regular fa-clock"></i
        ></el-icon>
      </el-tooltip>
    </div>
  </div>
  <div class="infinite-list-wrapper" style="overflow: auto">
    <ul
      v-infinite-scroll="load"
      class="list"
      :infinite-scroll-disabled="disabled"
    >
      <li
        v-for="(chat, index) in tableData"
        :key="index"
        :class="chat.talk_id === talkIdOn ? 'list-item active' : 'list-item'"
        @click="openChatHis($event, chat)"
        :data-index="index"
      >
        <el-tooltip
          class="box-item"
          effect="light"
          :content="chat.talk_name"
          placement="right"
          :disabled="!shouldShowTooltip(index)"
        >
          <template #content>
            {{ chat.talk_name }}
          </template>
          <div class="content">
            <span :ref="(el) => handleRef(el, index)" class="text-truncate"
              ><i class="fa-regular fa-comments"></i>{{ chat.talk_name }}</span
            >
            <el-dropdown
              trigger="click"
              @visible-change="handleVisibleChange"
              placement="bottom-end"
            >
              <span class="el-dropdown-link">
                <i
                  ref="trigger"
                  :data-index="index"
                  class="fa-solid fa-ellipsis"
                ></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu
                  :style="{ pointerEvents: isVisible ? 'auto' : 'none' }"
                >
                  <el-dropdown-item :icon="EditPen" @click="handleEditMsg(chat)"
                    >重命名</el-dropdown-item
                  >
                  <el-dropdown-item
                    :icon="Delete"
                    class="delete"
                    @click="handleDeleteMsg(chat)"
                    >删除</el-dropdown-item
                  >
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-tooltip>
      </li>
    </ul>
    <div class="last-msg" v-loading="loading"></div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, defineEmits, defineProps, watch } from "vue";
import router from "@/router";
import { EditPen, Delete } from "@element-plus/icons-vue";
import { useRoute } from "vue-router";

const routePath = useRoute();

const props = defineProps({
  chat: {
    type: Object,
    default: null,
  },
});

// 定义自定义事件
const emits = defineEmits(["change-data"]);

import { aiChatList, deleteChat, editChatName } from "@/api/aiChat";

const count = ref(0);
const totalCount = ref(0);
const tableData = ref([]);
const loading = ref(false);
const noMore = computed(() => count.value >= totalCount.value);
const disabled = computed(() => loading.value || noMore.value);
const currentPage = ref(1);
const pageSize = ref(15);
const contentRefs = ref([]);
const isVisible = ref(false);
const moreIcon = ref(null);
const talkIdOn = ref(-1);

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

function openChatHisList() {
  emits("change-data", { chatTitle: "", chatId: -1, type: "change" });
  router.replace("/home/chat/history");
}

const getAiChatList = () => {
  aiChatList({
    pageSize: pageSize.value,
    pageIndex: currentPage.value,
  })
    .then((obj) => {
      tableData.value = tableData.value.concat(obj.data.records);
      totalCount.value = obj.data.total_count;
      loading.value = false;
    })
    .catch((err) => {
      console.log(err);
      loading.value = false;
    });
};

const load = () => {
  loading.value = true;
  count.value += pageSize.value;
  currentPage.value++;
  getAiChatList();
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
  await deleteChat({ talk_id: chat.talk_id + "" });
  tableData.value = tableData.value.filter(
    (item) => item.talk_id !== chat.talk_id
  );
  getAiChatList();
}

function handleDeleteMsg(row) {
  emits("change-data", {
    chatTitle: row.talk_name,
    chatId: row.talk_id,
    type: "delete",
  });
}

async function editMsgOk(chat) {
  await editChatName(chat);
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
  getAiChatList();
});
</script>

<style>
.header-container {
  color: var(--el-text-color-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 40px;
  padding-left: 15px;
  padding-right: 18px;
  border-top: 1px solid var(--el-color-info-light-8);
  background: var(--el-bg-color);
  box-sizing: border-box;
}

.header-container .his-icon {
  display: none;
}

.header-container:hover .his-icon {
  display: block;
}

.infinite-list-wrapper {
  height: calc(100vh - 360px);
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

.el-popper[data-popper-placement="bottom-end"] > .el-popper__arrow {
  top: 0 !important;
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

.infinite-list-wrapper .list-item + .list-item {
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
</style>