<template>
  <div class="body">
    <div class="header">
      <el-form :inline="true" :model="state" class="demo-form-inline">
        <el-form-item label="用户名">
          <el-input
            v-model="state.user_name"
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
        <el-button size="large" type="danger" @click="batchDel"
          >删 除</el-button
        >
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
          prop="user_name"
          label="用户名"
          min-width="150"
        />
        <el-table-column prop="nick_name" label="昵称" min-width="150" />
        <el-table-column label="是否为管理员" min-width="120">
          <template v-slot="scope">
            <el-tag round type="info" v-if="scope.row.super_admin === 0">否</el-tag>
            <el-tag round type="success" v-if="scope.row.super_admin === 1">是</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="用户状态" min-width="120">
          <template v-slot="scope">
            <el-tag type="success" v-if="scope.row.user_state === 1">正常</el-tag>
            <el-tag type="info" v-if="scope.row.user_state === 0">停用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column
          prop="last_login_time"
          label="最后登录时间"
          min-width="200"
        />
        <el-table-column fixed="right" label="操作" min-width="120">
          <template v-slot="scope">
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

      <el-dialog
        v-model="centerDialogVisible"
        title="删除用户"
        width="400"
        align-center
      >
        <span>确定删除用户: {{ userNameList }} 的账号？</span>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="centerDialogVisible = false">取消</el-button>
            <el-button type="danger" @click="deleteUserOk"> 确定 </el-button>
          </div>
        </template>
      </el-dialog>
    </div>

    <EditUserDialog
      @close="close"
      v-if="state.open"
      :user="selectedUser"
      @submit="submitEdit"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { ElMessage } from "element-plus"; // 引入 ElMessage 组件
import { ApiUserFindListPage, ApiUserDel, ApiUserExit } from "@/api/apiUser";
import EditUserDialog from "./components/EditUserDialog.vue"; // 引入组件

const tableData = ref([]);
const tableCount = ref(0);
// 当前页码
const currentPage = ref(1);
const userNameList = ref("");

// 每页显示数量
const pageSize = ref(20);
let editDialogVisible = ref(false);
const selectedUser = ref(null);
const centerDialogVisible = ref(false);
let state = reactive({
  open: false,
  user_name: "",
  loading: false,
  delete_ids: "",
  user_name_list: "",
});

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
      params.search_criteria = `{"logic_operator": "or", "user_name": {"value": "${state.user_name}", "operator": "like"}, "nick_name": {"value": "${state.user_name}", "operator": "like"}}`;
    }
    const response = await ApiUserFindListPage(params);
    tableData.value = response.data.records;
    tableCount.value = response.data.total_count;
    state.loading = false; // 请求开始时设置为true
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
};

const openEditDialog = (row) => {
  console.log("Opening edit dialog for:", row); // 确认函数调用
  selectedUser.value = row;
  state.open = true;
};

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
    userNameList.value = list.map((item) => item.user_name).join("、");
  }
};

const batchDel = () => {
  centerDialogVisible.value = true;
};

const deleteUserOk = async () => {
  try {
    let params = { id: state.delete_ids + "" };
    await ApiUserDel(params);
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
});
</script>

<style scoped>
.header {
  width: 100%;
  height: 80px;
  background: #fff;
  border-radius: 5px;
  box-sizing: border-box;
  box-shadow: 0 2px 12px rgb(0, 0, 0, 0.1);
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
  color: rgb(0, 0, 0, 0.6);
  border-left: 3px solid #3e8ef7;
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
  max-width: 1115px;
}

.el-table thead {
  color: rgb(0, 0, 0, 0.8) !important;
}

:deep(.el-table .cell) {
  padding: 4px 12px;
}

.data-view {
  width: 100%;
  background: #fff;
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
  color: rgb(0, 0, 0, 0.6);
  line-height: 45px;
  margin-right: 20px;
}

/* 隐藏 el-table 的无数据提示 */
:deep(.el-table__empty-block) {
  opacity: 0 !important;
}
</style>
