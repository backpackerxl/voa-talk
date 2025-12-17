<template>
  <div class="loginbody">
    <div class="logindata">
      <el-card v-if="loginPage">
        <p class="logintext">
          <Logo />
        </p>
        <div class="formdata">
          <el-form ref="loginForm" :model="form" :rules="rules" label-position="top" label-width="100px">
            <el-form-item label="用户名/邮箱号" prop="username">
              <el-input class="in-box" v-model="form.username" size="large" clearable placeholder="用户名/邮箱号登录">
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
          <p class="text">其他登录方式</p>
          <div class="logo-container">
            <el-tooltip class="box-item" effect="light" content="免密登录" placement="bottom">
              <div class="item" @click="verifyOtpOrAuthn">
                <i class="fa-solid fa-key"></i>
              </div>
            </el-tooltip>
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
          <div v-else class="link-success">
            <p><el-text class="mx-1">关联成功！</el-text></p>
            <p><el-text class="mx-1" size="small">请点击完成按钮完成后续操作, 并妥善保存恢复码, 以防授权设备丢失可用于找回账号！</el-text></p>
            <p>
              <el-text class="mx-1" size="small" v-for="item in recoveryCode" :key="item">
                {{ item }}&nbsp;&nbsp;
              </el-text>
              <i class="copy-icon fa-solid fa-copy"
                @click="copySecret($event.currentTarget, recoveryCode.join(' '))"></i>
            </p>
          </div>
          <el-button size="large" type="primary" @click="linkAccount" v-if="!linkOTPShow">关联此账号</el-button>
          <el-button size="large" type="primary" @click="dialogOTPVisible = true" v-else>
            完 成
          </el-button>
        </div>
        <div class="verify-webAuthn" v-else>
          <div class="formdata">
            <el-form ref="loginForm" :model="formOtp" :rules="otpRules" label-position="top" label-width="100px">
              <el-form-item label="请输入一次性密码/恢复码" prop="optcode" v-if="otpShow">
                <el-input class="in-box otp-input" v-model="formOtp.optcode" size="large" clearable
                  :placeholder="placeholderTxt"></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div class="butt">
            <el-button size="large" type="primary" @click="verifyOtpOrAuthn" :disabled="authnBtn" :icon="Pointer">{{
              authnTxt
            }}</el-button>
          </div>
          <div>
            <el-collapse>
              <el-collapse-item name="3">
                <template #title="{ isActive }">
                  <div :class="['title-wrapper', { 'is-active': isActive }]">
                    其他验证方式
                    <el-icon class="header-icon">
                      <info-filled />
                    </el-icon>
                  </div>
                </template>
                <div class="verify-other-butt">
                  <el-button type="primary" @click="verifyOTPCode" plain>安全密码验证</el-button>
                  <el-button type="danger" @click="verifyRecoveryCode" plain>一次性恢复码验证</el-button>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
        <el-collapse class="collapse-container" v-model="activeNames" accordion v-if="state.open">
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
import { registerBegin, registerComplete, generateOtpQrcode, verifyRecovery, loginBegin, loginComplete, verifyOtp } from "@/api/twoFAuth";
import { useRouter } from "vue-router";
import store from "@/store"; // 导入Vuex store
import { User, Lock } from "@element-plus/icons-vue";
import { encryptAes, decryptAes } from "@/utils/tools";
import { copySecret } from "@/utils/render-html";
import { arrayBufferToBase64Url, base64UrlToArrayBuffer } from "@/utils/webAuthnHelper";
import Logo from "@/components/Logo";
// import Captcha from "@/components/Captcha";
import Beian from "@/components/Beian";
import { ElMessage } from "element-plus";
import { InfoFilled, Pointer } from '@element-plus/icons-vue'
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
const authnTxt = ref('设备验证');
const recoveryCode = ref([]);
const placeholderTxt = ref('');
const nextId = ref('');

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
    { max: 12, message: "不能大于12个字符", trigger: "blur" },
  ],
};

