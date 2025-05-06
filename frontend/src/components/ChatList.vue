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
        class="list-item"
        @click="openChatHis($event, chat)"
        :data-index="index"
      >
        <el-tooltip
          class="box-item"
          effect="dark"
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
const oldTarget = ref(null);
const isVisible = ref(false);
const moreIcon = ref(null);

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
  if (oldTarget.value) {
    oldTarget.value.classList.remove("active");
  }
  const currentTarget = event.currentTarget;
  currentTarget.classList.add("active");
  oldTarget.value = currentTarget;
  emits("change-data", {
    chatTitle: row.talk_name,
    chatId: row.talk_id,
    type: "change",
  });
  router.replace("/home/chat/" + row.talk_id);
}

function openChatHisList() {
  emits("change-data", { chatTitle: "", chatId: -1, type: "change" });
  router.replace("/home/chat/history");
  if (oldTarget.value) {
    oldTarget.value.classList.remove("active");
  }
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
        if (oldTarget.value) {
          oldTarget.value.classList.remove("active");
        }
        break;
      case "new":
        delete newChat.type;
        tableData.value = [newChat, ...tableData.value];
        if (oldTarget.value) {
          oldTarget.value.classList.remove("active");
        }
        break;
      default:
        break;
    }
  }
);

async function deleteUserOk(chat) {
  await deleteChat({ talk_id: chat.talk_id + "" });
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
  getAiChatList();
});
</script>

<style>
.header-container {
  color: rgb(35, 35, 35);
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 40px;
  margin-top: 20px;
  padding-left: 15px;
  padding-right: 18px;
  border-top: 1px solid rgb(35, 35, 35, 0.1);
}

.infinite-list-wrapper {
  height: 62vh;
  padding: 5px;
}

.infinite-list-wrapper .list {
  padding: 0;
  margin: 0;
  list-style: none;
  font-size: 14px;
}

.infinite-list-wrapper .list-item {
  height: 45px;
  color: rgb(35, 35, 35);
}

.infinite-list-wrapper .list-item:hover,
.infinite-list-wrapper .list-item.active {
  background: rgb(233, 234, 236);
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

.el-popper[data-popper-placement^="bottom"] > .el-popper__arrow {
  top: 0 !important;
}

.el-dropdown-menu__item {
  border-radius: 6px;
  --el-dropdown-menuItem-hover-fill: rgb(35, 35, 35, 0.1);
  --el-dropdown-menuItem-hover-color: rgb(35, 35, 35);
  --el-text-color-regular: rgb(35, 35, 35);
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
  margin-top: 10px;
}

.last-msg {
  height: 20px;
  width: 20px;
  --el-loading-spinner-size: 18px;
  --el-color-primary: rgb(103, 103, 105);
}

:deep(.el-loading-spinner .path) {
  stroke-width: 4 !important;
}
</style>