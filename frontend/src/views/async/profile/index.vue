<template>
  <div class="user-edit">
    <el-upload
      ref="uploadRef"
      :style="imageUrl ? 'display: none' : 'display: block'"
      :action="config.BASE_URL + '/upload'"
      list-type="picture-card"
      :headers="{ Token: store.state.app.authorization }"
      :on-success="handleSuccess"
      :before-upload="beforeUpload"
      :show-file-list="false"
      accept="image/png, image/jpeg"
    >
      <el-icon><Plus /></el-icon>
    </el-upload>
    <div @click="uploadImg" class="avater" v-if="imageUrl">
      <img
        :src="imageUrl"
        alt="Uploaded Image"
        style="max-width: 100%; margin-top: 20px"
      />
    </div>

    <h3 class="nick-name">{{ welcomStr }}</h3>
    <el-form label-position="right" label-width="60px" style="width: 400px">
      <el-form-item label="昵称" prop="nickName">
        <el-input
          v-model="welcomStr"
          placeholder="请输入邮箱，系统将发送修改密码的邮件"
          clearable
          size="large"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <div class="button-group">
          <el-button size="large" type="primary" @click="saveUserInfo"
            >保 存</el-button
          >
        </div>
      </el-form-item>
    </el-form>
    <div class="opt">
      <p>便捷操作</p>
      <el-button
        size="large"
        type="primary"
        @click="openChatHis"
        :icon="ChatLineRound"
        >查看历史对话</el-button
      >
      <el-button
        size="large"
        type="primary"
        @click="openNewChat"
        :icon="ChatDotSquare"
        >开启新对话</el-button
      >
      <el-button size="large" type="primary" @click="forgetPwd" :icon="Edit"
        >重置密码</el-button
      >
      <p class="them-text">自定义主题色</p>
      <div class="them-color">
        <el-tooltip
          v-for="item in colorList"
          :key="item.id"
          class="box-item"
          effect="light"
          :content="item.tip"
          :placement="item.place"
        >
          <div
            :class="checkThemId === item.id ? 'item checked' : 'item'"
            @click="selectColor(item)"
            :style="'background-color: ' + item.bgColor"
          >
            <i class="fas fa-check"></i>
          </div>
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import store from "@/store";
import {
  Delete,
  Download,
  Plus,
  ZoomIn,
  ChatDotSquare,
  ChatLineRound,
  Edit,
} from "@element-plus/icons-vue";
const welcomStr = ref(store.state.app.nickName);
import router from "@/router";
import { updateUser } from "@/api/apiUser";
import { ElMessage } from "element-plus";
import { config } from "@/utils/config";

const avatarUrl = store.state.app.avatar;
const imageUrl = ref(avatarUrl);
const saveUrl = ref(avatarUrl.replace(config.BASE_URL, ""));
const checkThemId = ref(1);
const colorList = ref([
  {
    id: 1,
    bgColor: "#4d6bfe",
    tip: "霓虹蓝",
    tag: null,
    place: "top",
  },
  {
    id: 2,
    bgColor: "#ff7625",
    tip: "岩力橙",
    tag: "cyan",
    place: "top",
  },
  {
    id: 3,
    bgColor: "#0052d9",
    tip: "皇家蓝",
    tag: "blue",
    place: "top",
  },
  {
    id: 4,
    bgColor: "#00A884",
    tip: "流光绿",
    tag: "green",
    place: "top",
  },
  {
    id: 5,
    bgColor: "#00b458",
    tip: "宝石绿",
    tag: "genblue",
    place: "top",
  },
  {
    id: 6,
    bgColor: "#06b3d3",
    tip: "海湾蓝",
    tag: "indigo",
    place: "bottom",
  },
  {
    id: 7,
    bgColor: "#9463f7",
    tip: "宇宙紫",
    tag: "purple",
    place: "bottom",
  },
  {
    id: 8,
    bgColor: "#ffb400",
    tip: "闪电黄",
    tag: "orange",
    place: "bottom",
  },
  {
    id: 9,
    bgColor: "#f74584",
    tip: "玫瑰红",
    tag: "mixedred",
    place: "bottom",
  },
  {
    id: 10,
    bgColor: "#fd0077",
    tip: "璀璨洋红",
    tag: "red",
    place: "bottom",
  },
]);

