<template>
  <div ref="chatPage" class="chat-page">
    <RightClickMenu ref="rightClickMenu" :menu-items="menuItems">
      <div class="chat-window">
        <div class="last-msg load-msg" v-loading="openLoading"></div>
        <div v-for="(message, index) in messages" :key="index"
          :class="index === messages.length - 1 ? 'message active' : 'message'">
          <!-- 自定义复选框 -->
          <div class="custom-checkbox" v-if="isShare">
            <input type="checkbox" :id="'msg-' + message.id" :value="message.id" v-model="checkList"
              class="checkbox-input" />
            <label :for="'msg-' + message.id" class="checkbox-label"></label>
          </div>
          <div v-if="message.type === 'user'" :class="{
            'user-message': true,
            selected: checkList.includes(message.id),
          }" @click="toggleCheckbox(message.id, $event)" @contextmenu.prevent="openMenu($event, message)">
            <div v-if="index === messages.length - 2">
              <div v-if="showEditInput" class="edit-warrap">
                <i @click="closeSend" class="fa-solid fa-xmark"></i>
                <el-input v-model="mContent" style="width: 100%" :autosize="{ minRows: 1, maxRows: 15 }"
                  class="re-input" type="textarea" />
                <el-button type="primary" @click="reSendMessage(message.id)" circle class="send-message active">
                  <i :class="{
                    'fa-solid fa-arrow-up': !changeIcon,
                    'fa-solid fa-square': changeIcon,
                  }"></i>
                </el-button>
              </div>
            </div>
            <span>{{ message.content }}</span>
            <div class="tools" v-if="!isShare">
              <el-tooltip class="box-item" effect="light" content="复制" placement="top" v-if="isMob">
                <i @click="copyContent($event, message.content)" class="fa-solid fa-copy"></i>
              </el-tooltip>
              <el-tooltip class="box-item" effect="light" content="编辑" placement="top"
                v-if="index === messages.length - 2">
                <i @click="editQue($event, message.content)" class="fa-solid fa-pen-to-square"></i>
              </el-tooltip>
              <el-tooltip class="box-item" effect="light" content="分享" placement="top" v-if="isMob">
                <i @click="share(message.id)" class="fa-solid fa-share"></i>
              </el-tooltip>
              <el-tooltip class="box-item" effect="light" content="删除" placement="top" v-if="isMob">
                <i @click="deleteChat(message.id)" class="fa-solid fa-trash"></i>
              </el-tooltip>
            </div>
          </div>
          <div :class="{
            'markdown-body': true,
            selected: checkList.includes(message.id),
          }" v-else @click="toggleCheckbox(message.id, $event)" @contextmenu.prevent="openMenu($event, message)">
            <el-tooltip class="box-item" effect="customized" content="对话不是一个完整对话，不能生成推荐问题" placement="top"
              v-if="message.pause_ask_stats === '1'">
              <div class="inner" v-html="markdwonToHTML(message.content, true)"></div>
            </el-tooltip>
            <div class="inner" v-html="markdwonToHTML(message.content, true)" v-else></div>
            <div class="tools" v-if="!isShare">
              <el-tooltip class="box-item" effect="light" content="复制" placement="top" v-if="isMob">
                <i @click="copyContent($event, message.content)" class="fa-solid fa-copy"></i>
              </el-tooltip>
              <el-tooltip class="box-item" effect="light" content="重新生成" placement="top"
                v-if="index === messages.length - 1">
                <el-dropdown @visible-change="handleVisibleChange" trigger="click">
                  <button class="drp-btn">
                    <i class="fa-solid fa-rotate-right"></i>
                  </button>
                  <template #dropdown>
                    <el-dropdown-menu :style="{
                      pointerEvents: isVisible ? 'auto' : 'none',
                    }">
                      <el-dropdown-item v-for="item in options" :key="item.value" @click="
                        rotateChat(
                          message.id,
                          messages[messages.length - 2].content,
                          item.value
                        )
                        ">{{ item.label }}</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </el-tooltip>
              <el-tooltip class="box-item" effect="light" content="分享" placement="top" v-if="isMob">
                <i @click="share(message.id)" class="fa-solid fa-share"></i>
              </el-tooltip>
              <el-tooltip class="box-item" effect="light" content="删除" placement="top" v-if="isMob">
                <i @click="deleteChat(message.id)" class="fa-solid fa-trash"></i>
              </el-tooltip>
            </div>
          </div>
        </div>
        <div class="container">
          <div ref="oOutPut" class="markdown-body now" v-html="markdwonToHTML(respStr, true)"></div>
          <div class="thinking" v-if="modelTokens !== 0">
            <p>
              回答用时: {{ thinkTime }}s, 消耗模型token数: {{ modelTokens }}
            </p>
          </div>
          <div ref="cursorElement" class="cursor"></div>
          <div class="last-msg" v-loading="loading"></div>
          <div :class="{
            'record-list active': changeIcon,
            'record-list': !changeIcon,
          }" v-if="!isShare">
            <div class="item" v-for="(record, index) in recordList" :key="index">
              <span @click="recordQue(record.content)">{{ record.content }}? <i
                  class="fa-solid fa-arrow-right"></i></span>
            </div>
          </div>
        </div>
        <div class="box-share" v-if="isShare">
          <MyBackTag v-if="ishowAd" :change-icon="changeIcon" @click="scrollTopBottom(true)" />
          <!-- 全选控制区域 -->
          <div class="select-controls">
            <div class="custom-checkbox">
              <input type="checkbox" id="select-all" v-model="isAllSelected" class="checkbox-input" />
              <label for="select-all" class="checkbox-label">全选</label>
            </div>
            <div>
              <el-button @click="noShare">取消分享</el-button>
              <el-button @click="copyLink" type="primary">复制链接</el-button>
            </div>
          </div>
        </div>
      </div>
    </RightClickMenu>

    <div class="input-container" :style="welcomeWord ? 'bottom:40%' : 'bottom: 20px'" v-if="!isShare">
      <div class="welcome" v-if="welcomeWord">
        <Logo />
        <h2>{{ welcomStr }}</h2>
      </div>
      <div class="input__inner_container">
        <MyBackTag v-if="ishowAd" :change-icon="changeIcon" @click="scrollTopBottom(true)" />
        <el-input v-model="newMessage" :autosize="{ minRows: 2, maxRows: 10 }" @keyup.enter.exact="sendMessage"
          @keydown.shift.enter="handleShiftEnter" placeholder="输入您的问题..." type="textarea" @input="chengQValue" />
        <div class="opt">
          <el-select v-model="modelId" placeholder="请选择模型" style="width: 150px" clearable>
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
          <el-button type="primary" @click="sendMessage" circle :disabled="disabledBtn" :class="{
            'send-message active': !disabledBtn,
            'send-message': disabledBtn,
          }">
            <i :class="{
              'fa-solid fa-arrow-up': !changeIcon,
              'fa-solid fa-square': changeIcon,
            }"></i>
          </el-button>
        </div>
      </div>
    </div>
  </div>
  <el-dialog v-model="centerDialogVisible" title="删除对话" width="380" align-center>
    <span>确定删除，对话内容将不可恢复</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteChatOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
  <el-drawer v-model="drawer" title="选取文本复制" :with-header="true" size="100%">
    <span class="select-content">{{ selectContent }}</span>
  </el-drawer>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, watch } from "vue";
