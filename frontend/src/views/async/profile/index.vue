<template>
  <div class="user-edit">
    <el-upload ref="uploadRef" :style="imageUrl ? 'display: none' : 'display: block'"
      :action="config.BASE_URL + '/upload'" list-type="picture-card" :headers="{ Token: store.state.app.authorization }"
      :on-success="handleSuccess" :before-upload="beforeUpload" :show-file-list="false" accept="image/png, image/jpeg">
      <el-icon>
        <Plus />
      </el-icon>
    </el-upload>
    <div @click="uploadImg" class="avater" v-if="imageUrl">
      <img :src="imageUrl" alt="Uploaded Image" style="max-width: 100%; margin-top: 20px" />
    </div>

    <h3 class="nick-name">{{ welcomStr }}</h3>
    <el-form label-position="left" style="width: 330px">
      <el-form-item label="主题: " class="them-item">
        <el-dropdown>
          <el-button plain>
            <div class="me-icon">
              <span :class="them.icon"></span>
            </div>
            &nbsp;{{ them.label
            }}<el-icon class="el-icon--right">
              <ArrowDown />
            </el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-for="(item, index) in themList" :key="index" @click="changeThem(item)">
                <div class="me-icon">
                  <span :class="item.icon"></span>
                </div>
                &nbsp;{{ item.label }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-form-item>
      <el-form-item label="昵称: " prop="nickName">
        <el-input v-model="welcomStr" placeholder="请输入新的昵称" clearable size="large"></el-input>
      </el-form-item>
      <el-form-item label="邮箱: " prop="email">
        <div class="email-setting">
          <div>
            <el-tag size="large">{{
              userEmail !== "" ? userEmail : "绑定邮箱才能重置密码哦"
            }}</el-tag>
          </div>
          <div>
            <el-button plain :icon="Edit" @click="changeEmail">
              {{ userEmail !== "" ? "更换" : "绑定" }}
            </el-button>
          </div>
        </div>
      </el-form-item>
      <el-form-item>
        <div class="button-group">
          <el-button size="large" type="primary" @click="saveUserInfo">
            <svg t="1767109869237" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
              p-id="34482" width="16" height="16">
              <path
                d="M512 85.333333c-140.8 0-256 115.2-256 256 0 81.066667 38.4 153.6 98.133333 200.533334C196.266667 605.866667 85.333333 759.466667 85.333333 938.666667h85.333334c0-187.733333 153.6-341.333333 341.333333-341.333334 140.8 0 256-115.2 256-256S652.8 85.333333 512 85.333333z m0 426.666667c-93.866667 0-170.666667-76.8-170.666667-170.666667s76.8-170.666667 170.666667-170.666666 170.666667 76.8 170.666667 170.666666-76.8 170.666667-170.666667 170.666667zM917.333333 597.333333h-128c-12.8 0-21.333333-8.533333-21.333333-21.333333v-42.666667c0-12.8 8.533333-21.333333 21.333333-21.333333h128c12.8 0 21.333333 8.533333 21.333334 21.333333v42.666667c0 12.8-8.533333 21.333333-21.333334 21.333333zM917.333333 938.666667H618.666667c-12.8 0-21.333333-8.533333-21.333334-21.333334v-42.666666c0-12.8 8.533333-21.333333 21.333334-21.333334h298.666666c12.8 0 21.333333 8.533333 21.333334 21.333334v42.666666c0 12.8-8.533333 21.333333-21.333334 21.333334zM917.333333 768H618.666667c-12.8 0-21.333333-8.533333-21.333334-21.333333v-42.666667c0-12.8 8.533333-21.333333 21.333334-21.333333h298.666666c12.8 0 21.333333 8.533333 21.333334 21.333333v42.666667c0 12.8-8.533333 21.333333-21.333334 21.333333z"
                fill="#ffffff" p-id="34483"></path>
            </svg>
            &nbsp;
            保 存
          </el-button>
        </div>
      </el-form-item>
      <el-collapse v-model="activeNames" v-if="isSupportBiometric">
        <el-collapse-item name="1">
          <template #title="{ isActive }">
            <div :class="['title-wrapper', { 'is-active': isActive }]">
              注册WebAuthn
              <el-icon class="header-icon">
                <Key />
              </el-icon>
            </div>
          </template>
          <div>
            <el-button class="register-btn" type="primary" @click="registerWebAuthn" size="small">
              <div class="auth-icon">
                <span :class="authIcon"></span>
              </div>&nbsp;注册
            </el-button>
          </div>
          <div class="auth-data" v-if="authData.length > 0">
            <el-table :data="authData" stripe style="width: 330px">
              <el-table-column fixed prop="name" width="230">
                <template v-slot="scope">
                  <span class="txt">设备名称：{{ scope.row.name }}</span><br>
                  <span class="txt">创建时间：{{ scope.row.create_date }}</span>
                </template>
              </el-table-column>

              <el-table-column fixed="right" min-width="100">
                <template v-slot="scope">
                  <el-button :icon="Edit" size="small" circle @click="handleUpdateAuth(scope.row)" />
                  <el-button type="danger" :icon="Delete" size="small" circle @click="handleDeleteAuth(scope.row)" />
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-form>
    <div class="opt">
      <p>便捷操作</p>
      <div v-if="isSupportBiometric">
        <el-button size="large" type="primary" @click="noKeyLogin" v-if="isNoKeyLogin">
          <div class="auth-icon">
            <span :class="authIcon"></span>
          </div>&nbsp;
          开启{{ biometricType }}登录
        </el-button>
        <el-button size="large" type="primary" @click="closeKeyLogin" v-else>
          <div class="auth-icon">
            <span :class="authIcon"></span>
          </div>&nbsp;
          关闭{{ biometricType }}登录
        </el-button>
      </div>
      <el-button size="large" type="primary" @click="forgetPwd">
        <svg t="1767109398317" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="28778" width="16" height="16">
          <path
            d="M148.835185 426.377261h670.957116v173.28548h65.395426V422.166298c0-33.717704-26.341769-61.183463-58.856484-61.183464h-77.166323V244.237858c0-65.814423-27.909755-127.508882-78.592311-173.742476C620.729046 25.03378 554.653626 0 484.536241 0S348.343435 25.03378 298.499872 70.496382c-50.681556 46.221595-78.592311 107.929054-78.59231 173.742476v116.743976h-77.61132c-32.449715 0-58.855484 27.465759-58.855484 61.118464v453.189026c0 33.704704 26.405768 61.171464 58.855484 61.171464h399.617496v-65.395427H148.835185z m136.454803-182.138403c0-98.616135 89.382216-178.843432 199.246253-178.843431s199.233253 80.227296 199.233253 178.843431v116.743976H285.289988z"
            fill="#ffffff" p-id="28779"></path>
          <path
            d="M383.029131 601.558725h204.021211v65.395426H383.029131z m427.450251 86.126244a32.697713 32.697713 0 0 0 0 46.247595l18.467839 18.401838H636.043912v65.395427h271.783617a32.697713 32.697713 0 0 0 23.136797-55.821511l-74.224349-74.223349a32.697713 32.697713 0 0 0-46.259595 0zM643.001851 893.941161a32.697713 32.697713 0 0 0 0 46.247594l74.224349 74.224349a32.697713 32.697713 0 0 0 46.247595-46.247594l-18.402839-18.402839h192.838309v-65.395426H666.125648a32.592714 32.592714 0 0 0-23.123797 9.573916z"
            fill="#ffffff" p-id="28780"></path>
        </svg>&nbsp;
        更换密码
      </el-button>
      <div v-if="isMob && loginType === 'voatalk'">
        <el-button size="large" type="primary" @click="linkQQ" v-if="clickQQFlow !== 0">
          <svg t="1767109149691" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="24966" width="16" height="16">
            <path
              d="M824.8 613.2c-16-51.4-34.4-94.6-62.7-165.3C766.5 262.2 689.3 112 511.5 112 331.7 112 256.2 265.2 261 447.9c-28.4 70.8-46.7 113.7-62.7 165.3-34 109.5-23 154.8-14.6 155.8 18 2.2 70.1-82.4 70.1-82.4 0 49 25.2 112.9 79.8 159-26.4 8.1-85.7 29.9-71.6 53.8 11.4 19.3 196.2 12.3 249.5 6.3 53.3 6 238.1 13 249.5-6.3 14.1-23.8-45.3-45.7-71.6-53.8 54.6-46.2 79.8-110.1 79.8-159 0 0 52.1 84.6 70.1 82.4 8.5-1.1 19.5-46.4-14.5-155.8z"
              p-id="24967" fill="#ffffff"></path>
          </svg>&nbsp;
          {{ qqActionTxt[clickQQFlow] }}
        </el-button>
      </div>
      <div v-if="isMob && loginType === 'voatalk'">
        <el-button size="large" type="primary" @click="linkGitHub" v-if="clickGitHubFlow !== 0">
          <svg t="1767109018108" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
            p-id="23912" width="16" height="16">
            <path
              d="M512 128C299.872 128 128 299.872 128 512c0 169.6 110.016 313.6 262.624 364.384 19.264 3.52 26.24-8.256 26.24-18.496 0-9.152-0.352-33.28-0.48-65.28-106.88 23.136-129.376-51.488-129.376-51.488-17.504-44.384-42.624-56.256-42.624-56.256-34.88-23.744 2.624-23.232 2.624-23.232 38.496 2.752 58.752 39.488 58.752 39.488 34.24 58.752 89.856 41.76 111.744 32 3.52-24.864 13.504-41.76 24.384-51.36-85.248-9.632-174.88-42.624-174.88-189.76 0-42.016 15.008-76.256 39.488-103.136-3.872-9.6-17.12-48.736 3.744-101.6 0 0 32.256-10.24 105.632 39.36A367.584 367.584 0 0 1 512 313.76c32.64 0.128 65.504 4.352 96.128 12.864 73.376-49.6 105.504-39.36 105.504-39.36 20.992 52.864 7.872 92 3.84 101.6 24.64 26.88 39.392 61.12 39.392 103.136 0 147.52-89.728 179.872-175.232 189.504 13.76 11.744 25.984 35.232 25.984 71.008 0 51.36-0.352 92.736-0.352 105.376 0 10.24 6.848 22.24 26.368 18.496C786.112 825.504 896 681.6 896 512c0-212.128-171.872-384-384-384z"
              p-id="23913" fill="#ffffff"></path>
          </svg>&nbsp;
          {{ githubActionTxt[clickGitHubFlow] }}
        </el-button>
      </div>
      <p class="them-text">自定义主题色</p>
      <div class="them-color">
        <el-tooltip v-for="item in colorList" :key="item.id" class="box-item" effect="light" :content="item.tip"
          :placement="item.place">
          <div :class="checkThemId === item.id ? 'item checked' : 'item'" @click="selectColor(item)"
            :style="'background-color: ' + item.bgColor">
            <i class="fas fa-check"></i>
          </div>
        </el-tooltip>
      </div>
    </div>
  </div>
  <el-dialog v-model="editDialogVisible" title="修改邮箱号" width="380" align-center>
    <el-form :model="registerForm" :rules="rules" ref="registerFormRef" placeholder="请输入邮箱号">
      <el-form-item label="邮箱号: " prop="email">
        <el-input size="large" v-model="registerForm.email" />
      </el-form-item>
      <el-form-item label="验证码: " prop="code">
        <el-input type="number" size="large" v-model="registerForm.code" placeholder="请输入验证码">
          <template #suffix>
            <el-button class="get-code" :disabled="codeDisabled" @click="getEmailCode" plain>{{ emailCodeContent
            }}</el-button>
          </template>
        </el-input>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="editEmailOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="addEqNameDialogVisible" title="添加WebAuthn设备" width="380" align-center>
    <el-form :model="registerEqForm" :rules="rulesEqName" ref="registerEqFormRef" placeholder="请输入设备名称">
      <el-form-item label="设备名称: " prop="name">
        <el-input size="large" v-model="registerEqForm.name" />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="addEqNameDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addEqNameOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="editEqNameDialogVisible" title="修改WebAuthn设备" width="380" align-center>
    <el-form :model="registerEqForm" :rules="rulesEqName" ref="registerEqFormRef" placeholder="请输入设备名称">
      <el-form-item label="设备名称: " prop="name">
        <el-input size="large" v-model="registerEqForm.name" />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="editEqNameDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updateEqNameOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="deleteEqDialogVisible" title="删除WebAuthn设备" width="380" align-center>
    <span>确定删除，设备将不可恢复</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="deleteEqDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteEqOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>

  <el-dialog v-model="bindAccountDialogVisible" width="380" :show-close="false" align-center>
    <div class="logintext">
      <img :src="userAvatarUrl ? userAvatarUrl : avater" alt="头像" class="user-avatar" />
      <h4 class="user-name-txt">关联：{{ userNameTxt }} 账号</h4>
    </div>
    <div>
      <p></p>
      <el-tag type="warning" class="bind-warning">注意：关联号后，下面的对话内容将合并到当前登录账号下</el-tag>
      <el-table v-loading="state.loading" :data="tableData" border stripe style="width: 360px">
        <el-table-column fixed prop="talk_name" label="对话名称" width="360" />
      </el-table>
      <div class="me-pagination">
        <span>共 {{ tableCount }} 条</span>
        <el-pagination layout="prev, pager, next" :page-size="pageSize" :total="tableCount"
          @current-change="pageQuery" />
      </div>
    </div>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="cancelBindAccount">取消</el-button>
        <el-button type="primary" @click="bindAccount"> 关联 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue";
import store from "@/store";
import {
  Plus,
  Edit,
  Delete,
  ArrowDown,
  Key,
} from "@element-plus/icons-vue";
const welcomStr = ref(store.state.app.nickName);
const userEmail = ref("");
const emailValue = store.state.app.userEmail;
if (emailValue !== "null" && emailValue !== "") {
  userEmail.value = emailValue;
}

const registerForm = ref({
  email: userEmail.value,
  code: "",
});

const editDialogVisible = ref(false);
import router from "@/router";
import { updateUser, sendEmailCodeApi, updateUserEmail } from "@/api/apiUser";
import { getOtherUserChatList, linkOtherUser, noLinkOtherUser } from "@/api/aiChat";
import { arrayBufferToBase64Url, base64UrlToArrayBuffer } from "@/utils/webAuthnHelper";
import { checkBiometricSupport } from "@/utils/webAuthn";
import { loginBegin, loginComplete, registerBegin, registerComplete, updateDevice, deleteDevice, getDevices } from "@/api/twoFAuth";
import { ElMessage, ElMessageBox } from "element-plus";
import { config } from "@/utils/config";
import { handleThem } from "@/utils/tools";
import device from "current-device";
import avater from "@/assets/images/avater.png";
const userNameTxt = ref('');
const userAvatarUrl = ref('');
const authIcon = ref('');

const avatarUrl = store.state.app.avatar;
const loginType = store.state.app.loginType;
const imageUrl = ref(avatarUrl);
const codeDisabled = ref(false);
const emailCodeContent = ref("获取验证码");
const saveUrl = ref(config.BASE_URL);
const checkThemId = ref(1);
const isMob = ref(!device.mobile());
const isSupportBiometric = ref(false);
const isNoKeyLogin = ref(true);
const biometricType = ref('');
const activeNames = ref([]);
const bindAccountDialogVisible = ref(false);
const tableData = ref([]);
const authData = ref([]);
const tableCount = ref(0);
const addEqNameDialogVisible = ref(false);
const editEqNameDialogVisible = ref(false);
const deleteEqDialogVisible = ref(false);
const registerEqForm = ref({
  name: "",
  id: -1,
});
// 当前页码
const currentPage = ref(1);
// 每页显示数量
const pageSize = ref(6);

let state = reactive({
  loading: false,
});

const colorList = ref([
  {
    id: 1,
    bgColor: "#4d6bfe",
    tip: "霓虹蓝",
    tag: null,
    place: "top",
  },
  {
    id: 2,
    bgColor: "#ff7625",
    tip: "岩力橙",
    tag: "cyan",
    place: "top",
  },
  {
    id: 3,
    bgColor: "#0052d9",
    tip: "皇家蓝",
    tag: "blue",
    place: "top",
  },
  {
    id: 4,
    bgColor: "#00A884",
    tip: "流光绿",
    tag: "green",
    place: "top",
  },
  {
    id: 5,
    bgColor: "#00b458",
    tip: "宝石绿",
    tag: "genblue",
    place: "top",
  },
  {
    id: 6,
    bgColor: "#06b3d3",
    tip: "海湾蓝",
    tag: "indigo",
    place: "bottom",
  },
  {
    id: 7,
    bgColor: "#9463f7",
    tip: "宇宙紫",
    tag: "purple",
    place: "bottom",
  },
  {
    id: 8,
    bgColor: "#ffb400",
    tip: "闪电黄",
    tag: "orange",
    place: "bottom",
  },
  {
    id: 9,
    bgColor: "#f74584",
    tip: "玫瑰红",
    tag: "mixedred",
    place: "bottom",
  },
  {
    id: 10,
    bgColor: "#fd0077",
    tip: "璀璨洋红",
    tag: "red",
    place: "bottom",
  },
]);

let pcOrMobile = device.mobile() ? "mobile" : "pc";

const appId = "102796804";
const redirectUri = encodeURIComponent("https://www.voatalk.online/others/handle");
const stateF = "qqLogin"; // 用于防止攻击
const scope = "get_user_info"; // 所需权限

const qqLoginUrl = ref(
  `https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=${appId}&redirect_uri=${redirectUri}&state=${stateF}&scope=${scope}&display=${pcOrMobile}`
);

const githubClientId = "Ov23liTrl7t8g4EZP3j7";
const githubStateF = "githubLogin"; // 用于防止攻击
const gitHubScope = "user"; // 所需权限


const githubLoginUrl = ref(
  `https://github.com/login/oauth/authorize?client_id=${githubClientId}&redirect_uri=${redirectUri}&state=${githubStateF}&scope=${gitHubScope}`
);


const uploadRef = ref(null);
const them = ref(JSON.parse(store.state.app.them));
const themList = ref([
  {
    them: "light",
    label: "浅色",
    icon: "icon theme-light",
  },
  {
    them: "dark",
    label: "深色",
    icon: "icon theme-dark",
  },
  {
    them: "os",
    label: "跟随系统",
    icon: "icon theme-os",
  },
]);
const emailRule = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

function handleDeleteAuth(item) {
  deleteEqDialogVisible.value = true;
  registerEqForm.value = item;
}

function deleteEqOk() {
  deleteEqDialogVisible.value = false;
  deleteDevice({ id: registerEqForm.value.id }).then(res => {
    if (res.code === 200) {
      ElMessage.success('删除成功');
      getDevices().then(res => {
        authData.value = res.data || [];
      });
    }
  }).catch(err => {
    ElMessage.error(err.msg);
  });
}



function handleUpdateAuth(item) {
  registerEqForm.value = item;
  editEqNameDialogVisible.value = true;
}

function updateEqNameOk() {
  registerEqFormRef.value.validate((valid) => {
    if (valid) {
      editEqNameDialogVisible.value = false;
      updateDevice({ name: registerEqForm.value.name, id: registerEqForm.value.id }).then(res => {
        if (res.code === 200) {
          ElMessage.success('修改成功');
          getDevices().then(res => {
            authData.value = res.data || [];
          });
        }
      }).catch(err => {
        ElMessage.error(err.msg);
      });
    }
  });
}

function registerWebAuthn() {
  registerEqForm.value = {
    name: "",
    id: -1,
  };
  addEqNameDialogVisible.value = true;
}

const registerEqFormRef = ref(null);

function addEqNameOk() {
  registerEqFormRef.value.validate((valid) => {
    if (valid) {
      addEqNameDialogVisible.value = false;
      linkAccount();
    }
  });
}

async function linkAccount() {
  try {
    // 注册WebAuthn
    const support = await checkBiometricSupport();
    const supported = support.supported;
    // const supported = false;
    const obj = await registerBegin({ username: store.state.app.userName, supported });
    if (obj.code !== 200) {
      ElMessage.error(obj.msg);
      return;
    }
    const options = obj.data;

    // 2. 转换选项格式
    const publicKey = {
      ...options,
      challenge: base64UrlToArrayBuffer(options.challenge || ''),
      user: {
        ...options.user,
        id: base64UrlToArrayBuffer(options.user.id || '')
      },
      // 兼容老浏览器：修正residentKey值
      authenticatorSelection: {
        ...options.authenticatorSelection
      },
      // 验证场景不需要 pubKeyCredParams/rp/user，后端也无需返回
      timeout: options.timeout || 60000,
    };

    // 3. 调用 WebAuthn API 创建凭证
    // ElMessage.info('请使用您的安全密钥、指纹或面部识别进行验证关联...');

    const credential = await navigator.credentials.create({
      publicKey: publicKey
    });

    // 3. 准备发送到服务器的数据（核心修复：transports字段）
    let transports = [];
    // 安全获取transports：兼容不同浏览器实现
    if (credential.response?.getTransports) {
      try {
        const rawTransports = credential.response.getTransports();
        // 确保transports是数组（防止返回Set/undefined）
        transports = Array.isArray(rawTransports)
          ? rawTransports
          : (rawTransports ? [rawTransports] : []);
      } catch (e) {
        transports = ['internal']; // 异常兜底
      }
    } else {
      transports = ['internal']; // 无getTransports方法时兜底
    }

    const credentialJson = {
      id: credential.id || '', // 空值兜底
      rawId: arrayBufferToBase64Url(credential.rawId),
      type: credential.type || 'public-key', // 兜底默认值
      response: {
        attestationObject: arrayBufferToBase64Url(
          credential.response?.attestationObject || new ArrayBuffer(0)
        ),
        clientDataJSON: arrayBufferToBase64Url(
          credential.response?.clientDataJSON || new ArrayBuffer(0)
        ),
        transports: transports // 确保是纯数组，无Set/undefined
      },
      req_id: options.req_id || '',
      name: registerEqForm.value.name || 'smart device',
    };

    // 5. 验证注册
    await registerComplete(credentialJson);

    ElMessage.success('注册成功！');
    getDevices().then(res => {
      authData.value = res.data || [];
    });

  } catch (error) {
    console.error('注册失败:', error);
    if (error.code !== 400) {
      ElMessage.error('注册失败');
    }
  }
}

function changeThem(item) {
  handleThem(item);
  them.value = item;
  store.dispatch("app/setThem", JSON.stringify(item));
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
    let resp = await sendEmailCodeApi({
      email: registerForm.value.email
    });
    if (resp.code === 200) {
      // 实现倒计时
      codeDisabled.value = true;
      countdown = 60;
      startCountdown();
      ElMessage({
        message: "验证码发送成功",
        type: "success",
      });
    }
  } catch (error) {
    console.error(error);
  }
}

