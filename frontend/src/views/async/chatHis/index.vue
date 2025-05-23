<template>
  <div class="body">
    <div class="data-inner">
      <div class="header">
        <el-form :inline="true" :model="state" class="demo-form-inline">
          <el-form-item label="对话名称">
            <el-input
              v-model="state.user_name"
              placeholder="模糊搜索历史对话"
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
            <el-button size="large" type="danger" @click="batchDel"
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
            prop="talk_name"
            label="对话名称"
            min-width="450"
          />
          <el-table-column
            fixed
            prop="nick_name"
            label="对话拥有者"
            min-width="200"
          />
          <el-table-column
            fixed
            prop="create_date"
            label="对话产生的时间"
            min-width="200"
          />
          <el-table-column fixed="right" label="操作" min-width="180">
            <template v-slot="scope">
              <el-button
                link
                type="primary"
                size="small"
                @click="openChatInfo(scope.row)"
              >
                详情
              </el-button>
              <el-button
                link
                type="primary"
                size="small"
                @click="openEditDialog(scope.row)"
              >
                编辑
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
      </div>
    </div>
  </div>

  <el-dialog
    v-model="centerDialogVisible"
    title="删除对话"
    width="400"
    align-center
  >
    <span>确定删除，对话内容将不可恢复</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteUserOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog
    v-model="editDialogVisible"
    title="编辑对话名称"
    width="400"
    align-center
  >
    <el-input size="large" v-model="chatTitle" />
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="editMsgOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { ElMessage } from "element-plus"; // 引入 ElMessage 组件
import { queryChat, editChatName, deleteChat } from "@/api/aiChat";
import { useStore } from "vuex"; // Use Vuex's useStore function
import router from "@/router";

const store = useStore(); // Initialize the store

const tableData = ref([]);

const tableCount = ref(0);
// 当前页码
const currentPage = ref(1);

const chatTitle = ref("");

const chatId = ref(-1);

// 每页显示数量
const pageSize = ref(20);
let editDialogVisible = ref(false);

const centerDialogVisible = ref(false);

let state = reactive({
  user_name: "",
  loading: false,
  delete_ids: "",
  user_name_list: "",
});

function close() {
  state.open = false;
}

async function openChatInfo(row) {
  store.dispatch("app/setSliderData", {
    talk_id: row.talk_id,
    talk_name: row.talk_name || "",
    type: "open",
  });
  router.replace("/home/chat/" + row.talk_id);
}

const fetchData = async () => {
  try {
    state.loading = true; // 请求开始时设置为true
    const params = {
      pageSize: pageSize.value,
      pageIndex: currentPage.value,
    };
    params.search_criteria =
      '{"sort": {"field": "create_date", "order": "desc"}}';
    // 有参数就采用模糊查询
    if (state.user_name !== "") {
      params.search_criteria = `{"talk_name": {"value": "${state.user_name}", "operator": "like"}, "sort": {"field": "create_date", "order": "desc"}}`;
    }
    const response = await queryChat(params);
    tableData.value = response.data.records;
    tableCount.value = response.data.total_count;
    state.loading = false; // 请求开始时设置为true
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
};

const openEditDialog = (row) => {
  chatTitle.value = row.talk_name;
  chatId.value = row.talk_id;
  editDialogVisible.value = true;
};

async function editMsgOk() {
  await editChatName({ talk_id: chatId.value, talk_name: chatTitle.value });
  fetchData();
  editDialogVisible.value = false;
  store.dispatch("app/setSliderData", { fetch: true });
}

const pageQuery = (page) => {
  currentPage.value = page;
  fetchData();
};

const changeCheckBox = (list) => {
  if (list.length > 0) {
    state.delete_ids = list.map((item) => item.talk_id).join(",");
  } else {
    state.delete_ids = "";
  }
};

const batchDel = () => {
  if (state.delete_ids === "") {
    ElMessage.warning("请勾选需要删除的对话");
  } else {
    centerDialogVisible.value = true;
  }
};

const deleteUserOk = async () => {
  try {
    let params = { talk_id: state.delete_ids + "" };
    await deleteChat(params);
    ElMessage({
      message: "删除成功",
      type: "success",
    });
    fetchData();
    store.dispatch("app/setSliderData", { fetch: true });
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
  state.delete_ids = row.talk_id;
};

onMounted(() => {
  fetchData();
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
}

.header {
  width: 100%;
  height: 80px;
  background: var(--el-bg-color);
  box-shadow: 0 2px 10px rgb(0, 0, 0, 0.1);
  border-radius: 5px;
  box-sizing: border-box;
  margin-top: 20px;
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

.el-form {
  display: flex;
  height: inherit;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}

.el-form-item {
  margin: 0 !important;
}

:deep(.el-form-item__label) {
  line-height: 40px !important;
}

.el-table {
  height: 66vh !important;
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

.text-truncate {
  max-width: 170px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 隐藏 el-table 的无数据提示 */
:deep(.el-table__empty-block) {
  opacity: 0 !important;
}
</style>