import {
  AiChat,
  saveAiChat,
  saveAiChatTitle,
  aiOneChat,
  deleteOneChat,
  queryRecommend,
  shareChat,
} from "@/api/aiChat";
import { ApiModelList } from "@/api/modelConfig";
import { getGreeting, smoothScroll } from "@/utils/tools";
import { markdwonToHTML, addCopy, renderMermaid } from "@/utils/render-html";
import { useRoute } from "vue-router";
import store from "@/store";
import { ElMessage } from "element-plus";
import "@/assets/css/github-markdown.css";
import "@/assets/css/hljs-github.css";
import "katex/dist/katex.min.css";
import Logo from "@/components/Logo.vue";
import RightClickMenu from "@/components/RightClickMenu.vue";
import MyBackTag from "@/components/MyBackTag.vue";
import * as clipboard from "clipboard-polyfill";

const routePath = useRoute();

const welcomStr = ref(getGreeting() + "，" + store.state.app.nickName);

const messages = ref([]);

const newMessage = ref("");

const modelId = ref("");

const options = ref([]);

const disabledBtn = ref(true);

const respStr = ref("");

const chatId = ref(-1);

const loading = ref(false);

const openLoading = ref(false);

const welcomeWord = ref(false);

const oOutPut = ref(null);

const cursorElement = ref(null);