function getEmailCode() {
  if (emailRule.test(registerForm.value.email)) {
    sendEmailCode();
  } else {
    ElMessage.error("请填写正确的邮箱号");
  }
}

function changeEmail() {
  editDialogVisible.value = true;
}

const registerFormRef = ref(null);

function editEmailOk() {
  registerFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const resp = await updateUserEmail({
          email: registerForm.value.email,
          verCode: registerForm.value.code,
        });
        if (resp.code === 200) {
          // 这里可以添加实际的登出逻辑，比如清除 token 或者重定向到登录页面
          store.dispatch("app/clearAvatar");
          store.dispatch("app/clearAuthorization");
          store.dispatch("app/clearUserRole");
          store.dispatch("app/clearNickName");
          store.dispatch("app/clearUserName");
          store.dispatch("app/clearUserEmail");
          store.dispatch("app/clearLoginType");
          ElMessage({
            message: "修改成功",
            type: "success",
          });
          // 重定向到根路径
          router.push("/");
        } else {
          ElMessage.error("修改失败!");
        }
        editDialogVisible.value = false;
      } catch (error) {
        console.error(error);
      }
    }
  });
}

const rules = {
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    {
      pattern: emailRule,
      type: "email",
      message: "邮箱格式不正确",
      trigger: ["blur", "change"],
    },
  ],
  code: [{ required: true, message: "请输入邮箱验证码", trigger: "blur" }],
};