const otpRules = {
  optcode: [
    { required: true, message: "请输入一次性密码/恢复码", trigger: "blur" },
    // 自定义校验规则：长度为6时触发函数
    {
      validator: (rule, value, callback) => {
        // 1. 空值不处理（交给必填校验）
        if (!value) {
          callback();
          return;
        }
        // 2. 长度为6时触发目标函数
        if (value.length === 6 && placeholderTxt.value === 'XXX XXX') {
          authnBtn.value = true;
          authnTxt.value = '验证中...';
          setTimeout(() => {
            handleOptcodeComplete(value); // 触发自定义逻辑
            authnBtn.value = false;
            authnTxt.value = '验 证';
          }, 600);
        }
        // 4. 长度为8时触发目标函数
        if (value.length === 8 && placeholderTxt.value === 'XXXX XXXX') {
          authnBtn.value = true;
          authnTxt.value = '验证中...';
          setTimeout(() => {
            handleRecoveryCodeComplete(value); // 触发自定义逻辑
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
  try {
    // 验证一次性密码
    const verifyResponse = await verifyOtp({
      username: form.value.username,
      otp_code: optcode,
      next_id: nextId.value,
    });
    ElMessage.success(verifyResponse.data.message);
    cacheUserInfoAndRedirect(verifyResponse.data.userinfo);
  } catch (error) {
    formOtp.value.optcode = '';
    console.error('错误信息：', error.message); // 如 'token过期'/'参数错误'
    // 捕获异常：读取挂载的 code 和 错误信息
    if (error.code === 301) {
      loginPage.value = true;
    }
  }
}

async function handleRecoveryCodeComplete(recoveryCode) {
  // 验证恢复密码
  try {
    const verifyResponse = await verifyRecovery({
      username: form.value.username,
      recovery_code: encryptAes(recoveryCode),
      next_id: nextId.value,
    });
    ElMessage.success(verifyResponse.data.message);
    cacheUserInfoAndRedirect(verifyResponse.data.userinfo);
  } catch (error) {
    formOtp.value.optcode = '';
    console.error('错误信息：', error.message); // 如 'token过期'/'参数错误'
    // 捕获异常：读取挂载的 code 和 错误信息
    if (error.code === 301) {
      loginPage.value = true;
    }
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
      nextId.value = response.data.next_id || '';
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
  store.dispatch("app/setUserEmail", userinfo.email || '');
  store.dispatch("app/setAvatar", userinfo.avatar || '');
  router.replace("/home/chat");
}

async function verifyOtpOrAuthn() {
  otpShow.value = false;
  authnTxt.value = '设备验证';
  if (!form.value.username) {
    ElMessage.error('请输入用户名进行免密登录！');
    return;
  }
  // 开始设备验证
  try {
    // 注册WebAuthn
    const obj = await loginBegin({ username: form.value.username });
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
    ElMessage.info('请使用您的安全密钥、指纹或面部识别进行验证...');

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

    ElMessage.success('身份验证成功！');
    cacheUserInfoAndRedirect(result.data.userinfo);

  } catch (error) {
    let errorMessage = error.message || '未知错误';
    // Handle specific error types
    if (error.name === 'NotAllowedError') {
      errorMessage = '用户拒绝了认证请求或操作超时';
    } else if (error.name === 'InvalidStateError') {
      errorMessage = '认证器状态无效';
    } else if (error.name === 'NotFoundError') {
      errorMessage = '未找到匹配的凭证';
    }
    console.error('身份验证失败:', errorMessage);
    // ElMessage.error(`身份验证失败: ${errorMessage}`);
  }
}

function verifyOTPCode() {
  otpShow.value = true;
  formOtp.value.optcode = '';
  placeholderTxt.value = 'XXX XXX';
}

function verifyRecoveryCode() {
  otpShow.value = true;
  formOtp.value.optcode = '';
  placeholderTxt.value = 'XXXX XXXX';
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
      challenge: base64UrlToArrayBuffer(options.challenge || ''),
      user: {
        ...options.user,
        id: base64UrlToArrayBuffer(options.user.id || '')
      },
      // 兼容老浏览器：修正residentKey值
      authenticatorSelection: {
        ...options.authenticatorSelection,
        residentKey: options.authenticatorSelection.residentKey === 'preferred'
          ? 'discouraged'
          : options.authenticatorSelection.residentKey
      }
    };

    // 3. 调用 WebAuthn API 创建凭证
    ElMessage.info('请使用您的安全密钥、指纹或面部识别进行验证关联...');

    const credential = await navigator.credentials.create({
      publicKey: publicKey
    });

    // 3. 准备发送到服务器的数据（核心修复：transports字段）
    let transports = [];
    // 安全获取transports：兼容不同浏览器实现
    if (credential.response?.getTransports) {
      try {
        const rawTransports = credential.response.getTransports();
        // 确保transports是数组（防止返回Set/undefined）
        transports = Array.isArray(rawTransports)
          ? rawTransports
          : (rawTransports ? [rawTransports] : []);
      } catch (e) {
        transports = ['internal']; // 异常兜底
      }
    } else {
      transports = ['internal']; // 无getTransports方法时兜底
    }

    const credentialJson = {
      id: credential.id || '', // 空值兜底
      rawId: arrayBufferToBase64Url(credential.rawId),
      type: credential.type || 'public-key', // 兜底默认值
      response: {
        attestationObject: arrayBufferToBase64Url(
          credential.response?.attestationObject || new ArrayBuffer(0)
        ),
        clientDataJSON: arrayBufferToBase64Url(
          credential.response?.clientDataJSON || new ArrayBuffer(0)
        ),
        transports: transports // 确保是纯数组，无Set/undefined
      },
      req_id: options.req_id || '' // 空值兜底
    };
    // 5. 验证注册
    const result = await registerComplete(credentialJson);

    if (result.code !== 200) {
      ElMessage.error(result.error || '关联验证失败');
      throw new Error(result.error || '关联验证失败');
    }

    ElMessage.success('关联成功！');
    recoveryCode.value = result.data.fa_recovery_code.map(item => decryptAes(item));

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
  line-height: 1.4;
  padding: 10px;
  margin: 0;
  font-size: 18px;
}

.link-user .link-success p {
  line-height: 1.6;
  padding: 0;
  margin: 0;
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

.collapse-container {
  overflow: auto;
  max-height: 280px;
}

.verify-other-butt .el-button {
  border: none;
  width: 100%;
  margin: 5px 0;
}
</style>