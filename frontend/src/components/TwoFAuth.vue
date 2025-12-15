<template>
  <div class="container">

  </div>
</template>

<script setup>
import { registerBegin, registerComplete, generateOtpQrcode, loginBegin, loginComplete, verifyOtp } from "@/api/twoFAuth";
import { nextTick, ref } from "vue";
import { RefreshRight, DArrowRight } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

</script>

<style scoped></style>