const rulesEqName = {
  name: [{ required: true, message: "请输入设备名称", trigger: "blur" }],
};



function handleSuccess(response, file, fileList) {
  saveUrl.value = saveUrl.value + response.image_url;
  imageUrl.value = saveUrl.value;
}

function uploadImg() {
  if (uploadRef.value) {
    const input = uploadRef.value.$el.querySelector('input[type="file"]');
    if (input) {
      input.click();
    }
  }
}

function beforeUpload(file) {
  const isJpgOrPng = file.type === "image/jpeg" || file.type === "image/png";
  if (!isJpgOrPng) {
    ElMessage.error("上传图片只能是 JPG 或者 PNG 格式!");
  }
  return isJpgOrPng;
}

const qqActionTxt = {
  1: '关联QQ账号',
  2: '继续关联QQ账号',
  3: '解除关联QQ账号',
}

const clickQQFlow = ref(+store.state.app.bindQQ)

const githubActionTxt = {
  1: '关联GitHub账号',
  2: '继续关联GitHub账号',
  3: '解除关联GitHub账号',
}

const clickGitHubFlow = ref(+store.state.app.bindGitHub);

function cancelBindAccount() {
  store.dispatch("app/clearBindOtherAccount");
  if (clickQQFlow.value === 2) {
    clickQQFlow.value = 1;
  }

  if (clickGitHubFlow.value === 2) {
    clickGitHubFlow.value = 1;
  }
  bindAccountDialogVisible.value = false;
}

