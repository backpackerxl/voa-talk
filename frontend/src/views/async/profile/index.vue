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
    <el-form label-position="left" style="width: 330px">
      <el-form-item label="主题: " class="them-item">
        <el-dropdown>
          <el-button plain>
            <div class="me-icon">
              <span :class="them.icon"></span>
            </div>
            &nbsp;{{ them.label
            }}<el-icon class="el-icon--right"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item
                v-for="(item, index) in themList"
                :key="index"
                @click="changeThem(item)"
              >
                <div class="me-icon">
                  <span :class="item.icon"></span>
                </div>
                &nbsp;{{ item.label }}</el-dropdown-item
              >
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-form-item>
      <el-form-item label="昵称: " prop="nickName">
        <el-input
          v-model="welcomStr"
          placeholder="请输入新的昵称"
          clearable
          size="large"
        ></el-input>
      </el-form-item>
      <el-form-item label="邮箱: " prop="email">
        <div class="email-setting">
          <div>
            <el-tag size="large">{{
              userEmail !== "" ? userEmail : "绑定邮箱可获取平台资讯"
            }}</el-tag>
          </div>
          <div>
            <el-button plain :icon="Edit" @click="changeEmail">{{
              userEmail !== "" ? "更换" : "绑定"
            }}</el-button>
          </div>
        </div>
      </el-form-item>
      <el-form-item>
        <div class="button-group">
          <el-button
            size="large"
            type="primary"
            @click="saveUserInfo"
            :icon="Edit"
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
        v-if="isMob"
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
  <el-dialog
    v-model="editDialogVisible"
    title="修改邮箱号"
    width="380"
    align-center
  >
    <el-form
      :model="registerForm"
      :rules="rules"
      ref="registerFormRef"
      placeholder="请输入邮箱号"
    >
      <el-form-item label="邮箱号: " prop="email">
        <el-input size="large" v-model="registerForm.email" />
      </el-form-item>
      <el-form-item label="验证码: " prop="code">
        <el-input
          type="number"
          size="large"
          v-model="registerForm.code"
          placeholder="请输入验证码"
        >
          <template #suffix>
            <el-button
              class="get-code"
              :disabled="codeDisabled"
              @click="getEmailCode"
              plain
              >{{ emailCodeContent }}</el-button
            >
          </template>
        </el-input>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="editEmailOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog
    v-model="state.open"
    title="请拖动滑块完成验证"
    width="380"
    align-center
  >
    <Captcha ref="myCaptcha" @verify="verifyImg" />
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue";
import store from "@/store";
import {
  Plus,
  ChatDotSquare,
  ChatLineRound,
  Edit,
  ArrowDown,
} from "@element-plus/icons-vue";
const welcomStr = ref(store.state.app.nickName);
const userEmail = ref(store.state.app.userEmail);

const registerForm = ref({
  email: userEmail.value,
  code: "",
});

let state = reactive({
  open: false,
});

const editDialogVisible = ref(false);
import router from "@/router";
import { updateUser, sendEmailCodeApi, updateUserEmail } from "@/api/apiUser";
import { ElMessage } from "element-plus";
import { config } from "@/utils/config";
import { handleThem } from "@/utils/tools";
import device from "current-device";
import Captcha from "@/components/Captcha";

const avatarUrl = store.state.app.avatar;
const imageUrl = ref(avatarUrl);
const myCaptcha = ref(null);
const codeDisabled = ref(false);
const emailCodeContent = ref("获取验证码");
const reqCId = ref("-1");
const captchaCode = ref("-1");
const saveUrl = ref(avatarUrl.replace(config.BASE_URL, ""));
const checkThemId = ref(1);
const isMob = ref(!device.mobile());
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
const them = ref(JSON.parse(store.state.app.them));
const themList = ref([
  {
    them: "light",
    label: "浅色",
    icon: "icon theme-light",
  },
  {
    them: "dark",
    label: "深色",
    icon: "icon theme-dark",
  },
  {
    them: "os",
    label: "跟随系统",
    icon: "icon theme-os",
  },
]);
const emailRule = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

function changeThem(item) {
  handleThem(item);
  them.value = item;
  store.dispatch("app/setThem", JSON.stringify(item));
}

function verifyImg(obj) {
  if (obj.tag === true) {
    captchaCode.value = obj.token;
    sendEmailCode();
    state.open = false;
  } else {
    ElMessage.error("验证不通过");
  }
}

let countdown = 60;

