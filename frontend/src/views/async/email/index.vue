<template>
  <div class="body">
    <div class="data-inner">
      <div class="header">
        <el-form :inline="true" :model="state" class="demo-form-inline">
          <el-form-item label="邮件主题">
            <el-input
              v-model="state.subject"
              placeholder="模糊搜索用户名或昵称"
              size="large"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-button size="large" type="primary" @click="fetchData"
              >查 询</el-button
            >
          </el-form-item>
        </el-form>
        <div class="option">
          <p>数据列表</p>
          <div>
            <el-button
              size="large"
              type="primary"
              :icon="Edit"
              @click="openEmailEdit"
              >写邮件</el-button
            >
            <el-button
              size="large"
              type="danger"
              @click="batchDel"
              :icon="Delete"
              >删 除</el-button
            >
          </div>
        </div>
      </div>
      <div class="data-view">
        <el-table
          v-loading="state.loading"
          :data="tableData"
          border
          stripe
          style="width: 100%"
          @select="changeCheckBox"
          @select-all="changeCheckBox"
        >
          <el-table-column type="selection" width="55" />
          <!-- 表格列定义 -->
          <el-table-column
            fixed
            prop="subject"
            label="邮件主题"
            min-width="170"
          />
          <el-table-column prop="body" label="邮件内容" min-width="250">
            <template #default="{ row }">
              <el-popover
                placement="bottom"
                title="发送结果："
                content=""
                trigger="hover"
                width="300"
              >
                <div v-html="row.body"></div>
                <template #reference>
                  <div class="text-truncate">{{ row.body }}</div>
                </template>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column prop="send_users" label="收件人邮箱" min-width="180">
            <template #default="{ row }">
              <el-popover
                placement="bottom"
                title=""
                content=""
                trigger="hover"
                width="200"
              >
                <el-tag
                  v-for="(ev, index) in JSON.parse(row.send_users)"
                  :key="index"
                  :type="typeList[index % typeList.length]"
                  style="margin-bottom: 6px"
                  >{{ ev }}</el-tag
                >
                <template #reference>
                  <div class="text-truncate">
                    <el-tag
                      v-for="(ev, index) in JSON.parse(row.send_users)"
                      :key="index"
                      :type="typeList[index % typeList.length]"
                      >{{ ev }}</el-tag
                    >
                  </div>
                </template>
              </el-popover>
            </template>
          </el-table-column>
          <el-table-column
            prop="create_date"
            label="发送时间"
            min-width="160"
          />
          <el-table-column fixed="right" label="操作" min-width="120">
            <template v-slot="scope">
              <el-button
                link
                type="primary"
                size="small"
                @click="openEditDialog(scope.row)"
              >
                查看
              </el-button>
              <el-button
                link
                type="danger"
                size="small"
                @click="handleDelete(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="me-pagination">
          <span>共 {{ tableCount }} 条</span>
          <el-pagination
            layout="prev, pager, next"
            :page-size="pageSize"
            :total="tableCount"
            @current-change="pageQuery"
          />
        </div>

        <el-dialog
          v-model="centerDialogVisible"
          title="删除用户"
          width="400"
          align-center
        >
          <span>确定删除所选邮件记录？此操作不可恢复</span>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="centerDialogVisible = false">取消</el-button>
              <el-button type="danger" @click="deleteUserOk"> 确定 </el-button>
            </div>
          </template>
        </el-dialog>

        <el-dialog
          v-model="infoDialog"
          title="发送详情"
          width="980"
          style="max-height: 600px"
          align-center
        >
          <el-form :model="form" label-width="100px" class="custom-form">
            <el-form-item
              prop="subject"
              label="邮件主题："
              class="custom-form-item"
            >
              <el-input
                v-model="form.subject"
                style="width: 240px"
                placeholder="请填写邮件主题"
                :disabled="true"
              ></el-input>
            </el-form-item>
            <el-form-item
              prop="user_list"
              label="收件人："
              class="custom-form-item"
            >
              <el-select
                v-model="value"
                multiple
                filterable
                clearable
                :reserve-keyword="false"
                :collapse-tags="true"
                :collapse-tags-tooltip="true"
                placeholder="请选择收件人"
                style="width: 240px"
                :disabled="true"
              >
                <el-option
                  v-for="item in options"
                  :key="item.id"
                  :label="item.nick_name"
                  :value="item.email"
                >
                  <div class="flex items-center">
                    <el-avatar
                      v-if="item.avatar"
                      :src="item.avatar"
                      size="small"
                    />
                    <el-avatar
                      v-else
                      src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                      size="small"
                    />
                    <span class="lable-text">{{ item.nick_name }}</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item
              prop="body"
              label="邮件内容："
              class="custom-form-item"
            >
              <div v-html="infoHtml" class="info-html"></div>
            </el-form-item>
          </el-form>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="infoDialog = false">关闭</el-button>
            </div>
          </template>
        </el-dialog>

        <el-drawer
          v-model="editEmail"
          title="写邮件"
          :with-header="true"
          size="100%"
        >
          <el-form :model="form" label-width="100px" class="custom-form">
            <el-form-item
              prop="subject"
              label="邮件主题："
              class="custom-form-item"
            >
              <el-input
                v-model="form.subject"
                style="width: 240px"
                placeholder="请填写邮件主题"
              ></el-input>
            </el-form-item>
            <el-form-item
              prop="user_list"
              label="收件人："
              class="custom-form-item"
            >
              <el-select
                v-model="value"
                multiple
                filterable
                clearable
                :reserve-keyword="false"
                :collapse-tags="true"
                :collapse-tags-tooltip="true"
                placeholder="请选择收件人"
                style="width: 240px"
              >
                <el-option
                  v-for="item in options"
                  :key="item.id"
                  :label="item.nick_name"
                  :value="item.email"
                >
                  <div class="flex items-center">
                    <el-avatar
                      v-if="item.avatar"
                      :src="item.avatar"
                      size="small"
                    />
                    <el-avatar
                      v-else
                      src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                      size="small"
                    />
                    <span class="lable-text">{{ item.nick_name }}</span>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item
              prop="body"
              label="邮件内容："
              class="custom-form-item"
            >
              <div style="border: 1px solid var(--w-e-textarea-border-color)">
                <Toolbar
                  style="
                    border-bottom: 1px solid var(--w-e-textarea-border-color);
                  "
                  :editor="editorRef"
                  :defaultConfig="toolbarConfig"
                  mode="default"
                />
                <Editor
                  style="height: 600px; overflow-y: hidden"
                  v-model="valueHtml"
                  :defaultConfig="editorConfig"
                  mode="default"
                  @onCreated="handleCreated"
                />
              </div>
            </el-form-item>
          </el-form>
          <template #footer>
            <div class="dialog-footer">
              <el-button @click="editEmail = false">取消</el-button>
              <el-button type="primary" @click="sendMyEmail">发送</el-button>
            </div>
          </template>
        </el-drawer>
      </div>
    </div>
  </div>
