<template>
  <el-dialog
    v-model="state.open"
    title="编辑用户"
    width="520"
    @close="close"
    class="custom-dialog"
  >
    <el-form :model="form" label-width="120px" class="custom-form">
      <el-form-item label="模型ID：" class="custom-form-item">
        <el-input
          v-model="form.model_id"
          disabled
          v-if="form.id !== ''"
        ></el-input>
        <el-input v-model="form.model_id" v-if="form.id === ''"></el-input>
      </el-form-item>
      <el-form-item label="模型名称：" class="custom-form-item">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="接口Api：" class="custom-form-item">
        <el-input v-model="form.req_url"></el-input>
      </el-form-item>
      <el-form-item label="接口Key：" class="custom-form-item">
        <el-input v-model="form.api_key"></el-input>
      </el-form-item>
      <el-form-item label="排序：" class="custom-form-item">
        <el-input v-model="form.sort"></el-input>
      </el-form-item>
      <el-form-item label="模型描述：" class="custom-form-item">
        <el-input type="textarea" v-model="form.desc"></el-input>
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
  model_id: "",
  name: "",
  req_url: "",
  api_key: "",
  desc: "",
  sort: 0,
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
      form.value.model_id = newUser.model_id || "";
      form.value.id = newUser.id || "";
      form.value.name = newUser.name || "";
      form.value.req_url = newUser.req_url || "";
      form.value.api_key = newUser.api_key || "";
      form.value.sort = newUser.sort || 0;
      form.value.desc = newUser.desc || "";
    }
  },
  { immediate: true }
);

const submitEdit = async () => {
  if (form.value.id === "") {
    delete form.value.id;
  }
  emit("submit", form.value);
  form.value = {
    model_id: "",
    name: "",
    req_url: "",
    api_key: "",
    desc: "",
    id: "",
  };
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
