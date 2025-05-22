<template>
  <div class="loginbody">
    <GitHubLink url="https://github.com/backpackerxl/voa-talk" />
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
        >
          <el-form-item label="新密码" prop="pwd">
            <el-input
              v-model="registerForm.pwd"
              placeholder="请输入新密码"
              size="large"
              clearable
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item label="确认新密码" prop="pwd_ok">
            <el-input
              v-model="registerForm.pwd_ok"
              placeholder="请确认新密码"
              clearable
              size="large"
              show-password
            ></el-input>
          </el-form-item>
          <div class="button-group">
            <el-button size="large" type="primary" @click="handleResetPwd"
              >修改密码</el-button
            >
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import { resetPWD } from "@/api/login";
import { encryptAes } from "@/utils/tools";
import GitHubLink from "@/components/GitHubLink";
import Logo from "@/components/Logo";

const registerForm = ref({
  pwd: "",
  pwd_ok: "",
});

const validatePassword = (rule, value, callback) => {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_])[A-Za-z\d\W_]{8,}$/;
  if (!regex.test(value)) {
    callback(new Error("密码最低8位, 包含小写、大写、特殊字符最少各一个"));
  } else {
    callback();
  }
};

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.value.pwd) {
    callback(new Error("密码不一致"));
  } else {
    callback();
  }
};

const rules = {
  pwd: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { validator: validatePassword, trigger: "blur" },
  ],
  pwd_ok: [
    { required: true, message: "请重新输入新密码", trigger: "blur" },
    { validator: validateConfirmPassword, trigger: "blur" },
  ],
};

const registerFormRef = ref(null);
const router = useRouter();
const routePath = useRoute();

const handleResetPwd = async () => {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      // Aa!#123456
      const { pwd, pwd_ok } = registerForm.value;
      const secret_key = routePath.params.secretKey || "";
      console.log("密码重置数据:", { pwd, pwd_ok, secret_key });
      try {
        const res = await resetPWD({ pwd: encryptAes(pwd), secret_key });
        // console.log("密码重置后端返回：", res);
        if (res.code === 200) {
          ElMessage.success("密码重置成功！");
          router.push("/");
        } else {
          ElMessage.error(res.msg);
        }
      } catch (error) {
        console.log(error);
      }
    } else {
      ElMessage.error("请填写完整的密码信息。");
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
  --el-input-height: 46px;
  border-radius: 8px !important;
  box-shadow: 0 0 0 4px var(--el-input-border-color) inset !important;
  background-color: transparent !important;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 4px var(--el-color-primary) inset !important;
}

:deep(.el-form-item.is-error .el-input__wrapper) {
  box-shadow: 0 0 0 4px var(--el-color-danger) inset !important;
}
</style>
