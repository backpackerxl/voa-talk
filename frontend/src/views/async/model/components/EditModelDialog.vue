<template>
  <el-dialog
    v-model="state.open"
    :title="title"
    width="480"
    @close="close"
    class="custom-dialog"
  >
    <el-form
      :model="form"
      :rules="rules"
      ref="registerFormRef"
      label-width="100px"
      class="custom-form"
    >
      <el-form-item prop="model_id" label="模型ID：" class="custom-form-item">
        <el-input
          v-model="form.model_id"
          disabled
          v-if="form.id !== ''"
        ></el-input>
        <el-input v-model="form.model_id" v-if="form.id === ''"></el-input>
      </el-form-item>
      <el-form-item prop="name" label="模型名称：" class="custom-form-item">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item prop="req_url" label="接口Api：" class="custom-form-item">
        <el-input v-model="form.req_url"></el-input>
      </el-form-item>
      <el-form-item prop="api_key" label="接口Key：" class="custom-form-item">
        <el-input v-model="form.api_key"></el-input>
      </el-form-item>
      <el-form-item prop="sort" label="排序：" class="custom-form-item">
        <el-input v-model="form.sort"></el-input>
      </el-form-item>
      <el-form-item prop="desc" label="模型描述：" class="custom-form-item">
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
import { ElMessage } from "element-plus";

let emit = defineEmits(["close", "submit"]);
const props = defineProps({
  model: Object,
  title: String,
});

function close() {
  emit("close");
}

const form = ref({
  model_id: null,
  name: null,
  req_url: null,
  api_key: null,
  desc: null,
  sort: 0,
  id: "",
});
let state = reactive({
  open: true,
});

const rules = {
  model_id: [{ required: true, message: "模型ID", trigger: "blur" }],
  name: [{ required: true, message: "请输入模型名称", trigger: "blur" }],
  req_url: [
    { required: true, message: "请输入模型ApiUrl", trigger: "blur" },
    {
      validator: (rule, value, callback) => {
        const pattern =
          /^(https?:\/\/)(([\w-]+(\.[\w-]+)+)|localhost|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))([\/\w\-.,@?^=%&:~+#]*[\w\-@?^=%&\/~+#])?$/;
        if (!pattern.test(value)) {
          callback(new Error("模型ApiUrl格式不正确"));
        } else {
          callback();
        }
      },
      trigger: ["blur", "change"],
    },
  ],
  api_key: [{ required: true, message: "请输入模型ApiKey", trigger: "blur" }],
};

const registerFormRef = ref(null);

watch(
  () => props.model,
  (newModel) => {
    // console.log("New user data received in dialog:", newUser); // 检查数据接收
    if (newModel) {
      form.value.model_id = newModel.model_id || "";
      form.value.id = newModel.id || "";
      form.value.name = newModel.name || "";
      form.value.req_url = newModel.req_url || "";
      form.value.api_key = newModel.api_key || "";
      form.value.sort = newModel.sort || 0;
      form.value.desc = newModel.desc || "";
    }
  },
  { immediate: true }
);

const submitEdit = () => {
  registerFormRef.value.validate(function (valid) {
    if (valid) {
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
    } else {
      ElMessage.warning("请填写完整的模型配置。");
    }
  });
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