const changeIcon = ref(false);

const centerDialogVisible = ref(false);

const delChatId = ref(-1);

const recordList = ref([]);

const showEditInput = ref(false);

const mContent = ref("");

const chatPid = ref(null);

const isVisible = ref(false);

const checkList = ref([]);

const isShare = ref(false);

const modelTokens = ref(0);

const thinkTime = ref(0);

const chatPage = ref(null);

const isMob = ref(!device.mobile());

const rightClickMenu = ref(null);

const drawer = ref(false);

const selectContent = ref("");

const ishowAd = ref(false);

let oSpanC = null,
  isPuseAsk = false,
  lastScrollTop = 0,
  scrollUpDistance = 0,
  oDivTools = null;

function handleVisibleChange(visible) {
  isVisible.value = visible;
}

const menuItems = ref([
  {
    icon: "fa-solid fa-copy",
    label: "复制内容",
    classList: [],
    action: (data) => {
      clipboard.writeText(data.content).then(
        () => {
          ElMessage.success("复制成功");
        },
        () => {
          ElMessage.error("链接复制失败");
          console.log("error!");
        }
      );
    },
  },
  {
    icon: "fa-solid fa-share",
    label: "分享对话",
    classList: [],
    action: (data) => {
      isShare.value = true;
      checkList.value.push(data.id);
    },
  },
  {
    icon: "fa-solid fa-trash",
    label: "删除对话",
    classList: ["delete"],
    action: (data) => {
      deleteChat(data.id);
    },
  },
]);

if (!isMob.value) {
  menuItems.value.push({
    icon: "fa-regular fa-object-ungroup",
    label: "选取文字",
    classList: [],
    action: (data) => {
      selectContent.value = data.content;
      drawer.value = true;
    },
  });
}

function openMenu(event, message) {
  rightClickMenu.value &&
    rightClickMenu.value.handleContextMenu(event, message);
}

function toggleCheckbox(id) {
  const checkbox = document.getElementById(`msg-${id}`);
  if (checkbox) {
    checkbox.checked = !checkbox.checked;

    // 更新v-model绑定的值
    const index = checkList.value.indexOf(id);
    if (checkbox.checked && index === -1) {
      checkList.value.push(id);
    } else if (!checkbox.checked && index !== -1) {
      checkList.value.splice(index, 1);
    }
  }
}

function share(id) {
  isShare.value = true;
  toggleCheckbox(id);
}

// 全选计算属性
const isAllSelected = computed({
  get() {
    return (
      messages.value.length > 0 &&
      checkList.value.length === messages.value.length / 2
    );
  },
  set(value) {
    checkList.value = value
      ? [...new Set(messages.value.map((msg) => msg.id))]
      : [];
  },
});

function noShare() {
  isShare.value = false;
  checkList.value = [];
}

async function copyLink() {
  if (checkList.value.length <= 0) {
    ElMessage.warning("请选择要分享的对话");
    return;
  }
  let params = {
    ids: checkList.value,
  };
  const obj = await shareChat(params);
  let req_url = window.location.origin;
  clipboard.writeText(req_url + "/thread/" + obj.data.share_id).then(
    () => {
      ElMessage.success("链接复制成功");
    },
    () => {
      ElMessage.error("链接复制失败");
      console.error("无法复制链接:", err);
    }
  );
  noShare();
}

watch(
  () => routePath,
  async (newRoute, oldRoute) => {
    if (newRoute.params.id) {
      welcomeWord.value = false;
      chatId.value = Number(newRoute.params.id);
      await getOneChatData();
      const obj = await queryRecommend({ talk_id: chatId.value });
      recordList.value = obj.data.reco_list;
      modelTokens.value = 0;
      nextTick(function () {
        // 自动滚动到最新消息位置
        renderMermaid();
        scrollTopBottom();
      });
    } else {
      chatId.value = -1;
      messages.value = [];
      welcomeWord.value = true;
      recordList.value = [];
      modelTokens.value = 0;
    }
  },
  { deep: true }
);

