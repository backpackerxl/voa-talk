<template>
  <div class="loginbody">
    <div class="register-container">
      <el-card class="register-card">
        <p class="logintext">AiChat 找回密码</p>
        <el-form
          :model="registerForm"
          :rules="rules"
          ref="registerFormRef"
          label-position="right"
          label-width="100px"
        >
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱，系统将发送修改密码的邮件"
              clearable
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <div class="button-group">
              <el-button size="large" type="primary" @click="handleForget"
                >找回密码</el-button
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
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { forgetPwd } from "@/api/login";

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
      req_url = req_url + '/#/' + 'resetPwd'
      console.log("邮箱：:", { email, req_url });

      try {
        const res = await forgetPwd({ email, req_url });
        if (res.code === 200) {
          ElMessage.success(
            "发送成功！请检查邮箱以完成验证。"
          );
          router.push("/");
        } else {
          ElMessage.error(res.msg);
        }
      } catch (error) {
        console.log(error);
        ElMessage.error("发送失败，请重试。");
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