async function bindAccount() {
  try {
    if (clickQQFlow.value === 2) {
      try {
        const resp = await linkOtherUser({
          bindOtherAccount: store.state.app.bindOtherAccount,
          state: '1'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "关联成功",
            type: "success",
          });
          store.dispatch("app/setBindQQ", 3);
          clickQQFlow.value = 3;
        }
      } catch (error) {
        console.error(error);
      }
    }

    if (clickGitHubFlow.value === 2) {
      try {
        const resp = await linkOtherUser({
          bindOtherAccount: store.state.app.bindOtherAccount,
          state: '2'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "关联成功",
            type: "success",
          });
          clickGitHubFlow.value = 3;
        }
      } catch (error) {
        console.error(error);
      }
    }
  } catch (error) {
    if (clickQQFlow.value === 2) {
      clickQQFlow.value = 1;
    }

    if (clickGitHubFlow.value === 2) {
      clickGitHubFlow.value = 1;
    }
    console.error("Failed to bind account:", error);
  }
  store.dispatch("app/clearBindOtherAccount");
  bindAccountDialogVisible.value = false;
}

const pageQuery = (page) => {
  currentPage.value = page;
  fetchChatHisData();
};

async function fetchChatHisData() {
  try {
    state.loading = true; // 请求开始时设置为true
    const params = {
      pageSize: pageSize.value,
      pageIndex: currentPage.value,
      bindOtherAccount: store.state.app.bindOtherAccount,
      search_criteria: '{"sort": {"field": "create_date", "order": "desc"}}',
    };
    const response = await getOtherUserChatList(params);
    if (response.code === 200) {
      userNameTxt.value = response.data.other_username;
      userAvatarUrl.value = response.data.other_avatar;
      tableData.value = response.data.list.records;
      tableCount.value = response.data.list.total_count;
      state.loading = false; // 请求开始时设置为true
    }
  } catch (error) {
    console.error(error);
  }
}


