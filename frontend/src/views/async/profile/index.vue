<template>
  <div class="user-edit">
    <el-upload ref="uploadRef" :style="imageUrl ? 'display: none' : 'display: block'"
      :action="config.BASE_URL + '/upload'" list-type="picture-card" :headers="{ Token: store.state.app.authorization }"
      :on-success="handleSuccess" :before-upload="beforeUpload" :show-file-list="false" accept="image/png, image/jpeg">
      <el-icon>
        <Plus />
      </el-icon>
    </el-upload>
    <div @click="uploadImg" class="avater" v-if="imageUrl">
      <img :src="imageUrl" alt="Uploaded Image" style="max-width: 100%; margin-top: 20px" />
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
            }}<el-icon class="el-icon--right">
              <ArrowDown />
            </el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-for="(item, index) in themList" :key="index" @click="changeThem(item)">
                <div class="me-icon">
                  <span :class="item.icon"></span>
                </div>
                &nbsp;{{ item.label }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-form-item>
      <el-form-item label="昵称: " prop="nickName">
        <el-input v-model="welcomStr" placeholder="请输入新的昵称" clearable size="large"></el-input>
      </el-form-item>
      <el-form-item label="邮箱: " prop="email">
        <div class="email-setting">
          <div>
            <el-tag size="large">{{
              userEmail !== "" ? userEmail : "绑定邮箱才能重置密码哦"
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
          <el-button size="large" type="primary" @click="saveUserInfo" :icon="Edit">保 存</el-button>
        </div>
      </el-form-item>
    </el-form>
    <div class="opt">
      <p>便捷操作</p>
      <div v-if="isSupportBiometric">
        <el-button size="large" type="primary" @click="noKeyLogin" :icon="Key" v-if="isNoKeyLogin">开启{{ biometricType
        }}登录</el-button>
        <el-button size="large" type="primary" @click="closeKeyLogin" :icon="Key" v-else>关闭{{ biometricType
        }}登录</el-button>
      </div>
      <el-button size="large" type="primary" @click="forgetPwd" :icon="Edit">更换密码</el-button>
      <div v-if="isMob && loginType === 'voatalk'">
        <el-button size="large" type="primary" @click="linkQQ" :icon="Link" v-if="clickQQFlow !== 0">{{
          qqActionTxt[clickQQFlow]
        }}</el-button>
      </div>
      <div v-if="isMob && loginType === 'voatalk'">
        <el-button size="large" type="primary" @click="linkGitHub" :icon="Link" v-if="clickGitHubFlow !== 0">{{
          githubActionTxt[clickGitHubFlow]
        }}</el-button>
      </div>
      <p class="them-text">自定义主题色</p>
      <div class="them-color">
        <el-tooltip v-for="item in colorList" :key="item.id" class="box-item" effect="light" :content="item.tip"
          :placement="item.place">
          <div :class="checkThemId === item.id ? 'item checked' : 'item'" @click="selectColor(item)"
            :style="'background-color: ' + item.bgColor">
            <i class="fas fa-check"></i>
          </div>
        </el-tooltip>
      </div>
    </div>
  </div>
  <el-dialog v-model="editDialogVisible" title="修改邮箱号" width="380" align-center>
    <el-form :model="registerForm" :rules="rules" ref="registerFormRef" placeholder="请输入邮箱号">
      <el-form-item label="邮箱号: " prop="email">
        <el-input size="large" v-model="registerForm.email" />
      </el-form-item>
      <el-form-item label="验证码: " prop="code">
        <el-input type="number" size="large" v-model="registerForm.code" placeholder="请输入验证码">
          <template #suffix>
            <el-button class="get-code" :disabled="codeDisabled" @click="getEmailCode" plain>{{ emailCodeContent
            }}</el-button>
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

  <el-dialog v-model="bindAccountDialogVisible" width="380" :show-close="false" align-center>
    <div class="logintext">
      <img :src="userAvatarUrl ? userAvatarUrl : avater" alt="头像" class="user-avatar" />
      <h4 class="user-name-txt">关联：{{ userNameTxt }} 账号</h4>
    </div>
    <div>
      <p></p>
      <el-tag type="warning" class="bind-warning">注意：关联号后，下面的对话内容将合并到当前登录账号下</el-tag>
      <el-table v-loading="state.loading" :data="tableData" border stripe style="width: 360px">
        <el-table-column fixed prop="talk_name" label="对话名称" width="360" />
      </el-table>
      <div class="me-pagination">
        <span>共 {{ tableCount }} 条</span>
        <el-pagination layout="prev, pager, next" :page-size="pageSize" :total="tableCount"
          @current-change="pageQuery" />
      </div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="cancelBindAccount">取消</el-button>
        <el-button type="primary" @click="bindAccount"> 关联 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue";
import store from "@/store";
import {
  Plus,
  Link,
  Key,
  Edit,
  ArrowDown,
} from "@element-plus/icons-vue";
const welcomStr = ref(store.state.app.nickName);
const userEmail = ref("");
const emailValue = store.state.app.userEmail;
if (emailValue !== "null" && emailValue !== "") {
  userEmail.value = emailValue;
}

const registerForm = ref({
  email: userEmail.value,
  code: "",
});

const editDialogVisible = ref(false);
import router from "@/router";
import { updateUser, sendEmailCodeApi, updateUserEmail } from "@/api/apiUser";
import { getOtherUserChatList, linkOtherUser, noLinkOtherUser } from "@/api/aiChat";
import { arrayBufferToBase64Url, base64UrlToArrayBuffer } from "@/utils/webAuthnHelper";
import { checkBiometricSupport } from "@/utils/webAuthn";
import { loginBegin, loginComplete } from "@/api/twoFAuth";
import { ElMessage } from "element-plus";
import { config } from "@/utils/config";
import { handleThem } from "@/utils/tools";
import device from "current-device";
import avater from "@/assets/images/avater.png";
const userNameTxt = ref('');
const userAvatarUrl = ref('');

const avatarUrl = store.state.app.avatar;
const loginType = store.state.app.loginType;
const imageUrl = ref(avatarUrl);
const codeDisabled = ref(false);
const emailCodeContent = ref("获取验证码");
const saveUrl = ref(config.BASE_URL);
const checkThemId = ref(1);
const isMob = ref(!device.mobile());
const isSupportBiometric = ref(false);
const isNoKeyLogin = ref(true);
const biometricType = ref('');
const bindAccountDialogVisible = ref(false);
const tableData = ref([]);
const tableCount = ref(0);
// 当前页码
const currentPage = ref(1);
// 每页显示数量
const pageSize = ref(6);

let state = reactive({
  loading: false,
});

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

let pcOrMobile = device.mobile() ? "mobile" : "pc";

const appId = "102796804";
const redirectUri = encodeURIComponent("https://www.voatalk.online/others/handle");
const stateF = "qqLogin"; // 用于防止攻击
const scope = "get_user_info"; // 所需权限

const qqLoginUrl = ref(
  `https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=${appId}&redirect_uri=${redirectUri}&state=${stateF}&scope=${scope}&display=${pcOrMobile}`
);

const githubClientId = "Ov23liTrl7t8g4EZP3j7";
const githubStateF = "githubLogin"; // 用于防止攻击
const gitHubScope = "user"; // 所需权限


const githubLoginUrl = ref(
  `https://github.com/login/oauth/authorize?client_id=${githubClientId}&redirect_uri=${redirectUri}&state=${githubStateF}&scope=${gitHubScope}`
);


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
  try {
    let resp = await sendEmailCodeApi({
      email: registerForm.value.email
    });
    if (resp.code === 200) {
      // 实现倒计时
      codeDisabled.value = true;
      countdown = 60;
      startCountdown();
      ElMessage({
        message: "验证码发送成功",
        type: "success",
      });
    }
  } catch (error) {
    console.error(error);
  }
}

function getEmailCode() {
  if (emailRule.test(registerForm.value.email)) {
    sendEmailCode();
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
      try {
        const resp = await updateUserEmail({
          email: registerForm.value.email,
          verCode: registerForm.value.code,
        });
        if (resp.code === 200) {
          // 这里可以添加实际的登出逻辑，比如清除 token 或者重定向到登录页面
          store.dispatch("app/clearAvatar");
          store.dispatch("app/clearAuthorization");
          store.dispatch("app/clearUserRole");
          store.dispatch("app/clearNickName");
          store.dispatch("app/clearUserName");
          store.dispatch("app/clearUserEmail");
          store.dispatch("app/clearLoginType");
          ElMessage({
            message: "修改成功",
            type: "success",
          });
          // 重定向到根路径
          router.push("/");
        } else {
          ElMessage.error("修改失败!");
        }
        editDialogVisible.value = false;
      } catch (error) {
        console.error(error);
      }
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
  saveUrl.value = saveUrl.value + response.image_url;
  imageUrl.value = saveUrl.value;
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

const qqActionTxt = {
  1: '关联QQ账号',
  2: '继续关联QQ账号',
  3: '解除关联QQ账号',
}

const clickQQFlow = ref(+store.state.app.bindQQ)

const githubActionTxt = {
  1: '关联GitHub账号',
  2: '继续关联GitHub账号',
  3: '解除关联GitHub账号',
}

const clickGitHubFlow = ref(+store.state.app.bindGitHub);

function cancelBindAccount() {
  store.dispatch("app/clearBindOtherAccount");
  if (clickQQFlow.value === 2) {
    clickQQFlow.value = 1;
  }

  if (clickGitHubFlow.value === 2) {
    clickGitHubFlow.value = 1;
  }
  bindAccountDialogVisible.value = false;
}

async function bindAccount() {
  try {
    if (clickQQFlow.value === 2) {
      try {
        const resp = await linkOtherUser({
          bindOtherAccount: store.state.app.bindOtherAccount,
          state: '1'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "关联成功",
            type: "success",
          });
          store.dispatch("app/setBindQQ", 3);
          clickQQFlow.value = 3;
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (clickGitHubFlow.value === 2) {
      try {
        const resp = await linkOtherUser({
          bindOtherAccount: store.state.app.bindOtherAccount,
          state: '2'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "关联成功",
            type: "success",
          });
          clickGitHubFlow.value = 3;
        }
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    if (clickQQFlow.value === 2) {
      clickQQFlow.value = 1;
    }

    if (clickGitHubFlow.value === 2) {
      clickGitHubFlow.value = 1;
    }
    console.error("Failed to bind account:", error);
  }
  store.dispatch("app/clearBindOtherAccount");
  bindAccountDialogVisible.value = false;
}

const pageQuery = (page) => {
  currentPage.value = page;
  fetchChatHisData();
};

async function fetchChatHisData() {
  try {
    state.loading = true; // 请求开始时设置为true
    const params = {
      pageSize: pageSize.value,
      pageIndex: currentPage.value,
      bindOtherAccount: store.state.app.bindOtherAccount,
      search_criteria: '{"sort": {"field": "create_date", "order": "desc"}}',
    };
    const response = await getOtherUserChatList(params);
    if (response.code === 200) {
      userNameTxt.value = response.data.other_username;
      userAvatarUrl.value = response.data.other_avatar;
      tableData.value = response.data.list.records;
      tableCount.value = response.data.list.total_count;
      state.loading = false; // 请求开始时设置为true
    }
  } catch (error) {
    console.error(error);
  }
}


async function linkQQ() {
  switch (clickQQFlow.value) {
    case 1:
      // console.log('关联QQ账号');
      store.dispatch("app/setBindOtherAccount", 'qq_' + store.state.app.userName + '_' + new Date().getTime());
      window.open(
        qqLoginUrl.value, // 要打开的URL（本地页面/远程链接均可）
        '关联QQ账号',       // 窗口名称（可用于复用窗口）
        'width=800,height=600,left=100,top=100' // 窗口特征（尺寸、位置等）
      );
      clickQQFlow.value = 2;
      break;
    case 2:
      await fetchChatHisData();
      bindAccountDialogVisible.value = true;
      break;
    case 3:
      // console.log('解除关联QQ账号');
      try {
        const resp = await noLinkOtherUser({
          state: '1'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "解除关联成功",
            type: "success",
          });
          store.dispatch("app/setBindQQ", 1);
          clickQQFlow.value = 1;
        }
      } catch (error) {
        console.error(error);
      }
      break;
    default:
      break;
  }
}

async function linkGitHub() {
  switch (clickGitHubFlow.value) {
    case 1:
      // console.log('关联GitHub账号');
      store.dispatch("app/setBindOtherAccount", 'github_' + store.state.app.userName + '_' + new Date().getTime());
      window.open(
        githubLoginUrl.value, // 要打开的URL（本地页面/远程链接均可）
        '关联GitHub账号',       // 窗口名称（可用于复用窗口）
        'width=800,height=600,left=100,top=100' // 窗口特征（尺寸、位置等）
      );
      clickGitHubFlow.value = 2;
      break;
    case 2:
      await fetchChatHisData();
      bindAccountDialogVisible.value = true;
      break;
    case 3:
      // console.log('解除关联GitHub账号');
      try {
        const resp = await noLinkOtherUser({
          state: '2'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "解除关联成功",
            type: "success",
          });
          store.dispatch("app/setBindGitHub", 1);
          clickGitHubFlow.value = 1;
        }
      } catch (error) {
        console.error(error);
      }
      break;
    default:
      break;
  }
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

function closeKeyLogin() {
  store.dispatch("app/clearNoKeyLogin");
  isNoKeyLogin.value = true;
  ElMessage.success(`${biometricType.value}登录已关闭！`);
}

async function noKeyLogin() {
  // 开始设备验证
  try {
    // 注册WebAuthn
    const support = await checkBiometricSupport();
    if (!support.supported) {
      ElMessage.error('当前设备不支持生物验证');
      return;
    }
    const obj = await loginBegin({ username: store.state.app.userName });
    if (obj.code !== 200) {
      ElMessage.error(obj.msg);
      return;
    }
    const options = obj.data;

    // 验证场景：仅处理必要参数，删除 rp/user（验证场景不需要）
    const publicKey = {
      ...options,
      challenge: base64UrlToArrayBuffer(options.challenge || ''),
      allowCredentials: options.allowCredentials?.map(cred => ({
        ...cred,
        id: base64UrlToArrayBuffer(cred.id || '')
      })) || [],
      // 验证场景不需要 pubKeyCredParams/rp/user，后端也无需返回
      timeout: options.timeout || 60000
    };

    // 前置校验：确保 allowCredentials 非空
    if (!publicKey.allowCredentials.length) {
      throw new Error('未找到匹配的验证凭证');
    }

    // 3. 调用 WebAuthn API 创建凭证
    // ElMessage.info('请使用您的安全密钥、指纹或面部识别进行验证...');

    // 关键：验证场景用 get，不是 create！！！
    const credential = await navigator.credentials.get({
      publicKey: publicKey
    });

    // 后续处理凭证逻辑不变（注意：验证场景的 response 字段和注册场景不同）
    const credentialJson = {
      id: credential.id,
      rawId: arrayBufferToBase64Url(credential.rawId),
      type: credential.type,
      response: {
        authenticatorData: arrayBufferToBase64Url(credential.response.authenticatorData),
        clientDataJSON: arrayBufferToBase64Url(credential.response.clientDataJSON),
        signature: arrayBufferToBase64Url(credential.response.signature),
        userHandle: credential.response.userHandle ? arrayBufferToBase64Url(credential.response.userHandle) : null
      },
      req_id: options.req_id // 传递后端的 req_id 用于验证
    };
    // 5. 验证身份信息
    const result = await loginComplete(credentialJson);

    if (result.code !== 200) {
      ElMessage.error(result.error || '关联验证失败');
      throw new Error(result.error || '关联验证失败');
    }

    ElMessage.success(`${biometricType.value}登录已开启！`);
    const noKeyLoginObj = {
      avatar: result.data.userinfo.avatar || '',
      gid: result.data.userinfo.userName,
      biometricType: biometricType.value,
    }
    store.dispatch("app/setNoKeyLogin", JSON.stringify(noKeyLoginObj));
    isNoKeyLogin.value = false;
  } catch (error) {
    let errorMessage = error.message || '未知错误';
    // Handle specific error types
    if (error.name === 'NotAllowedError') {
      errorMessage = '用户拒绝了认证请求或操作超时';
    } else if (error.name === 'InvalidStateError') {
      errorMessage = '认证器状态无效';
    } else if (error.name === 'NotFoundError') {
      errorMessage = '未找到匹配的凭证';
    } else if (error.name === 'SecurityError') {
      errorMessage = '登录网址未注册认证器';
    }
    console.error('身份验证失败:', error.name);
    ElMessage.error(`身份验证失败: ${errorMessage}`);
  }
}

onMounted(async function () {
  let colorObj = store.state.app.mainColor;
  if (colorObj) {
    checkThemId.value = JSON.parse(colorObj).id;
  }
  document.documentElement.querySelector("title").innerText = "我的主页";
  // 调用检测函数
  const support = await checkBiometricSupport();
  isSupportBiometric.value = support.supported;
  biometricType.value = support.biometricType || '';
  isNoKeyLogin.value = store.state.app.noKeyLogin === '' || JSON.parse(store.state.app.noKeyLogin).gid !== store.state.app.userName;
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

.logintext {
  display: flex;
  height: 50px;
  align-items: center;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.user-name-txt {
  font-size: 20px;
  font-weight: 500;
  margin: 0;
  margin-left: 6px;
  padding: 0;
  color: var(--el-text-color-primary);
}

.me-pagination {
  width: inherit;
  display: flex;
  justify-content: flex-end;
}

.me-pagination span {
  font-size: 14px;
  color: var(--el-text-color-primary);
  line-height: 45px;
  margin-right: 20px;
}

.bind-warning {
  margin: 10px 0;
  width: 350px;
}
</style>
