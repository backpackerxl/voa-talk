<template>
  <div class="body">
    <div class="data-inner">
      <div class="header">
        <el-form :inline="true" :model="state">
          <div>
            <el-form-item label="模糊搜索：">
              <el-input style="width: 200px;" v-model="state.user_name" placeholder="模糊搜索对话名称" clearable />
            </el-form-item>
            &nbsp;&nbsp;
            <el-form-item label="时间：">
              <el-config-provider :locale="zhCn">
                <el-date-picker v-model="state.create_date" type="datetimerange" :shortcuts="shortcuts"
                  format="YYYY-MM-DD HH" range-separator="-" start-placeholder="开始日期" end-placeholder="结束日期"
                  :show-footer="false" style="width: 250px;" />
              </el-config-provider>
            </el-form-item>
          </div>
          <el-form-item>
            <el-button type="primary" @click="fetchData" :icon="Search">查 询</el-button>
          </el-form-item>
        </el-form>
        <div class="option">
          <p>数据列表</p>
          <div>
            <el-button type="danger" @click="batchDel" :icon="Delete">删 除</el-button>
          </div>
        </div>
      </div>
      <div class="data-view">
        <el-table v-loading="state.loading" :data="tableData" border stripe style="width: 100%" @select="changeCheckBox"
          @select-all="changeCheckBox">
          <el-table-column type="selection" width="55" />
          <!-- 表格列定义 -->
          <el-table-column fixed prop="talk_name" label="对话名称" min-width="300" />
          <el-table-column prop="nick_name" label="对话拥有者" min-width="200" />
          <el-table-column prop="create_date" label="对话产生的时间" min-width="200" />
          <el-table-column fixed="right" label="操作" min-width="180">
            <template v-slot="scope">
              <el-button link type="primary" size="small" @click="openChatInfo(scope.row)">
                详情
              </el-button>
              <el-button link type="primary" size="small" @click="openEditDialog(scope.row)">
                编辑
              </el-button>
              <el-button link type="danger" size="small" @click="handleDelete(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="me-pagination">
          <span>共 {{ tableCount }} 条</span>
          <el-pagination layout="prev, pager, next" :page-size="pageSize" :total="tableCount"
            @current-change="pageQuery" />
        </div>
      </div>
    </div>
  </div>

  <el-dialog v-model="centerDialogVisible" title="删除对话" width="400" align-center>
    <span>确定删除，对话内容将不可恢复</span>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteUserOk"> 确定 </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="editDialogVisible" title="编辑对话名称" width="400" align-center>
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
import { Delete, Search } from "@element-plus/icons-vue"; // 引入图标
import { ElConfigProvider } from 'element-plus';
import { formatFullDateTime, shortcuts, getOneMonthTimeRange } from "@/utils/tools";
import zhCn from 'element-plus/es/locale/lang/zh-cn';

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
  create_date: getOneMonthTimeRange(),
  loading: false,
  delete_ids: "",
  user_name_list: "",
});

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
    params.search_criteria = {
      "talk_name": { "value": state.user_name, "operator": "like" },
      "sort": { "field": "create_date", "order": "desc" }
    };

    if (state.create_date) {
      const stm = formatFullDateTime(state.create_date[0]);
      const etm = formatFullDateTime(state.create_date[1]);
      params.search_criteria.create_date = {
        "value": [{ "value": stm, "operator": "gte" }, { "value": etm, "operator": "lte" }],
        "operator": "range"
      };
    }
    params.search_criteria = JSON.stringify(params.search_criteria);
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
  document.documentElement.querySelector("title").innerText = "历史对话";
});
</script>

<style scoped>
.body {
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.body .data-inner {
  padding: 5px;
  width: calc(100% - 120px);
}

.header {
  width: 100%;
  height: 70px;
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

.el-form {
  display: flex;
  height: inherit;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}

.el-form-item {
  margin: 0 !important;
}

.el-table {
  height: calc(100vh - 300px) !important;
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
</style>