async function linkQQ() {
  switch (clickQQFlow.value) {
    case 1:
      // console.log('关联QQ账号');
      store.dispatch("app/setBindOtherAccount", 'qq_' + store.state.app.userName + '_' + new Date().getTime());
      window.open(
        qqLoginUrl.value, // 要打开的URL（本地页面/远程链接均可）
        '关联QQ账号',       // 窗口名称（可用于复用窗口）
        'width=800,height=600,left=100,top=100' // 窗口特征（尺寸、位置等）
      );
      clickQQFlow.value = 2;
      break;
    case 2:
      await fetchChatHisData();
      bindAccountDialogVisible.value = true;
      break;
    case 3:
      // console.log('解除关联QQ账号');
      try {
        const resp = await noLinkOtherUser({
          state: '1'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "解除关联成功",
            type: "success",
          });
          store.dispatch("app/setBindQQ", 1);
          clickQQFlow.value = 1;
        }
      } catch (error) {
        console.error(error);
      }
      break;
    default:
      break;
  }
}

async function linkGitHub() {
  switch (clickGitHubFlow.value) {
    case 1:
      // console.log('关联GitHub账号');
      store.dispatch("app/setBindOtherAccount", 'github_' + store.state.app.userName + '_' + new Date().getTime());
      window.open(
        githubLoginUrl.value, // 要打开的URL（本地页面/远程链接均可）
        '关联GitHub账号',       // 窗口名称（可用于复用窗口）
        'width=800,height=600,left=100,top=100' // 窗口特征（尺寸、位置等）
      );
      clickGitHubFlow.value = 2;
      break;
    case 2:
      await fetchChatHisData();
      bindAccountDialogVisible.value = true;
      break;
    case 3:
      // console.log('解除关联GitHub账号');
      try {
        const resp = await noLinkOtherUser({
          state: '2'
        })
        if (resp.code === 200) {
          ElMessage({
            message: "解除关联成功",
            type: "success",
          });
          store.dispatch("app/setBindGitHub", 1);
          clickGitHubFlow.value = 1;
        }
      } catch (error) {
        console.error(error);
      }
      break;
    default:
      break;
  }
}

