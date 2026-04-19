<template>
  <div class="loginbody">
    <div class="register-container">
      <el-card class="register-card">
        <p class="logintext">
          <Logo />
        </p>
        <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-position="top" label-width="100px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名" clearable size="large"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pwd">
            <el-input v-model="registerForm.pwd" placeholder="请输入新密码" size="large" clearable show-password></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="pwd_ok">
            <el-input v-model="registerForm.pwd_ok" placeholder="请确认新密码" clearable size="large"
              show-password></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="registerForm.email" placeholder="请输入邮箱，登录密码将会发送到你的邮箱" clearable size="large"></el-input>
          </el-form-item>
          <el-form-item label="验证码: " prop="code">
            <el-input type="number" size="large" v-model="registerForm.code" placeholder="请输入6位验证码">
              <template #suffix>
                <el-button class="get-code" :disabled="codeDisabled" @click="sendEmailCode" plain>{{ emailCodeContent
                }}</el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <div class="button-group">
              <el-button size="large" type="primary" @click="sendRegister">注 册</el-button>
              <div class="login">
                <a @click="goToLogin">登 录</a>
              </div>
            </div>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
  <Beian />
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { encryptAes } from "@/utils/tools";
import { enrollUser, sendEnrollCode } from "@/api/login";
import Logo from "@/components/Logo.vue";
import Beian from "@/components/Beian.vue";

const registerForm = ref({
  username: "",
  pwd: "",
  pwd_ok: "",
  email: "",
  code: ""
});

const codeDisabled = ref(false);
const emailCodeContent = ref("获取验证码");

const validatePassword = (rule, value, callback) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,12}$/;
  if (!regex.test(value)) {
    callback(new Error("密码8~12位, 包含大小写、特殊字符(!@#$%^&*)最少一个"));
  } else {
    callback();
  }
};

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.value.pwd) {
    callback(new Error("两次密码不一致"));
  } else {
    callback();
  }
};

const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

const rules = {
  username: [
    { required: true, message: "请输入登录账户", trigger: "blur" },
    {
      pattern: /^[a-zA-Z0-9]+$/,
      message: "登录账户只能包含字母和数字",
      trigger: ["blur", "change"],
    },
  ],
  pwd: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { validator: validatePassword, trigger: "blur" },
  ],
  pwd_ok: [
    { required: true, message: "请重新输入新密码", trigger: "blur" },
    { validator: validateConfirmPassword, trigger: "blur" },
  ],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    {
      pattern: emailRegex,
      type: "email",
      message: "邮箱格式不正确",
      trigger: ["blur", "change"],
    },
  ],
  code: [
    { required: true, message: "请输入6位验证码", trigger: "blur" },
    { min: 6, max: 6, message: "验证码长度为6位", trigger: "blur" },
  ]
};

const router = useRouter();

const registerFormRef = ref(null);

function sendRegister() {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      const { pwd, code, username, email } = registerForm.value;

      try {
        const res = await enrollUser({
          username,
          password: encryptAes(pwd),
          email,
          captcha_code: code,
        });
        // console.log("注册后端返回：", res);
        if (res.code === 200) {
          ElMessage.success('注册成功！');
          router.push("/");
        }
      } catch (error) {
        console.log(error);
      }
    }
  });
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
    if (!emailRegex.test(registerForm.value.email)) {
      ElMessage.error("邮箱格式不正确");
      return;
    }
    let res = await sendEnrollCode({
      username: registerForm.value.username,
      email: registerForm.value.email
    });
    // 实现倒计时
    codeDisabled.value = true;
    countdown = 60;
    startCountdown();
    if (res.code === 200) {
      ElMessage.success('邮件发送成功，注意查收！');
    }
  } catch (error) {
    console.log(error);
  }
}

const goToLogin = () => {
  router.push("/");
};
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

.register-card {
  width: 380px;
  box-shadow: 0px 4px 6px rgb(0, 0, 0, 0.1);
}

.button-group,
.el-input {
  width: 100%;
}

.button-group {
  height: 76px;
}

.button-group .el-button {
  margin: 15px 0;
  width: 100% !important;
  border: none;
  font-size: 16px;
}

.login {
  color: var(--el-text-color-primary);
  text-align: right;
  font-size: 16px;
}

.login a {
  cursor: pointer;
}

.login a:hover {
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

.get-code {
  cursor: pointer;
  user-select: none;
  border: none;
  padding: 0;
  margin: 0;
}
</style>
