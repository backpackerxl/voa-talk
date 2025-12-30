<template></template>

<script setup>
import { otherLogin } from "@/api/login";
import { ElMessage } from "element-plus";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import store from "@/store"; // 导入Vuex store
const router = useRouter();

onMounted(function () {
  const url = new URL(window.location.href);
  const params = new URLSearchParams(url.search);
  const bindOtherAccount = store.state.app.bindOtherAccount || '';

  const code = params.get("code");
  const state = params.get("state");

  otherLogin({
    code,
    login_type: state,
    redirect_uri: encodeURIComponent("https://www.voatalk.online/others/handle"),
    bind_other_account: bindOtherAccount,
  })
    .then((obj) => {
      if (!bindOtherAccount) {
        ElMessage.success("🎉登录成功，跳转中...");

        store.dispatch("app/setAuthorization", obj.data.jwtToken);
        store.dispatch("app/setUserRole", obj.data.superAdmin);
        store.dispatch("app/setNickName", obj.data.nickName);
        store.dispatch("app/setUserName", obj.data.userName);
        store.dispatch("app/setUserEmail", obj.data.email);
        store.dispatch("app/setAvatar", obj.data.avatar);
        store.dispatch("app/setLoginType", obj.data.loginType || '');

        router.replace("/home/chat");
      } else {
        ElMessage.success("🎉第三方已响应，请关闭弹窗，继续后面的操作！");
      }
    })
    .catch((err) => {
      console.log(err);
      router.replace("/login");
    });
});
</script>

<style scoped></style>
