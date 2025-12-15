<template>
  <div class="loginbody">
    <div class="logindata">
      <el-card v-if="loginPage">
        <p class="logintext">
          <Logo />
        </p>
        <div class="formdata">
          <el-form ref="loginForm" :model="form" :rules="rules" label-position="top" label-width="100px">
            <el-form-item label="账号" prop="username">
              <el-input class="in-box" v-model="form.username" size="large" clearable placeholder="请输入账号">
                <!-- 使用 prefix-icon 插槽添加图标 -->
                <template #prefix>
                  <el-icon>
                    <User />
                  </el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input class="in-box" v-model="form.password" size="large" clearable placeholder="请输入密码" show-password>
                <!-- 使用 prefix-icon 插槽添加图标 -->
                <template #prefix>
                  <el-icon>
                    <Lock />
                  </el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-form>
        </div>
        <div class="tool">
          <div>
            <el-checkbox v-model="checked" @change="remenber">记住密码
            </el-checkbox>
          </div>
          <div>
            <a @click="forgetpas">忘记密码？</a>
          </div>
        </div>
        <div class="butt">
          <el-button size="large" type="primary" @click="submitLogin">登 录</el-button>
          <div class="register">
            <a @click="register">注 册</a>
          </div>
        </div>
        <div class="other-login">
          <p class="text">第三方登录</p>
          <div class="logo-container">
            <el-tooltip class="box-item" effect="light" content="QQ登录" placement="bottom">
              <div class="item" @click="qqLogin">
                <i class="fa-brands fa-qq"></i>
              </div>
            </el-tooltip>
            <el-tooltip class="box-item" effect="light" content="GitHub登录" placement="bottom">
              <div class="item" @click="githubLogin">
                <i class="fa-brands fa-github"></i>
              </div>
            </el-tooltip>
          </div>
        </div>
      </el-card>
      <el-card v-if="!loginPage">
        <p class="logintext">
          <Logo />
        </p>
        <div class="link-user" v-if="state.open">
          <p class="text">开启WebAuthn登录</p>
          <div v-if="!linkOTPShow">
            <el-form-item label="账号:" prop="username">
              <el-input class="in-box" v-model="form.username" size="large" disabled>
                <!-- 使用 prefix-icon 插槽添加图标 -->
                <template #prefix>
                  <el-icon>
                    <User />
                  </el-icon>
                </template>
              </el-input>
            </el-form-item>
          </div>
          <div v-else>
            <el-result icon="success" title="关联成功！" sub-title="请点击完成按钮完成后续操作"></el-result>
          </div>
          <el-button size="large" type="primary" @click="linkAccount" v-if="!linkOTPShow">关联此账号</el-button>
          <el-button size="large" type="primary" @click="dialogOTPVisible = true" v-else>
            完 成
          </el-button>
        </div>
        <div class="verify-webAuthn" v-else>
          <div class="formdata">
            <el-form ref="loginForm" :model="formOtp" :rules="otpRules" label-position="top" label-width="100px">
              <el-form-item label="请输入一次性密码" prop="optcode" v-if="otpShow">
                <el-input class="in-box otp-input" v-model="formOtp.optcode" size="large" clearable
                  placeholder="XXX XXX"></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div class="butt">
            <el-button size="large" type="primary" @click="verifyOtpOrAuthn" :disabled="authnBtn">{{ authnTxt
            }}</el-button>
            <div class="register">
              <a @click="otpShow = !otpShow">一次性密码验证</a>
            </div>
          </div>
        </div>
        <el-collapse v-model="activeNames" accordion v-if="state.open">
          <el-collapse-item name="1" v-if="qrcode">
            <template #title="{ isActive }">
              <div :class="['title-wrapper', { 'is-active': isActive }]">
                关联OTP
                <el-icon class="header-icon">
                  <info-filled />
                </el-icon>
              </div>
            </template>
            <div>
              扫描二维码或通过密钥添加应用, 成功后可通过验证码验明身份, 完成后点击按钮继续完成登录。
            </div>
            <div class="otp-container">
              <img :src="qrcode" alt="OTP QR Code" class="qr-img" />
              <p class="qr-secret">密钥：<span>{{ qrSecret }}</span><i class="copy-icon fa-solid fa-copy"
                  @click="copySecret($event.currentTarget, qrSecret)"></i>
              </p>
            </div>
          </el-collapse-item>
          <el-collapse-item name="2" title="什么是 WebAuthn?">
            <div>
              WebAuthn 是一种 Web 标准，允许用户使用生物识别、安全密钥或手机进行身份验证，提高账户的安全性。
            </div>
            <div>
              <p>支持的认证方式:</p>
              <ul>
                <li>Windows Hello / Face ID / Touch ID</li>
                <li>YubiKey 等安全密钥</li>
                <li>手机认证器应用</li>
              </ul>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-card>
    </div>
  </div>
  <Beian />
  <!-- <el-dialog
    v-model="state.open"
    title="请拖动滑块完成验证"
    width="380"
    align-center
  >
    <Captcha ref="myCaptcha" @verify="verifyImg" />
  </el-dialog> -->

  <el-dialog v-model="dialogOTPVisible" title="OTP关联" width="380" align-center>
    <span>是否需要关联OTP认证?</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="goLogin">继续登录</el-button>
        <el-button type="primary" @click="linkOTP">
          关联OTP
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { loginUser } from "@/api/login";
import { registerBegin, registerComplete, generateOtpQrcode, loginBegin, loginComplete, verifyOtp } from "@/api/twoFAuth";
import { useRouter } from "vue-router";
import store from "@/store"; // 导入Vuex store
import { User, Lock } from "@element-plus/icons-vue";
import { encryptAes } from "@/utils/tools";
import { copySecret } from "@/utils/render-html";
import { arrayBufferToBase64Url, base64UrlToArrayBuffer, isValidBase64Url, getServerUrl } from "@/utils/webAuthnHelper";
import Logo from "@/components/Logo";
// import Captcha from "@/components/Captcha";
import Beian from "@/components/Beian";
import { ElMessage } from "element-plus";
import { InfoFilled } from '@element-plus/icons-vue'
import { ref, reactive, onMounted } from "vue";
const router = useRouter();
import device from "current-device";