function forgetPwd() {
  const route = router.resolve({
    name: "Forget",
  });
  window.open(route.href, "_blank");
}

async function saveUserInfo() {
  let avatar = saveUrl.value;
  if (saveUrl.value === config.BASE_URL) {
    avatar = store.state.app.avatar;
  }
  const resp = await updateUser({
    avatar: avatar,
    nick_name: welcomStr.value,
  });
  if (resp.code === 200) {
    store.dispatch("app/setNickName", welcomStr.value);
    store.dispatch("app/setAvatar", imageUrl.value);
    ElMessage({
      message: "修改成功",
      type: "success",
    });
  } else {
    ElMessage.error("修改失败");
  }
}

let oldTag = ref(colorList.value[0].tag);

if (store.state.app.mainColor) {
  oldTag = ref(JSON.parse(store.state.app.mainColor).tag);
}

function selectColor(item) {
  checkThemId.value = item.id;
  // console.log(oldTag.value);
  if (oldTag.value) {
    document.documentElement.classList.remove(oldTag.value);
  }

  if (item.tag) {
    document.documentElement.classList.add(item.tag);
  }
  oldTag.value = item.tag;
  store.dispatch("app/setMainColor", JSON.stringify(item));
}

function closeKeyLogin() {
  store.dispatch("app/clearNoKeyLogin");
  isNoKeyLogin.value = true;
  ElMessage.success(`${biometricType.value}登录已关闭！`);
}

