<template>
  <div class="loginbody">
    <div class="register-container">
      <el-card class="register-card">
        <p class="logintext">AiChat 修改密码</p>
        <el-form
          :model="registerForm"
          :rules="rules"
          ref="registerFormRef"
          label-position="right"
          label-width="100px"
        >
          <el-form-item label="密码" prop="pwd">
            <el-input
              v-model="registerForm.pwd"
              placeholder="请输入新密码"
              size="large"
              clearable
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="pwd_ok">
            <el-input
              v-model="registerForm.pwd_ok"
              placeholder="请确认新密码"
              clearable
              size="large"
              show-password
            ></el-input>
          </el-form-item>
          <el-form-item>
            <div class="button-group">
              <el-button size="large" type="primary" @click="handleResetPwd"
                >修改密码</el-button
              >
            </div>
          </el-form-item>
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
  pwd: [{ validator: validatePassword, trigger: "blur" }],
  pwd_ok: [{ validator: validateConfirmPassword, trigger: "blur" }],
};

const registerFormRef = ref(null);
const router = useRouter();
const routePath = useRoute();

const handleResetPwd = async () => {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      // Aa!#123456
      const { pwd, pwd_ok } = registerForm.value;
      const secret_key = routePath.params.secretKey || '';
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
        ElMessage.error("密码重置失败，请重试。");
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
  height: 100%;
  min-width: 1000px;
  background-image: url("@/assets/login3.jpg");
  background-size: 100% 100%;
  background-position: center center;
  overflow: auto;
  background-repeat: no-repeat;
  position: fixed;
  line-height: 100%;
  padding-top: 150px;
}

.logintext {
  text-align: center;
  font-size: 24px;
  font-weight: 500;
  color: rgb(103, 103, 105);
}

.register-card {
  margin-left: 120px;
  width: 500px;
  box-shadow: 0px 10px 30px 10px rgb(255, 255, 255, 0.3);
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
  background: rgb(103, 103, 105, 0.8);
}

.button-group .el-button:hover {
  background: rgb(103, 103, 105);
}

:deep(.el-input__wrapper) {
  padding: 5px 15px;
  margin: 4px 0;
  border-radius: 8px !important;
  box-shadow: 0 0 0 4px var(--el-input-border-color, var(--el-border-color))
    inset !important;
  background-color: transparent !important;
}

:deep(.el-form-item__label) {
  line-height: 56px;
}

:deep(.el-input__wrapper.is-focus) {
  padding: 5px 15px;
  border-radius: 8px !important;
  box-shadow: 0 0 0 4px #676769 inset !important;
}
</style>