let pcOrMobile = device.mobile() ? "mobile" : "pc";

const appId = "102796804";
const redirectUri = encodeURIComponent("https://voatalk.online/others/handle");
const stateF = "qqLogin"; // 用于防止攻击
const scope = "get_user_info"; // 所需权限

const qqLoginUrl = ref(
  `https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=${appId}&redirect_uri=${redirectUri}&state=${stateF}&scope=${scope}&display=${pcOrMobile}`
);
const form = ref({
  username: null,
  password: null,
});

const formOtp = ref({
  optcode: null,
});

const loginPage = ref(true);

const loginForm = ref(null);

const qrcode = ref(null);
const qrSecret = ref(null);

const checked = ref(false);

const dialogOTPVisible = ref(false);

const activeNames = ref(['1']);

const linkOTPShow = ref(false);
const otpShow = ref(false);
const authnBtn = ref(false);
const authnTxt = ref('验 证');

// const myCaptcha = ref(null);

// const captchaCode = ref("-1");

let state = reactive({
  open: false,
});

const rules = {
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    { max: 20, message: "不能大于20个字符", trigger: "blur" },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { max: 10, message: "不能大于10个字符", trigger: "blur" },
  ],
};

const otpRules = {
  optcode: [
    { required: true, message: "请输入一次性密码", trigger: "blur" },
    { min: 6, max: 6, message: "一次性密码必须为6位", trigger: "blur" },
    // 自定义校验规则：长度为6时触发函数
    {
      validator: (rule, value, callback) => {
        // 1. 空值不处理（交给必填校验）
        if (!value) {
          callback();
          return;
        }
        // 2. 长度为6时触发目标函数
        if (value.length === 6) {
          authnBtn.value = true;
          authnTxt.value = '验证中...';
          setTimeout(() => {
            handleOptcodeComplete(value); // 触发自定义逻辑
            authnBtn.value = false;
            authnTxt.value = '验 证';
          }, 600);
        }
        // 3. 校验通过（不阻断原有校验）
        callback();
      },
      trigger: ["change"] // 输入/失去焦点时触发, 改变时触发
    }
  ],
}

