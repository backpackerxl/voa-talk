<template>
  <p class="txt">登录成功！正在为您跳转...</p>
</template>

<script setup>
import { qqUserLogin } from "@/api/login";
import { ElMessage } from "element-plus";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import store from "@/store"; // 导入Vuex store
const router = useRouter();

onMounted(function () {
  const url = new URL(window.location.href);
  const params = new URLSearchParams(url.search);

  const code = params.get("code");
  const state = params.get("state");

  if (state === "qqLogin") {
    qqUserLogin({
      code,
      redirect_uri: encodeURIComponent("https://voatalk.online/others/handle"),
    })
      .then((obj) => {
        ElMessage.success("登录成功");

        store.dispatch("app/setAuthorization", obj.data.jwtToken);
        store.dispatch("app/setUserRole", obj.data.superAdmin);
        store.dispatch("app/setNickName", obj.data.nickName);
        store.dispatch("app/setUserName", obj.data.userName);
        store.dispatch("app/setUserEmail", obj.data.email);
        store.dispatch("app/setAvatar", obj.data.avatar);

        router.replace("/home/chat");
      })
      .catch((err) => {
        console.log(err);
        router.replace("/login");
      });
  }
});
</script>

<style scoped>
.txt {
  text-align: center;
}
</style>