</template>

<script setup>
import "@wangeditor/editor/dist/css/style.css"; // 引入 css
import { ref, reactive, onMounted, shallowRef, onBeforeUnmount } from "vue";
import { Edit, Delete } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus"; // 引入 ElMessage 组件
import { findListPage, emailDel, findUsers, sendEmail } from "@/api/emailLogs";
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";

const tableData = ref([]);
const tableCount = ref(0);
// 当前页码
const currentPage = ref(1);
const userNameList = ref("");

const typeList = ["primary", "success", "info", "warning", "danger"];

// 每页显示数量
const pageSize = ref(20);
const editEmail = ref(false);
const selectedUser = ref(null);
const valueHtml = ref("<p><br></p>");
const infoHtml = ref("");
const editorRef = shallowRef();
const centerDialogVisible = ref(false);
const infoDialog = ref(false);
let state = reactive({
  open: false,
  subject: "",
  loading: false,
  delete_ids: "",
  user_name_list: "",
});

const options = ref([]);
const value = ref([]);

const form = ref({
  subject: null,
  body: null,
  send_users: [],
});

const toolbarConfig = {};
const editorConfig = { placeholder: "请输入内容..." };

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
  const editor = editorRef.value;
  if (editor == null) return;
  editor.destroy();
});

const handleCreated = (editor) => {
  editorRef.value = editor; // 记录 editor 实例，重要！
};