async function noKeyLogin() {
  // 开始设备验证
  try {
    // 注册WebAuthn
    const support = await checkBiometricSupport();
    if (!support.supported) {
      ElMessage.error('当前设备不支持生物验证, 请使用其他验证方式！');
      return;
    }
    const supported = support.supported;
    // const supported = false;
    const obj = await loginBegin({ username: store.state.app.userName, supported });
    if (obj.code !== 200) {
      ElMessage.error(obj.msg);
      return;
    }

    const options = obj.data;

    // 验证场景：仅处理必要参数，删除 rp/user（验证场景不需要）
    const publicKey = {
      ...options,
      challenge: base64UrlToArrayBuffer(options.challenge || ''),
      allowCredentials: options.allowCredentials?.map(cred => ({
        ...cred,
        id: base64UrlToArrayBuffer(cred.id || '')
      })) || [],
      // 验证场景不需要 pubKeyCredParams/rp/user，后端也无需返回
      timeout: options.timeout || 60000,
    };

    // 前置校验：确保 allowCredentials 非空
    if (!publicKey.allowCredentials.length) {
      throw new Error('未找到匹配的验证凭证');
    }

    // 3. 调用 WebAuthn API 创建凭证
    // ElMessage.info('请使用您的安全密钥、指纹或面部识别进行验证...');

    // 关键：验证场景用 get，不是 create！！！
    const credential = await navigator.credentials.get({
      publicKey: publicKey
    });

    // 后续处理凭证逻辑不变（注意：验证场景的 response 字段和注册场景不同）
    const credentialJson = {
      id: credential.id,
      rawId: arrayBufferToBase64Url(credential.rawId),
      type: credential.type,
      response: {
        authenticatorData: arrayBufferToBase64Url(credential.response.authenticatorData),
        clientDataJSON: arrayBufferToBase64Url(credential.response.clientDataJSON),
        signature: arrayBufferToBase64Url(credential.response.signature),
        userHandle: credential.response.userHandle ? arrayBufferToBase64Url(credential.response.userHandle) : null
      },
      req_id: options.req_id || ''
    };
    // 5. 验证身份信息
    const result = await loginComplete(credentialJson);

    ElMessage.success(`${biometricType.value}登录已开启！`);
    const noKeyLoginObj = {
      avatar: result.data.userinfo.avatar || '',
      gid: result.data.userinfo.userName,
      biometricType: biometricType.value,
    }
    store.dispatch("app/setNoKeyLogin", JSON.stringify(noKeyLoginObj));
    isNoKeyLogin.value = false;
  } catch (error) {
    console.error('身份验证失败:', error.name, error.message);
    if (error.code !== 400) {
      ElMessage.error('身份验证失败');
    }
  }
}

onMounted(async function () {
  let colorObj = store.state.app.mainColor;
  if (colorObj) {
    checkThemId.value = JSON.parse(colorObj).id;
  }
  document.documentElement.querySelector("title").innerText = "我的主页";
  // 调用检测函数
  const support = await checkBiometricSupport();
  isSupportBiometric.value = support.supported && loginType === 'voatalk';
  biometricType.value = support.biometricType || '';
  switch (biometricType.value) {
    case 'Face/Touch ID':
      authIcon.value = 'icon faceid';
      break;
    case '指纹/面部':
    case 'Touch ID':
      authIcon.value = 'icon fingerprint';
      break;
    case 'Windows Hello':
      authIcon.value = 'icon windowshello';
      break;
    default:
      break;
  }
  isNoKeyLogin.value = store.state.app.noKeyLogin === '' || JSON.parse(store.state.app.noKeyLogin).gid !== store.state.app.userName;
  // 获取设备列表
  getDevices().then(res => {
    authData.value = res.data || [];
  });
});
</script>