async function handleOptcodeComplete(optcode) {
  // 验证一次性密码
  const verifyResponse = await verifyOtp({
    username: form.value.username,
    otp_code: optcode,
  });
  if (verifyResponse.data.status === 'ok') {
    ElMessage.success(verifyResponse.data.message);
    cacheUserInfoAndRedirect(verifyResponse.data.userinfo);
  } else {
    ElMessage.error(verifyResponse.data.message);
  }
}

// function verifyImg(obj) {
//   if (obj.tag === true) {
//     captchaCode.value = obj.token;
//     sendPostRequest();
//     state.open = false;
//   } else {
//     ElMessage.error("验证不通过");
//   }
// }

function submitLogin() {
  loginForm.value.validate((valid) => {
    if (valid) {
      // 校验通过，发送请求
      sendPostRequest();
      // state.open = true;
      // myCaptcha.value && myCaptcha.value.init();
    }
  });
}

async function sendPostRequest() {
  try {
    const password = form.value.password;
    let encryptedPassword = encryptAes(password);
    // 使用加密后的密码进行登录
    const response = await loginUser(
      form.value.username,
      encryptedPassword
    );
    if (response.code === 200) {
      loginPage.value = false;
      // 检查用户是否注册了WebAuthn
      state.open = !response.data.register_authenticated;
    } else {
      ElMessage.error(response.msg);
    }
  } catch (error) {
    console.error(error);
  }
}

function cacheUserInfoAndRedirect(userinfo) {
  store.dispatch("app/setAuthorization", userinfo.jwtToken);
  store.dispatch("app/setUserRole", userinfo.superAdmin);
  store.dispatch("app/setNickName", userinfo.nickName);
  store.dispatch("app/setUserName", userinfo.userName);
  store.dispatch("app/setUserEmail", userinfo.email);
  store.dispatch("app/setAvatar", userinfo.avatar);
  router.replace("/home/chat");
}

async function verifyOtpOrAuthn() {

}

function goLogin() {
  dialogOTPVisible.value = false;
  // 执行继续登录的逻辑
  loginPage.value = true;
}

function linkOTP() {
  dialogOTPVisible.value = false;
  // 执行绑定OTP的逻辑
  // 获取并显示OTP QR码
  fetchOTPQRCode(form.value.username);
}

async function linkAccount() {
  try {
    // 注册WebAuthn
    const obj = await registerBegin({ username: form.value.username });
    if (obj.code !== 200) {
      ElMessage.error(obj.msg);
      return;
    }
    const options = obj.data;

    // 2. 转换选项格式
    const publicKey = {
      ...options,
      challenge: base64UrlToArrayBuffer(options.challenge),
      user: {
        ...options.user,
        id: base64UrlToArrayBuffer(options.user.id)
      }
    };

    // 3. 调用 WebAuthn API 创建凭证
    ElMessage.info('请使用您的安全密钥、指纹或面部识别进行验证...');

    const credential = await navigator.credentials.create({
      publicKey: publicKey
    });

    // 4. 准备发送到服务器的数据
    const credentialJson = {
      id: credential.id,
      rawId: arrayBufferToBase64Url(credential.rawId),
      type: credential.type,
      response: {
        attestationObject: arrayBufferToBase64Url(
          credential.response.attestationObject
        ),
        clientDataJSON: arrayBufferToBase64Url(
          credential.response.clientDataJSON
        ),
        transports: credential.response.getTransports ?
          credential.response.getTransports() : ['internal']
      },
      req_id: options.req_id
    };
    // 5. 验证注册
    ElMessage.info('正在验证关联信息...');

    const result = await registerComplete(credentialJson);

    if (result.code !== 200) {
      ElMessage.error(result.error || '关联验证失败');
      throw new Error(result.error || '关联验证失败');
    }

    ElMessage.success('关联成功！');

    linkOTPShow.value = true;

  } catch (error) {
    console.error('关联失败:', error);
    let errorMessage = error.message || '未知错误';
    // Handle specific error types
    if (error.name === 'NotAllowedError') {
      errorMessage = '用户拒绝了认证请求或操作超时';
    } else if (error.name === 'InvalidStateError') {
      errorMessage = '认证器状态无效';
    } else if (error.name === 'ConstraintError') {
      errorMessage = '凭证已存在';
    }
    ElMessage.error(`关联失败: ${errorMessage}`);
  }
}

