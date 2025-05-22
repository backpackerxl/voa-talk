<template>
  <div class="loginbody">
    <GitHubLink url="https://github.com/backpackerxl/voa-talk" />
    <div class="logindata">
      <el-card>
        <p class="logintext">
          <Logo />
        </p>
        <div class="formdata">
          <el-form
            ref="form"
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
            <!-- 验证码 -->
            <el-form-item label="验证码" prop="captchaCode">
              <el-input
                class="captcha-input in-box"
                v-model="form.captchaCode"
                size="large"
                clearable
                placeholder="请输入验证码"
              >
                <template #prefix>
                  <el-icon><Picture /></el-icon>
                </template>
              </el-input>
              <div class="captcha-image" v-loading="loading">
                <img :src="captchaImage" @click="refreshCaptcha" alt="验证码" />
              </div>
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
</template>

<script>
import { loginUser, loginCode } from "@/api/login";
import { useRouter } from "vue-router";
import store from "@/store"; // 导入Vuex store
import { Picture, User, Lock } from "@element-plus/icons-vue";
import { encryptAes } from "@/utils/tools";
import { config } from "@/utils/config";
import GitHubLink from "@/components/GitHubLink";
import Logo from "@/components/Logo";

export default {
  name: "LogIn",
  components: {
    Picture,
    User,
    Lock,
    GitHubLink,
    Logo,
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      form: {
        username: null,
        password: null,
        captchaCode: null,
      },
      captchaImage: null,
      loading: false, // 新增的属性，验证码加载使用
      captchaCode: null,
      checked: false,
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
          { max: 20, message: "不能大于20个字符", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" },
        ],
        captchaCode: [
          { required: true, message: "请输入验证码", trigger: "blur" },
          { max: 6, message: "不能大于6个字符", trigger: "blur" },
        ],
      },
    };
  },

  mounted() {
    this.refreshCaptcha(); // 加载验证码图片
  },

  methods: {
    // 获取验证码图片
    async refreshCaptcha() {
      this.loading = true; // 请求开始时设置为true
      try {
        const response = await loginCode();
        const binaryData = response.data.vCode;
        this.captchaImage = `data:image/png;base64,${binaryData}`;
        this.$notify({
          title: "成功",
          message: "验证码加载成功",
          type: "success",
        });
      } catch (error) {
        this.loading = false;
        this.$notify.error({
          title: "错误",
          message: "验证码加载失败",
        });
        console.error("Error fetching the captcha:", error);
      } finally {
        this.loading = false; // 请求结束时设置为false
      }
    },

    submitLogin() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          // 校验通过，发送请求
          this.sendPostRequest();
        } else {
          // 校验失败，提示用户
          this.$message.error("请填写完整登录信息");
          return false;
        }
      });
    },

    async sendPostRequest() {
      try {
        const password = this.form.password;
        let encryptedPassword = encryptAes(password);
        // 使用加密后的密码进行登录
        const response = await loginUser(
          this.form.username,
          encryptedPassword,
          this.form.captchaCode
        );
        // 假设这是登录成功后的处理逻辑
        if (response.code === 200) {
          this.$message({
            type: "success",
            message: "登录成功",
            showClose: true,
          });
          // console.log("服务响应：", response);

          // 往浏览器存入token
          // localStorage.setItem("token", response.data.data.jwtToken);
          store.dispatch("app/setAuthorization", response.data.jwtToken);
          store.dispatch("app/setUserRole", response.data.superAdmin);
          store.dispatch("app/setNickName", response.data.nickName);
          const avater = response.data.avatar;
          if (avater) {
            store.dispatch("app/setAvatar", config.BASE_URL + avater);
          }

          this.$router.replace("/home/chat");
        } else {
          this.$message({
            message: response.msg,
            type: "error",
            showClose: true,
          });
          this.refreshCaptcha();
        }
      } catch (error) {
        console.error(error);
        this.refreshCaptcha();
      }
    },
    // 记住密码
    remenber(data) {
      this.checked = data;
      if (this.checked) {
        localStorage.setItem("password", JSON.stringify(this.form));
      } else {
        localStorage.removeItem("password");
      }
    },
    forgetpas() {
      this.router.push("/forget");
    },
    register() {
      this.router.push("/register");
    },
  },
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

.captcha-input {
  width: 65%; /* 输入框占据一半宽度 */
}

.captcha-image {
  width: 35%; /* 图片占据一半宽度 */
  height: 46px; /* 您可以根据需要调整 */
  text-align: right;
}

.captcha-image img {
  height: 45px;
  object-fit: cover;
  cursor: pointer;
}
</style>