<template>
  <div class="container">
    <div class="warper">
      <el-skeleton style="width: 43vw" :loading="openLoading" animated>
        <template #template>
          <el-skeleton-item
            variant="text"
            style="
              width: 40%;
              height: 45px;
              margin-right: 60%;
              margin-top: 20px;
            "
          />
          <el-skeleton-item
            variant="text"
            style="width: 50%; height: 30px; margin-top: 20px"
          />
          <el-skeleton-item
            variant="text"
            style="width: 40%; height: 45px; margin-left: 50%; margin-top: 20px"
          />
          <el-skeleton-item
            variant="text"
            style="width: 90%; height: 80px; margin-top: 20px"
          />
          <el-skeleton-item
            variant="text"
            style="width: 70%; height: 45px; margin-left: 20%; margin-top: 20px"
          />
          <el-skeleton-item
            variant="text"
            style="width: 90%; height: 240px; margin-top: 20px"
          />
          <el-skeleton-item
            variant="text"
            style="width: 50%; height: 45px; margin-left: 40%; margin-top: 20px"
          />
          <el-skeleton-item
            variant="text"
            style="width: 90%; height: 200px; margin-top: 20px"
          />
        </template>
        <template #default>
          <div class="header">
            <h1>{{ title }}</h1>
            <p>{{ shareTime }} • 内容由 AI 生成，不能完全保障真实</p>
          </div>
          <div class="content-body">
            <div
              v-for="(message, index) in messages"
              :key="index"
              class="message"
            >
              <div v-if="message.type === 'user'" class="user-message">
                <span>{{ message.content }}</span>
                <div class="tools">
                  <el-tooltip
                    class="box-item"
                    effect="light"
                    content="复制"
                    placement="top"
                  >
                    <i
                      @click="copyContent($event, message.content)"
                      class="fa-solid fa-copy"
                    ></i>
                  </el-tooltip>
                </div>
              </div>
              <div class="markdown-body" v-else>
                <div
                  class="inner"
                  v-html="markdwonToHTML(message.content)"
                ></div>
                <div class="tools">
                  <el-tooltip
                    class="box-item"
                    effect="light"
                    content="复制"
                    placement="top"
                  >
                    <i
                      @click="copyContent($event, message.content)"
                      class="fa-solid fa-copy"
                    ></i>
                  </el-tooltip>
                </div>
              </div>
            </div>
          </div>
        </template>
      </el-skeleton>
    </div>

    <div class="to-voa">
      <el-button @click="goHome" type="primary" :icon="ChatDotSquare" round
        >前往VoaTalk</el-button
      >
    </div>
  </div>
  <el-backtop :right="100" :bottom="100" />
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import "@/assets/css/github-markdown.css";
import "@/assets/css/hljs-github.css";
import "katex/dist/katex.min.css";
import { markdwonToHTML, addCopy } from "@/utils/render-html";
import { ChatDotSquare } from "@element-plus/icons-vue";
import router from "@/router";

import { getRedisChat } from "@/api/aiChat";

const routePath = useRoute();
const messages = ref([]);
const title = ref(null);
const shareTime = ref(null);
const openLoading = ref(false);

function goHome() {
  router.replace("/home/chat");
}

function copyContent(event, content) {
  navigator.clipboard
    .writeText(content)
    .then(() => {
      const oCopy = event.target;
      oCopy.className = "fas fa-check"; // 切换为成功图标
      oCopy.style.color = "#28a745"; // 成功颜色
      ElMessage.success("复制成功");

      setTimeout(() => {
        oCopy.className = "fa-solid fa-copy";
        oCopy.style.color = "rgb(117 116 116)"; // 恢复原样
      }, 1000); // 2 秒后恢复原样
    })
    .catch((err) => {
      console.error("无法复制代码:", err);
    });
}

onMounted(async function () {
  console.log(routePath.params.id);
  openLoading.value = true;

  try {
    const obj = await getRedisChat({ r_id: routePath.params.id });
    console.log(obj);
    messages.value = obj.data.talk_logs;
    title.value = obj.data.title;
    shareTime.value = obj.data.share_time;
  } catch (err) {
    console.log(err);
  }

  openLoading.value = false;

  nextTick(function () {
    addCopy();
  });
});
</script>

<style scoped>
.container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.warper {
  width: 43vw;
  background: var(--el-bg-color);
  margin: 40px 0px;
  border-radius: 24px;
  padding: 48px;
  box-sizing: border-box;
  min-height: calc(100vh - 80px);
}

.to-voa {
  position: fixed;
  top: 20px;
  right: 20px;
}

.warper .header h1 {
  font-size: 24px;
  font-weight: 600;
}

.warper .header p {
  font-size: 12px;
  color: var(--el-text-color-primary);
  border-bottom: 1px solid var(--el-text-color-primary);
  padding-bottom: 30px;
}

.markdown-body {
  padding: 10px;
  background-color: transparent;
}

.user-message {
  text-align: right;
  padding: 10px;
}

.user-message span {
  background: var(--el-border-color);
  color: var(--el-text-color-primary);
  padding: 8px;
  border-radius: 8px;
  display: inline-flex;
  white-space: pre-wrap;
  max-width: 26vw;
  text-align: left;
  margin-bottom: 10px;
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
</style>