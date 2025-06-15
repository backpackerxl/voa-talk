<template>
  <div class="loginbody">
    <div class="register-container">
      <el-card class="register-card">
        <p class="logintext"><Logo /></p>
        <el-form
          :model="registerForm"
          :rules="rules"
          ref="registerFormRef"
          label-position="top"
        >
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱，系统将发送修改密码的邮件"
              clearable
              size="large"
            ></el-input>
          </el-form-item>
          <div class="button-group">
            <el-button size="large" type="primary" @click="handleForget"
              >找回密码</el-button
            >
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
  <Beian />
  <el-dialog v-model="state.open" title="请拖动滑块完成验证" width="380" align-center>
    <Captcha ref="myCaptcha" @verify="verifyImg" />
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { forgetPwd } from "@/api/login";
import Logo from "@/components/Logo";
import Beian from "@/components/Beian";
import Captcha from "@/components/Captcha";

const registerForm = ref({
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
    sendForget();
    state.open = false;
  } else {
    ElMessage.error("验证不通过");
  }
}

const rules = {
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

async function sendForget() {
  const { email } = registerForm.value;
  let req_url = window.location.origin;
  req_url = req_url + "/resetPwd";
  // console.log("邮箱：:", { email, req_url });

  try {
    const res = await forgetPwd({
      email,
      req_url,
      captcha_code: captchaCode.value,
    });
    if (res.code === 200) {
      ElMessage.success("发送成功！请检查邮箱以完成验证。");
      router.push("/");
    } else {
      ElMessage.error(res.msg);
    }
  } catch (error) {
    console.log(error);
  }
}

const registerFormRef = ref(null);
const router = useRouter();

const handleForget = () => {
  registerFormRef.value.validate((valid) => {
    if (valid) {
      state.open = true;
      myCaptcha.value && myCaptcha.value.init();
    }
  });
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

.button-group .el-button {
  margin: 15px 0;
  width: 100% !important;
  border: none;
  font-size: 16px;
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