async function getOneChatData() {
  openLoading.value = true;
  let obj = await aiOneChat({ talk_id: chatId.value });
  messages.value = obj.data;
  openLoading.value = false;
}

function chengQValue() {
  newMessage.value = newMessage.value.replace(/[\r\n]+$/, "");
  disabledBtn.value = newMessage.value.trim() === "";
}

function deleteChatOk() {
  deleteOneChat({ id: delChatId.value })
    .then((res) => {
      recordList.value = res.data.reco_list;
    })
    .catch((err) => {
      console.log(err);
    });
  messages.value = messages.value.filter((item) => item.id !== delChatId.value);
  centerDialogVisible.value = false;
}

function deleteChat(id) {
  centerDialogVisible.value = true;
  delChatId.value = id;
}

// 遍历子节点找到合适的文本节点和偏移量
function findTextNodeAndOffset(node) {
  if (node) {
    for (let i = node.childNodes.length - 1; i >= 0; i--) {
      let childNode = node.childNodes[i];
      if (
        childNode.nodeType === Node.TEXT_NODE &&
        /\S/.test(childNode.nodeValue)
      ) {
        childNode.nodeValue = childNode.nodeValue.replace(/\s+$/, "");
        return childNode;
      } else if (childNode.nodeType === Node.ELEMENT_NODE) {
        const result = findTextNodeAndOffset(childNode);
        if (result) {
          return result;
        }
      }
    }
  }
  return null;
}

function updateCursorPosition() {
  let currentNode = oOutPut.value;
  if (!currentNode) {
    return;
  }
  const result = findTextNodeAndOffset(currentNode);
  const text = document.createTextNode("\u200b");
  if (!result) {
    currentNode.appendChild(text);
  } else {
    result.parentElement.appendChild(text);
  }

  const range = document.createRange();
  range.setStart(text, 0);
  range.setEnd(text, 0);
  const rect = range.getBoundingClientRect();

  const containerRect = currentNode.getBoundingClientRect();
  let x = rect.left - containerRect.left + 12;
  cursorElement.value.style.left = x + "px";
  cursorElement.value.style.top = rect.top - containerRect.top + 8 + "px";
  if (containerRect.width < x) {
    cursorElement.value.style.display = "none";
  } else {
    cursorElement.value.style.display = "block";
  }
  text.remove();
}

function recordQue(content) {
  newMessage.value = content;
  sendMessage();
}

function editQue(node, content) {
  showEditInput.value = true;
  mContent.value = content;
  oSpanC = node.target.parentNode.previousElementSibling;
  oDivTools = node.target.parentNode;
  oDivTools.style.opacity = "0";
  oSpanC.style.display = "none";
}

function closeSend() {
  showEditInput.value = false;
  oDivTools.style = "";
  oSpanC.style = "";
}

function reSendMessage(id) {
  if (!id) {
    return;
  }
  delChatId.value = id;
  chatPid.value = id;
  delLastMsg();
  closeSend();
  newMessage.value = mContent.value;
  sendMessage();
}

function delLastMsg() {
  messages.value.pop();
  messages.value.pop();
}

function rotateChat(id, que, optId) {
  if (!id) {
    return;
  }
  chatPid.value = id;
  modelId.value = optId;
  newMessage.value = que;
  delLastMsg();
  sendMessage();
}

function copyContent(event, content) {
  clipboard.writeText(content).then(
    () => {
      const oCopy = event.target;
      oCopy.className = "fas fa-check"; // 切换为成功图标
      oCopy.style.color = "#28a745"; // 成功颜色
      ElMessage.success("复制成功");

      setTimeout(() => {
        oCopy.className = "fa-solid fa-copy";
        oCopy.style.color = "rgb(117 116 116)"; // 恢复原样
      }, 1000); // 2 秒后恢复原样
    },
    () => {
      ElMessage.error("链接复制失败");
      console.log("error!");
    }
  );
}

function handleShiftEnter(e) {
  e.preventDefault();
  newMessage.value = newMessage.value + "\n";
}

