<template>
  <div class="loginbody">
    <GitHubLink url="https://github.com/backpackerxl/voa-talk" />
    <div class="register-container">
      <el-card class="register-card">
        <p class="logintext">VoaTalk 找回密码</p>
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
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { forgetPwd } from "@/api/login";
import GitHubLink from "@/components/GitHubLink";

const registerForm = ref({
  email: "",
});

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

const registerFormRef = ref(null);
const router = useRouter();

const handleForget = async () => {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      const { email } = registerForm.value;
      let req_url = window.location.origin;
      req_url = req_url + "/resetPwd";
      console.log("邮箱：:", { email, req_url });

      try {
        const res = await forgetPwd({ email, req_url });
        if (res.code === 200) {
          ElMessage.success("发送成功！请检查邮箱以完成验证。");
          router.push("/");
        } else {
          ElMessage.error(res.msg);
        }
      } catch (error) {
        console.log(error);
      }
    } else {
      ElMessage.error("请填写完整的邮箱信息。");
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
}

.logintext {
  text-align: center;
  font-size: 24px;
  font-weight: 500;
  color: rgb(103, 103, 105);
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

:deep(.el-input__wrapper.is-focus) {
  padding: 5px 15px;
  border-radius: 8px !important;
  box-shadow: 0 0 0 4px #676769 inset !important;
}
</style>