function startCountdown() {
  const timer = setInterval(() => {
    countdown--;
    emailCodeContent.value = "重新发送 " + countdown + "s";

    if (countdown <= 0) {
      clearInterval(timer);
      emailCodeContent.value = "重新发送";
      codeDisabled.value = false;
    }
  }, 1000);
}

async function sendEmailCode() {
  const reqIdObj = await sendEmailCodeApi({
    nickName: welcomStr.value,
    email: registerForm.value.email,
    captcha_code: captchaCode.value,
  });
  reqCId.value = reqIdObj.data.reqId;
  // 实现倒计时
  codeDisabled.value = true;
  countdown = 60;
  startCountdown();
}

function getEmailCode() {
  if (emailRule.test(registerForm.value.email)) {
    state.open = true;
    myCaptcha.value && myCaptcha.value.init();
  } else {
    ElMessage.error("请填写正确的邮箱号");
  }
}

function changeEmail() {
  editDialogVisible.value = true;
}

const registerFormRef = ref(null);

function editEmailOk() {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      const resp = await updateUserEmail({
        reqId: reqCId.value,
        email: registerForm.value.email,
        verCode: registerForm.value.code,
      });
      if (resp.code === 200) {
        store.dispatch("app/setUserEmail", registerForm.value.email);
        userEmail.value = registerForm.value.email;
        ElMessage({
          message: "修改成功",
          type: "success",
        });
      } else {
        ElMessage.error("修改失败");
      }
      editDialogVisible.value = false;
    }
  });
}

const rules = {
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    {
      pattern: emailRule,
      type: "email",
      message: "邮箱格式不正确",
      trigger: ["blur", "change"],
    },
  ],
  code: [{ required: true, message: "请输入邮箱验证码", trigger: "blur" }],
};

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

let oldTag = ref(colorList.value[0].tag);

if (store.state.app.mainColor) {
  oldTag = ref(JSON.parse(store.state.app.mainColor).tag);
}

function selectColor(item) {
  checkThemId.value = item.id;
  // console.log(oldTag.value);
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
  document.documentElement.querySelector("title").innerText = "我的主页";
});
</script>

<style scoped>
.user-edit {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  height: calc(100vh - 120px);
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

.get-code {
  cursor: pointer;
  user-select: none;
  border: none;
  padding: 0;
  margin: 0;
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

.button-group .el-button {
  margin: 15px 0;
  width: 330px;
  border: none;
  font-size: 16px;
}

:deep(.el-input__wrapper) {
  transition: all 0.1s;
  border-radius: 6px !important;
  box-shadow: 0 0 0 3px var(--el-input-border-color) inset !important;
  background-color: transparent !important;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px var(--el-color-primary) inset !important;
}

:deep(.el-form-item.is-error .el-input__wrapper) {
  box-shadow: 0 0 0 3px var(--el-color-danger) inset !important;
}

.opt {
  display: flex;
  flex-direction: column;
}

.opt .el-button {
  width: 330px;
  margin: 10px 0;
  border: none;
  box-shadow: none;
}

.them-color {
  width: 330px;
  display: flex;
  flex-wrap: wrap;
}

.them-color .item {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  margin: 8px;
  cursor: pointer;
}

.them-color .item i {
  line-height: 50px;
  text-align: center;
  color: #fff;
  font-size: 26px;
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
  background: var(--w-e-textarea-border-color);
  height: 1px;
  width: 35%;
  top: 50%;
}

.opt p.them-text::before,
.opt p.them-text::after {
  width: 30%;
}

.opt p::before {
  left: 1px;
}
.opt p::after {
  right: 1px;
}

:deep(.them-item .el-form-item__content) {
  justify-content: end;
}

.me-icon .icon {
  width: 16px;
  height: 16px;
  display: block;
  background-color: var(--me-report-text-color);
}

.el-dropdown-menu__item:not(.is-disabled):focus .me-icon .icon,
.el-dropdown-menu__item:not(.is-disabled):hover .me-icon .icon,
.el-button:hover .me-icon .icon {
  background-color: var(--el-dropdown-menuItem-hover-color);
}

.me-icon .icon.theme-os {
  -webkit-mask-image: url("@/assets/images/theme-os.svg");
  mask-image: url("@/assets/images/theme-os.svg");
}

.me-icon .icon.theme-light {
  -webkit-mask-image: url("@/assets/images/theme-light.svg");
  mask-image: url("@/assets/images/theme-light.svg");
}

.me-icon .icon.theme-dark {
  -webkit-mask-image: url("@/assets/images/theme-dark.svg");
  mask-image: url("@/assets/images/theme-dark.svg");
}

.email-setting {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
</style>