async function fetchOTPQRCode(username) {
  try {
    const result = await generateOtpQrcode(username);

    if (result.code !== 200) {
      ElMessage.error(result.msg || '获取QR码失败');
      throw new Error(result.error || '获取QR码失败');
    }

    // 显示QR码和密钥
    qrcode.value = `data:image/png;base64,${result.data.qrcode}`;
    qrSecret.value = result.data.secret;
  } catch (error) {
    console.error('获取OTP QR码失败:', error);
    // 即使获取QR码失败，也不影响注册成功流程
    ElMessage.warning(`获取OTP QR码失败: ${error.message}`);
  }
}

// 记住密码
function remenber(data) {
  checked.value = data;
  if (checked.value) {
    localStorage.setItem("userInfo", JSON.stringify(form.value));
  } else {
    localStorage.removeItem("userInfo");
  }
}

onMounted(function () {
  const obj = localStorage.getItem("userInfo");
  if (obj) {
    form.value = JSON.parse(obj);
    checked.value = true;
  }
});

function forgetpas() {
  router.push("/forget");
}
function register() {
  router.push("/register");
}

function githubLogin() {
  if (device.mobile()) {
    window.open("https://github.com");
  } else {
    window.open(
      "https://github.com",
      "GitHub登录",
      "width=800,height=500,top=100,left=100,menubar=no,toolbar=no"
    );
  }
}

function qqLogin() {
  window.location.replace(qqLoginUrl.value);
  // if (device.mobile()) {
  //   window.open(qqLoginUrl.value);
  // } else {
  //   window.open(
  //     qqLoginUrl.value,
  //     "QQ登录",
  //     "width=800,height=500,top=100,left=100,menubar=no,toolbar=no"
  //   );
  // }
}
</script>

<style scoped>
.loginbody {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--el-bg-color);
}

.logintext {
  text-align: center;
  font-size: 24px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin: 10px 0;
}

.logindata {
  width: 380px;
  box-shadow: 0px 4px 6px rgb(0, 0, 0, 0.1);
}

.tool {
  display: flex;
  justify-content: space-between;
  color: var(--el-text-color-primary);
  font-size: 14px;
  height: 32px;
  line-height: 32px;
}

.tool a {
  cursor: pointer;
}

.butt {
  height: 86px;
}

.butt .el-button {
  margin: 15px 0;
  width: 100% !important;
  border: none;
  font-size: 16px;
}

.register {
  color: var(--el-text-color-primary);
  text-align: right;
  font-size: 16px;
  height: 40px;
}

.register a {
  cursor: copy;
}

.register a:hover,
.tool a:hover {
  color: var(--el-color-primary);
}

:deep(.el-input__wrapper) {
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

.other-login .text {
  text-align: center;
  color: var(--el-text-color-primary);
  padding: 6px 0;
  margin: 0;
  position: relative;
}

.other-login .text::before,
.other-login .text::after {
  position: absolute;
  content: "";
  background: var(--w-e-textarea-border-color);
  height: 1px;
  width: 35%;
  top: 50%;
}

.other-login .text::before {
  left: 1px;
}

.other-login .text::after {
  right: 1px;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-container .item {
  margin: 0 10px;
  font-size: 28px;
  color: var(--el-color-primary);
  cursor: pointer;
}

.link-user .text {
  text-align: center;
}

.link-user .el-button {
  margin: 15px 0;
  width: 100% !important;
  border: none;
  font-size: 16px;
}

.link-user .el-result {
  padding: 0 !important;
}

.otp-container .qr-img {
  width: 120px;
  height: 120px;
}

.otp-container .qr-secret .copy-icon {
  margin-left: 6px;
}

/* 控制el-input的输入框文本居中 */
.otp-input :deep(.el-input__inner) {
  text-align: center;
  font-size: 16px;
}

/* 可选：让placeholder也居中（部分浏览器需兼容） */
.otp-input :deep(.el-input__inner)::placeholder {
  text-align: center;
}
</style>