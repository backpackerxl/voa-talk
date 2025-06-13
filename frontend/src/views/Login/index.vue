<template>
  <div class="loginbody">
    <div class="logindata">
      <el-card>
        <p class="logintext">
          <Logo />
        </p>
        <div class="formdata">
          <el-form
            ref="loginForm"
            :model="form"
            :rules="rules"
            label-position="top"
            label-width="100px"
          >
            <el-form-item label="账号" prop="username">
              <el-input
                class="in-box"
                v-model="form.username"
                size="large"
                clearable
                placeholder="请输入账号"
              >
                <!-- 使用 prefix-icon 插槽添加图标 -->
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                class="in-box"
                v-model="form.password"
                size="large"
                clearable
                placeholder="请输入密码"
                show-password
              >
                <!-- 使用 prefix-icon 插槽添加图标 -->
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-form>
        </div>
        <div class="tool">
          <div>
            <el-checkbox v-model="checked" @change="remenber"
              >记住密码
            </el-checkbox>
          </div>
          <div>
            <a @click="forgetpas">忘记密码？</a>
          </div>
        </div>
        <div class="butt">
          <el-button size="large" type="primary" @click="submitLogin"
            >登 录</el-button
          >
          <div class="register">
            <a @click="register">注 册</a>
          </div>
        </div>
      </el-card>
    </div>
  </div>
  <Beian />
  <el-dialog v-model="state.open" title="请拖动滑块完成验证" width="380" align-center>
    <Captcha ref="myCaptcha" @verify="verifyImg" />
  </el-dialog>
</template>

<script setup>
import { loginUser } from "@/api/login";
import { useRouter } from "vue-router";
import store from "@/store"; // 导入Vuex store
import { User, Lock } from "@element-plus/icons-vue";
import { encryptAes } from "@/utils/tools";
import { config } from "@/utils/config";
import Logo from "@/components/Logo";
import Captcha from "@/components/Captcha";
import Beian from "@/components/Beian";
import { ElMessage } from "element-plus";
import { ref, reactive } from "vue";
const router = useRouter();

const form = ref({
  username: null,
  password: null,
});

const loginForm = ref(null);

const checked = ref(false);

const myCaptcha = ref(null);

const captchaCode = ref("-1");

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

function verifyImg(obj) {
  if (obj.tag === true) {
    captchaCode.value = obj.token;
    sendPostRequest();
    state.open = false;
  } else {
    ElMessage.error("验证不通过");
  }
}

function submitLogin() {
  loginForm.value.validate((valid) => {
    if (valid) {
      // 校验通过，发送请求
      state.open = true;
      myCaptcha.value && myCaptcha.value.init();
    } else {
      // 校验失败，提示用户
      ElMessage.error("请填写完整登录信息");
      return false;
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
      encryptedPassword,
      captchaCode.value
    );
    if (response.code === 200) {
      ElMessage.success("登录成功");

      store.dispatch("app/setAuthorization", response.data.jwtToken);
      store.dispatch("app/setUserRole", response.data.superAdmin);
      store.dispatch("app/setNickName", response.data.nickName);
      const avater = response.data.avatar;
      if (avater) {
        store.dispatch("app/setAvatar", config.BASE_URL + avater);
      }

      router.replace("/home/chat");
    } else {
      ElMessage.error(response.msg);
    }
  } catch (error) {
    console.error(error);
  }
}
// 记住密码
function remenber(data) {
  checked.value = data;
  if (checked.value) {
    localStorage.setItem("password", JSON.stringify(form.value));
  } else {
    localStorage.removeItem("password");
  }
}
function forgetpas() {
  router.push("/forget");
}
function register() {
  router.push("/register");
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
</style>