<style scoped>
.user-edit {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  height: calc(100vh - 120px);
}

:deep(.el-upload.el-upload--picture-card),
:deep(.el-upload-list--picture-card .el-upload-list__item-actions),
:deep(.el-upload-list--picture-card .el-upload-list__item-thumbnail) {
  border-radius: 50% !important;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  border: none !important;
}

.nick-name {
  margin-top: 35px;
}

.avater {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
}

.get-code {
  cursor: pointer;
  user-select: none;
  border: none;
  padding: 0;
  margin: 0;
}

.avater:hover::after {
  content: "点击更换头像";
  position: absolute;
  font-size: 16px;
  color: #fff;
  width: inherit;
  height: inherit;
  top: 90px;
  left: 30px;
  background: transparent;
}

.avater:hover::before {
  position: absolute;
  top: 20px;
  left: 0;
  content: "";
  width: inherit;
  height: inherit;
  border-radius: 50%;
  background-color: rgb(0, 0, 0, 0.4);
}

.avater img {
  object-fit: cover;
  width: inherit;
  height: inherit;
  border-radius: 50%;
}

.button-group .el-button {
  margin: 15px 0;
  width: 330px;
  border: none;
  font-size: 16px;
}

:deep(.el-input__wrapper) {
  transition: all 0.1s;
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

.opt {
  display: flex;
  flex-direction: column;
}

.opt .el-button {
  width: 330px;
  margin: 10px 0;
  border: none;
  box-shadow: none;
}

.register-btn {
  border: none;
}

.them-color {
  width: 330px;
  display: flex;
  flex-wrap: wrap;
}

.them-color .item {
  width: 50px;
  height: 50px;
  border-radius: 5px;
  margin: 8px;
  cursor: pointer;
}

.them-color .item i {
  line-height: 50px;
  text-align: center;
  color: #fff;
  font-size: 26px;
  display: none;
}

.them-color .item.checked i {
  display: block;
}

.opt p {
  text-align: center;
  color: var(--el-text-color-primary);
  position: relative;
}

.opt p::before,
.opt p::after {
  position: absolute;
  content: "";
  background: var(--w-e-textarea-border-color);
  height: 1px;
  width: 35%;
  top: 50%;
}

.opt p.them-text::before,
.opt p.them-text::after {
  width: 30%;
}

.opt p::before {
  left: 1px;
}

.opt p::after {
  right: 1px;
}

:deep(.them-item .el-form-item__content) {
  justify-content: end;
}

.me-icon .icon {
  width: 16px;
  height: 16px;
  display: block;
  background-color: var(--me-report-text-color);
}

.el-dropdown-menu__item:not(.is-disabled):focus .me-icon .icon,
.el-dropdown-menu__item:not(.is-disabled):hover .me-icon .icon,
.el-button:hover .me-icon .icon {
  background-color: var(--el-dropdown-menuItem-hover-color);
}

.me-icon .icon.theme-os {
  -webkit-mask-image: url("@/assets/images/theme-os.svg");
  mask-image: url("@/assets/images/theme-os.svg");
}

.me-icon .icon.theme-light {
  -webkit-mask-image: url("@/assets/images/theme-light.svg");
  mask-image: url("@/assets/images/theme-light.svg");
}

.me-icon .icon.theme-dark {
  -webkit-mask-image: url("@/assets/images/theme-dark.svg");
  mask-image: url("@/assets/images/theme-dark.svg");
}

.email-setting {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.logintext {
  display: flex;
  height: 50px;
  align-items: center;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.user-name-txt {
  font-size: 20px;
  font-weight: 500;
  margin: 0;
  margin-left: 6px;
  padding: 0;
  color: var(--el-text-color-primary);
}

.me-pagination {
  width: inherit;
  display: flex;
  justify-content: flex-end;
}

.me-pagination span {
  font-size: 14px;
  color: var(--el-text-color-primary);
  line-height: 45px;
  margin-right: 20px;
}

.bind-warning {
  margin: 10px 0;
  width: 350px;
}

@media (max-width: 768px) {
  .them-color {
    margin-bottom: 5px;
  }
}

.auth-icon .icon {
  width: 16px;
  height: 16px;
  display: block;
  background-color: #fff;
}

.auth-icon .icon.fingerprint {
  -webkit-mask-image: url("@/assets/images/fingerprint.svg");
  mask-image: url("@/assets/images/fingerprint.svg");
}

.auth-icon .icon.faceid {
  -webkit-mask-image: url("@/assets/images/faceid.svg");
  mask-image: url("@/assets/images/faceid.svg");
}

.auth-icon .icon.windowshello {
  -webkit-mask-image: url("@/assets/images/windowshello.svg");
  mask-image: url("@/assets/images/windowshello.svg");
}

.auth-data .txt {
  font-size: 12px;
}

.auth-data .el-table {
  height: 180px;
  margin-top: 10px;
}
</style>