function close() {
  state.open = false;
}
const fetchData = async () => {
  try {
    state.loading = true; // 请求开始时设置为true
    const params = {
      pageSize: pageSize.value,
      pageIndex: currentPage.value,
    };
    // 有参数就采用模糊查询
    if (state.user_name !== "") {
      params.search_criteria = `{"subject": {"value": "${state.subject}", "operator": "like"}, "sort": {"field": "create_date", "order": "desc"}}`;
    }
    const response = await findListPage(params);
    tableData.value = response.data.records;
    tableCount.value = response.data.total_count;
    state.loading = false; // 请求开始时设置为true
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
};

const openEmailEdit = function () {
  findUsers()
    .then((obj) => {
      options.value = obj.data;
    })
    .catch((err) => {
      console.log(err);
    });
  valueHtml.value =
    '<p style="text-indent: 2em;"><img src="data:image/png;base64,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" alt="logo" data-href="" style="width: 50.50px;height: 52.61px;"></p>';
  value.value = [];
  form.value.subject = null;
  editEmail.value = true;
};

async function openEditDialog(row) {
  const obj = await findUsers();
  infoDialog.value = true;
  options.value = obj.data;
  value.value = JSON.parse(row.send_users);
  infoHtml.value = row.body;
  form.value.subject = row.subject;
}

function sendMyEmail() {
  if (form.value.subject === null) {
    ElMessage.warning("请填写邮件主题");
    return;
  }

  if (value.value.length <= 0) {
    ElMessage.warning("请选择收件人");
    return;
  }

  if (valueHtml.value === "<p><br></p>") {
    ElMessage.warning("请填写邮件内容");
    return;
  }

  form.value.body = valueHtml.value;
  form.value.send_users = value.value;
  sendEmail(form.value)
    .then((res) => {
      editEmail.value = false;
      fetchData();
    })
    .catch((err) => {
      console.log(err);
    });
}

const submitEdit = async (updatedUser) => {
  try {
    await ApiUserExit(updatedUser);
    fetchData();
  } catch (error) {
    console.error("Failed to update user:", error);
  }
};

const pageQuery = (page) => {
  currentPage.value = page;
  fetchData();
};

const changeCheckBox = (list) => {
  if (list.length > 0) {
    state.delete_ids = list.map((item) => item.id).join(",");
  } else {
    state.delete_ids = "";
  }
};

const batchDel = () => {
  if (state.delete_ids === "") {
    ElMessage.warning("请勾选需要删除的邮件");
  } else {
    centerDialogVisible.value = true;
  }
};

const deleteUserOk = async () => {
  try {
    let params = { id: state.delete_ids + "" };
    await emailDel(params);
    ElMessage({
      message: "删除成功",
      type: "success",
    });
    fetchData();
  } catch (error) {
    console.error("Failed to delete user:", error);
    ElMessage({
      message: "删除失败",
      type: "error",
    });
  }
  centerDialogVisible.value = false;
};

const handleDelete = (row) => {
  centerDialogVisible.value = true;
  userNameList.value = row.user_name;
  state.delete_ids = row.id;
};

onMounted(() => {
  fetchData();
  document.documentElement.querySelector("title").innerText = "邮件管理";
});
</script>

<style scoped>
.body {
  display: flex;
  justify-content: center;
  margin: 0 2px;
}

.body .data-inner {
  width: 65vw;
  padding: 15px 0;
}

@media (max-width: 1024px) {
  .body .data-inner {
    width: 95vw;
  }
}

.header {
  width: 100%;
  height: 80px;
  background: var(--el-bg-color);
  box-shadow: 0 2px 10px rgb(0, 0, 0, 0.1);
  border-radius: 5px;
  box-sizing: border-box;
}

.header .option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 10px 0;
}

.header .option p {
  font-size: 14px;
  padding-left: 10px;
  color: var(--el-text-color-primary);
  border-left: 3px solid #3e8ef7;
}

.el-form.custom-form {
  display: block !important;
}

.el-form-item.custom-form-item {
  margin-bottom: 18px !important;
}

.el-form {
  display: flex;
  height: inherit;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

.el-input {
  width: 200px;
}

.el-form-item {
  margin: 0 !important;
}

:deep(.el-form-item__label) {
  line-height: 40px !important;
}

.el-table {
  height: 70vh !important;
}

.el-table thead {
  color: rgb(0, 0, 0, 0.8) !important;
}

:deep(.el-table .cell) {
  padding: 4px 12px;
}

.data-view {
  width: 100%;
  background: var(--el-bg-color);
  box-sizing: border-box;
  box-shadow: 0 2px 12px rgb(0, 0, 0, 0.1);
  position: relative;
  margin-top: 70px;
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

/* 隐藏 el-table 的无数据提示 */
:deep(.el-table__empty-block) {
  opacity: 0 !important;
}

.push-img {
  color: var(--el-text-color-primary);
  text-decoration: none;
  margin-right: 6px;
  font-size: 14px;
}

.push-img:hover {
  color: var(--el-color-primary);
}

.flex.items-center {
  display: flex;
  align-items: center;
}

.flex.items-center .lable-text {
  margin-left: 4px;
}

.text-truncate {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.info-html {
  height: 300px;
  width: 100%;
  overflow: auto;
}
</style>