const sendMessage = async () => {
  if (changeIcon.value) {
    isPuseAsk = true;
  }
  const firstCharIndex = newMessage.value.search(/[^\s]/);
  const isValid =
    firstCharIndex !== -1 && firstCharIndex < newMessage.value.length;
  if (!isValid) {
    return;
  }
  changeIcon.value = true;
  if (newMessage.value.trim() !== "") {
    respStr.value = "";
    welcomeWord.value = false;
    messages.value.push({ type: "user", content: newMessage.value });

    const userInput = newMessage.value;
    newMessage.value = "";
    modelTokens.value = 0;

    // console.log(userInput, modelId.value);

    let params = {
      user_input: userInput,
      model_id: modelId.value,
      session_id: chatId.value,
    };
    loading.value = true;

    const resp = await AiChat(params);

    if (resp.code === 500) {
      ElMessage.error("当前模型不可用，请切换其他模型或稍后重试！");
      return;
    }

    loading.value = false;

    // 记录回答时间
    let startThink = Date.now();
    const reader = resp.body.getReader();
    const textDecoder = new TextDecoder("utf-8");
    // 处理可能的分块数据
    while (1) {
      const { value, done: isDone } = await reader.read();
      if (isDone || isPuseAsk) {
        break;
      }
      if (value) {
        disabledBtn.value = false;
        const chunk = textDecoder.decode(value, { stream: true });
        const messages = chunk.split("\n\n");
        messages.forEach((message) => {
          if (message.startsWith("data: ")) {
            const cleanMessage = message.replace("data: ", "");
            const data = JSON.parse(cleanMessage);
            if (chatId.value === -1) {
              chatId.value = data.session_id;
              saveAiChatTitle({
                talk_id: chatId.value,
                user_input: userInput,
                model_id: modelId.value,
              })
                .then((obj) => {
                  chatId.value = obj.data.id;
                  store.dispatch("app/setSliderData", {
                    talk_id: obj.data.id,
                    talk_name: obj.data.title,
                    type: "new",
                  });
                })
                .catch((err) => {
                  console.log(err);
                });
            }
            respStr.value += data.content;
            nextTick(function () {
              updateCursorPosition();
              // 自动滚动到最新消息位置
              if (!ishowAd.value && chatPage.value) {
                const chatView = chatPage.value;
                chatView.scrollTo({
                  top: chatView.scrollHeight,
                });
              }
            });
          }
        });
      }
    }
    let tempValue = respStr.value;
    respStr.value = "";

    messages.value.push({
      type: "bot",
      content: tempValue,
      pause_ask_stats: !isPuseAsk ? "0" : "1",
    });

    nextTick(function () {
      // 记录回答结束时间
      let endThink = Date.now();
      thinkTime.value = (endThink - startThink) / 1000;
      cursorElement.value.style.display = "none";
      changeIcon.value = false;
      disabledBtn.value = true;
      // 自动滚动到最新消息位置
      renderMermaid();
      if (!ishowAd.value) {
        scrollTopBottom();
      }
    });

    if (chatId.value !== -1) {
      recordList.value = [];
      loading.value = true;
      const obj = await saveAiChat({
        id: chatPid.value,
        model_id: modelId.value,
        talk_id: chatId.value,
        resp_content: tempValue,
        req_content: userInput,
        pause_ask_stats: !isPuseAsk ? "0" : "1",
      });
      loading.value = false;
      const cId = obj.data.chat_id;
      modelTokens.value = obj.data.tokens;
      isPuseAsk = false; // 复位
      let lastIdx = messages.value.length - 1;
      chatPid.value = null;
      messages.value[lastIdx].id = cId;
      messages.value[lastIdx - 1].id = cId;
      recordList.value = obj.data.reco_list;
      nextTick(function () {
        // 自动滚动到最新消息位置
        renderMermaid();
        if (!ishowAd.value) {
          scrollTopBottom();
        }
      });
    }
  }
};

function scrollHanlde() {
  const currentScrollTop = chatPage.value.scrollTop;

  if (
    currentScrollTop + chatPage.value.clientHeight >=
    chatPage.value.scrollHeight - 1
  ) {
    ishowAd.value = false;
    return;
  }

  // 计算滚动距离和方向
  const scrollDelta = lastScrollTop - currentScrollTop;

  if (scrollDelta > 0) {
    // 向上滚动：累加距离
    scrollUpDistance += scrollDelta;
  } else {
    // 向下滚动：重置距离
    scrollUpDistance = 0;
  }

  // 判断是否向上滚动超过10px
  if (scrollUpDistance >= 10) {
    ishowAd.value = true;
  }

  // 更新上次滚动位置
  lastScrollTop = currentScrollTop;
}