const uploadRef = ref(null);

function handleSuccess(response, file, fileList) {
  saveUrl.value = response.image_url;
  imageUrl.value = config.BASE_URL + response.image_url;
}

function uploadImg() {
  if (uploadRef.value) {
    const input = uploadRef.value.$el.querySelector('input[type="file"]');
    if (input) {
      input.click();
    }
  }
}

function beforeUpload(file) {
  const isJpgOrPng = file.type === "image/jpeg" || file.type === "image/png";
  if (!isJpgOrPng) {
    ElMessage.error("上传图片只能是 JPG 或者 PNG 格式!");
  }
  return isJpgOrPng;
}

function openNewChat() {
  router.replace("/home/chat");
}

function openChatHis() {
  router.replace("/home/chat/history");
}

function forgetPwd() {
  const route = router.resolve({
    name: "Forget",
  });
  window.open(route.href, "_blank");
}

async function saveUserInfo() {
  const resp = await updateUser({
    avatar: saveUrl.value,
    nick_name: welcomStr.value,
  });
  if (resp.code === 200) {
    store.dispatch("app/setNickName", welcomStr.value);
    store.dispatch("app/setAvatar", imageUrl.value);
    ElMessage({
      message: "修改成功",
      type: "success",
    });
  } else {
    ElMessage.error("修改失败");
  }
}

let oldTag = ref(JSON.parse(store.state.app.mainColor).tag);

function selectColor(item) {
  checkThemId.value = item.id;
  console.log(oldTag.value);
  if (oldTag.value) {
    document.documentElement.classList.remove(oldTag.value);
  }

  if (item.tag) {
    document.documentElement.classList.add(item.tag);
  }
  oldTag.value = item.tag;
  store.dispatch("app/setMainColor", JSON.stringify(item));
}

onMounted(function () {
  let colorObj = store.state.app.mainColor;
  if (colorObj) {
    checkThemId.value = JSON.parse(colorObj).id;
  }
});
</script>

<style scoped>
.user-edit {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

:deep(.el-upload.el-upload--picture-card),
:deep(.el-upload-list--picture-card .el-upload-list__item-actions),
:deep(.el-upload-list--picture-card .el-upload-list__item-thumbnail) {
  border-radius: 50% !important;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  border: none !important;
}

.nick-name {
  margin-top: 35px;
}

.avater {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
}

.avater:hover::after {
  content: "点击更换头像";
  position: absolute;
  font-size: 16px;
  color: #fff;
  width: inherit;
  height: inherit;
  top: 90px;
  left: 30px;
  background: transparent;
}

.avater:hover::before {
  position: absolute;
  top: 20px;
  left: 0;
  content: "";
  width: inherit;
  height: inherit;
  border-radius: 50%;
  background-color: rgb(0, 0, 0, 0.4);
}

.avater img {
  object-fit: cover;
  width: inherit;
  height: inherit;
  border-radius: 50%;
}

.button-group,
.el-input {
  width: 85%;
}

.button-group .el-button {
  margin: 15px 0;
  width: 100% !important;
  border: none;
  font-size: 16px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px !important;
  box-shadow: 0 0 0 4px var(--el-input-border-color);
  background-color: transparent !important;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 4px var(--el-color-primary) !important;
}

.opt {
  display: flex;
  flex-direction: column;
}

.opt .el-button {
  width: 280px;
  margin: 10px 0;
  border: none;
  box-shadow: none;
}

.them-color {
  width: 280px;
  display: flex;
  flex-wrap: wrap;
}

.them-color .item {
  width: 45px;
  height: 45px;
  border-radius: 4px;
  margin: 5px;
  cursor: pointer;
}

.them-color .item i {
  line-height: 45px;
  text-align: center;
  color: #fff;
  font-size: 24px;
  display: none;
}

.them-color .item.checked i {
  display: block;
}

.opt p {
  text-align: center;
  color: var(--el-text-color-primary);
  position: relative;
}

.opt p::before,
.opt p::after {
  position: absolute;
  content: "";
  background: var(--el-text-color-primary);
  height: 1px;
  width: 35%;
  top: 50%;
}

.opt p.them-text::before,
.opt p.them-text::after {
  width: 30%;
}

.opt p::before {
  left: 0;
}
.opt p::after {
  right: 0;
}
</style>
