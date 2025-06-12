<template>
  <div class="loginbody">
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
    <Captcha />
  </div>
  <Beian />
</template>

<script>
import { loginUser, loginCode } from "@/api/login";
import { useRouter } from "vue-router";
import store from "@/store"; // 导入Vuex store
import { Picture, User, Lock } from "@element-plus/icons-vue";
import { encryptAes } from "@/utils/tools";
import { config } from "@/utils/config";
import Logo from "@/components/Logo";
import Captcha from "@/components/Captcha";
import Beian from "@/components/Beian";

export default {
  name: "LogIn",
  components: {
    Picture,
    User,
    Lock,
    Logo,
    Beian,
    Captcha,
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
      },
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
      },
    };
  },

  mounted() {},

  methods: {
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
        const response = await loginUser(this.form.username, encryptedPassword);
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
        }
      } catch (error) {
        this.$message({
          message: "服务异常",
          type: "error",
          showClose: true,
        });
        console.error(error);
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