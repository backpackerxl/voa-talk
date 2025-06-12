<template>
  <div class="loginbody">
    <div class="register-container">
      <el-card class="register-card">
        <p class="logintext">
          <Logo />
        </p>
        <el-form
          :model="registerForm"
          :rules="rules"
          ref="registerFormRef"
          label-position="top"
          label-width="100px"
        >
          <el-form-item label="昵称" prop="name">
            <el-input
              v-model="registerForm.name"
              placeholder="请输入昵称"
              clearable
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              clearable
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱，登录密码将会发送到你的邮箱"
              clearable
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <div class="button-group">
              <el-button size="large" type="primary" @click="handleRegister"
                >注 册</el-button
              >
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

  <el-dialog v-model="state.open" title="请拖动滑块完成验证" width="380">
    <Captcha ref="myCaptcha" @verify="verifyImg" />
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { enrollUser } from "@/api/login";
import Logo from "@/components/Logo";
import Beian from "@/components/Beian";
import Captcha from "@/components/Captcha";

const registerForm = ref({
  name: "",
  username: "",
  email: "",
});

const myCaptcha = ref(null);

const captchaCode = ref("-1");

let state = reactive({
  open: false,
});

function verifyImg(obj) {
  if (obj.tag === true) {
    captchaCode.value = obj.token;
    sendRegister();
    state.open = false;
  } else {
    ElMessage.error("验证不通过");
  }
}

const rules = {
  name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
  username: [
    { required: true, message: "请输入登录账户", trigger: "blur" },
    {
      pattern: /^[a-zA-Z0-9]+$/,
      message: "登录账户只能包含字母和数字",
      trigger: ["blur", "change"],
    },
  ],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    {
      pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
      type: "email",
      message: "邮箱格式不正确",
      trigger: ["blur", "change"],
    },
  ],
};

const registerFormRef = ref(null);
const router = useRouter();

async function sendRegister() {
  const { name, username, email } = registerForm.value;

  try {
    const res = await enrollUser({
      name,
      username,
      email,
      captcha_code: captchaCode.value,
    });
    // console.log("注册后端返回：", res);
    if (res.code === 200) {
      ElMessage.success("注册成功,密码已发送到您的注册邮箱。");
      router.push("/");
    } else {
      ElMessage.error(res.msg);
    }
  } catch (error) {
    console.log(error);
  }
}

const handleRegister = () => {
  registerFormRef.value.validate((valid) => {
    if (valid) {
      state.open = true;
      myCaptcha.value && myCaptcha.value.init();
    } else {
      ElMessage.error("请完善注册信息。");
    }
  });
};

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
</style>