onMounted(async () => {
  if (routePath && routePath.params.id) {
    welcomeWord.value = false;
    chatId.value = Number(routePath.params.id);
    const obj = await queryRecommend({ talk_id: chatId.value });
    recordList.value = obj.data.reco_list;
    await getOneChatData();
  } else {
    chatId.value = -1;
    messages.value = [];
    welcomeWord.value = true;
  }
  // 加载下拉框
  ApiModelList({
    search_criteria: '{"sort": {"field": "sort", "order": "desc"}}',
  })
    .then((res) => {
      if (res.data && res.data instanceof Array) {
        options.value = res.data.map((data) => {
          return {
            value: data.id,
            label: data.name,
          };
        });
        modelId.value = options.value[0].value;
      }
    })
    .catch((error) => {
      console.error("Failed to load model config:", error);
    });
  nextTick(function () {
    renderMermaid();
    addCopy(chatPage.value);
    chatPage.value.addEventListener("scroll", scrollHanlde);
    // 自动滚动到最新消息位置
    scrollTopBottom();
  });
});

function scrollTopBottom(animation = false) {
  ishowAd.value = false;
  if (chatPage.value) {
    const chatView = chatPage.value;
    if (animation) {
      smoothScroll(chatView, chatView.scrollHeight, function () {
        lastScrollTop = 0;
        scrollUpDistance = 0;
      });
    } else {
      chatView.scrollTop = chatView.scrollHeight;
      lastScrollTop = 0;
      scrollUpDistance = 0;
    }
  }
}
</script>

<style scoped>
.chat-page {
  display: flex;
  justify-content: center;
  overflow: auto;
  overflow-x: hidden;
  height: calc(100vh - 190px);
  margin: 0 2px;
  scrollbar-gutter: stable both-edges;
}

.el-skeleton {
  width: 48vw;
}

.chat-window {
  width: 48vw;
  transition: all 0.1s;
}

.chat-window .last-msg {
  height: 20px;
  width: 20px;
  --el-loading-spinner-size: 18px;
}

.chat-window .last-msg.load-msg {
  position: sticky;
  top: 0px;
  left: 50%;
  transform: translateX(50%);
  z-index: 2;
}

:deep(.el-loading-mask) {
  background-color: transparent !important;
}

:deep(.el-loading-spinner .path) {
  stroke-width: 4 !important;
}

.message .selected {
  background: var(--el-color-info-light-8);
  border-radius: 5px;
}

.markdown-body {
  padding: 10px;
  background-color: transparent;
}

.markdown-body.now {
  padding: 0px 10px;
}

.user-message {
  text-align: right;
  padding: 10px;
}

.user-message span {
  background: var(--me-bg-color);
  color: var(--el-text-color-primary);
  padding: 8px;
  border-radius: 8px;
  display: inline-flex;
  white-space: pre-wrap;
  overflow-x: auto;
  max-width: 26vw;
  text-align: left;
  margin-bottom: 10px;
}

.input-container {
  width: 48vw;
  position: fixed;
}

.input-container .welcome {
  text-align: center;
}

.input-container .welcome h2 {
  font-size: 18px;
  font-weight: 600;
}

.input__inner_container {
  padding: 10px;
  box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.12);
  border-radius: 10px;
  background: var(--el-bg-color);
  position: relative;
}

.input-container :deep(.el-textarea__inner) {
  border: none !important;
  box-shadow: none !important;
  resize: none;
  font-size: 16px;
  line-height: 1.5;
  padding: 0;
  background-color: transparent;
  caret-color: var(--el-color-primary);
}

.input-container :deep(.el-textarea__inner.is-focus) {
  border-radius: none !important;
  box-shadow: none !important;
  resize: none;
}

