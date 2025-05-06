<template>
  <el-dialog
    v-model="state.open"
    title="编辑用户"
    width="520"
    @close="close"
    class="custom-dialog"
  >
    <el-form :model="form" label-width="120px" class="custom-form">
      <el-form-item label="登录账户：" class="custom-form-item">
        <el-input v-model="form.user_name" disabled></el-input>
      </el-form-item>
      <el-form-item label="姓名：" class="custom-form-item">
        <el-input v-model="form.nick_name" disabled></el-input>
      </el-form-item>
      <el-form-item label="是否为管理员：" class="custom-form-item">
        <el-switch v-model="form.super_admin"></el-switch>
      </el-form-item>
      <el-form-item label="用户状态：" class="custom-form-item">
        <el-switch v-model="form.user_state"></el-switch>
      </el-form-item>
      <el-form-item label="邮箱：" class="custom-form-item">
        <el-input v-model="form.email" disabled></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="close" class="custom-button">取消</el-button>
      <el-button type="primary" @click="submitEdit" class="custom-button"
        >保存</el-button
      >
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, reactive, defineEmits } from "vue";

let emit = defineEmits(["close", "submit"]);
const props = defineProps({
  user: Object,
});

function close() {
  emit("close");
}

const form = ref({
  user_name: "",
  nick_name: "",
  super_admin: false,
  user_state: false,
  email: "",
  id: "",
});
let state = reactive({
  open: true,
});

watch(
  () => props.user,
  (newUser) => {
    console.log("New user data received in dialog:", newUser); // 检查数据接收
    if (newUser) {
      form.value.user_name = newUser.user_name || "";
      form.value.nick_name = newUser.nick_name || "";
      form.value.id = newUser.id || "";
      form.value.super_admin = newUser.super_admin === 1;
      form.value.user_state = newUser.user_state === 1;
      form.value.email = newUser.email || "";
    }
  },
  { immediate: true }
);

const submitEdit = async () => {
  emit("submit", form.value);
  close();
};
</script>

<style scoped>
:deep(.el-dialog__header) {
  background-color: #f5f5f5;
  border-bottom: 1px solid #ebeef5;
}

.custom-form-item {
  margin-bottom: 15px;
}

.custom-form-item .el-input,
.custom-form-item .el-switch {
  width: 100%;
}

.custom-button {
  margin-right: 10px;
}

.custom-form {
  padding: 10px 20px;
}
</style>