.opt {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

:deep(.el-select__wrapper) {
  border-radius: 75px;
  background-color: transparent;
}

.container {
  position: relative;
  padding: 0px 10px;
  margin-bottom: 180px;
}

.container .thinking {
  font-size: 14px;
  color: var(--el-color-info);
}

.container .cursor {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--el-text-color-primary);
  animation: blink 0.8s infinite;
  display: none;
}

.send-message {
  border: none;
  font-size: 16px;
}

.send-message i.fa-square {
  font-size: 12px;
}

@keyframes blink {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0;
  }
}

.record-list {
  display: block;
  padding-bottom: 10px;
}

.record-list.active {
  display: none;
}

.record-list .item {
  margin-bottom: 20px;
}

.record-list .item span {
  padding: 8px;
  background: var(--me-bg-color);
  border-radius: 8px;
  color: var(--el-text-color-primary);
  cursor: pointer;
  font-size: 14px;
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
}

.record-list span i {
  font-size: 12px;
  margin-left: 10px;
}

.message .tools {
  height: 30px;
  line-height: 30px;
  color: var(--el-text-color-regular);
  opacity: 0;
}

.tools i.fa-trash {
  color: rgb(255, 59, 48);
}

.tools i.fa-trash:hover {
  background: rgb(255, 59, 48, 0.1);
}

.context-menu-item.delete {
  color: rgb(255, 59, 48) !important;
}

.context-menu-item.delete:hover {
  background-color: rgb(255, 59, 48, 0.1) !important;
  color: rgb(255, 59, 48) !important;
}

.message:hover .tools,
.message.active .tools {
  opacity: 1;
}

.markdown-body .tools i {
  margin-right: 5px;
}

.user-message .tools i {
  margin-left: 5px;
}

.user-message .tools i,
.markdown-body .tools i {
  padding: 6px;
  cursor: pointer;
}

.tools i:hover {
  padding: 6px;
  background: rgb(117, 116, 116, 0.1);
  border-radius: 4px;
}

.edit-warrap {
  display: flex;
  align-items: center;
  min-height: 37px;
}

.edit-warrap .fa-xmark {
  font-size: 18px;
  color: var(--el-text-color-regular);
  cursor: pointer;
}

.edit-warrap .fa-xmark:hover {
  color: var(--el-text-color-primary);
}

.edit-warrap .re-input {
  margin: 0 10px;
}

.edit-warrap :deep(.el-textarea__inner) {
  border-radius: 6px !important;
  box-shadow: 0 0 0 2px var(--el-color-primary) inset !important;
  background-color: var(--el-bg-color);
  caret-color: var(--el-color-primary);
  resize: none;
}

.edit-warrap :deep(.el-textarea__inner.is-focus) {
  border-radius: 6px !important;
  box-shadow: 0 0 0 2px var(--el-color-primary) inset !important;
  resize: none;
}

.drp-btn {
  padding: 0;
  border: none;
  background: transparent;
  color: var(--el-text-color-regular);
  font-size: 16px;
}

.box-share {
  width: 43vw;
  height: 45px;
  position: fixed;
  bottom: 0;
}

.chat-window .message input[type="checkbox"] {
  transform: scale(1.2);
}

.box-share .select-controls input[type="checkbox"] {
  transform: scale(1.2);
}

.box-share .select-controls {
  font-size: 14px;
  color: var(--el-text-color-primary);
  user-select: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.select-content {
  display: inline-flex;
  white-space: pre-wrap;
  text-align: left;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
  user-select: text;
}

:deep(.el-button.is-circle) {
  padding: 10px;
}

@media (max-width: 1024px) {
  .chat-window {
    width: 70vw;
  }

  .input-container {
    width: 70vw;
  }

  .box-share {
    width: 70vw;
  }

  .el-skeleton {
    width: 70vw;
  }

  .user-message span {
    max-width: 54vw;
  }
}

@media (max-width: 768px) {
  .chat-window {
    width: 95vw;
  }

  .chat-page {
    height: calc(100vh - 200px);
  }

  .input-container {
    width: 90vw;
  }

  .box-share {
    width: 95vw;
  }

  .el-skeleton {
    width: 95vw;
  }

  .message .tools {
    opacity: 1;
  }

  .user-message span {
    max-width: 70vw;
  }

  .message .tools {
    font-size: 18px;
  }
}
</style>