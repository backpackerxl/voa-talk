<template>
  <div class="them-switch">
    <input
      v-model="themValue"
      @change="handleChange"
      type="checkbox"
      id="sun_switch"
    />
    <label for="sun_switch">
      <div class="switch">
        <el-tooltip
          class="box-item"
          effect="light"
          content="日间模式"
          placement="left"
        >
          <i
            :class="!themValue ? 'fa-solid fa-sun active' : 'fa-solid fa-sun'"
          ></i>
        </el-tooltip>
        <el-tooltip
          class="box-item"
          effect="light"
          content="夜间模式"
          placement="right"
        >
          <i
            :class="themValue ? 'fa-solid fa-moon active' : 'fa-solid fa-moon'"
          ></i>
        </el-tooltip>
      </div>
    </label>
  </div>
</template>

<script setup>
import store from "@/store";
import { ref, onMounted } from "vue";

const themValue = ref(false);

function handleChange() {
  let them = themValue.value ? "dark" : "light";
  if (themValue.value) {
    document.documentElement.classList.remove("light");
  } else {
    document.documentElement.classList.remove("dark");
  }
  document.documentElement.classList.add(them);
  store.dispatch("app/setThem", them);
}

onMounted(function () {
  themValue.value = store.state.app.them === "dark";
});
</script>

<style scoped>
.switch {
  position: relative;
  width: 60px;
  height: 28px;
  border-radius: 4px;
  background: var(--me-switch-bg-color);
  transition: background 0.5s ease-in-out;
  padding: 2px 0;
}

.switch i {
  position: absolute;
  line-height: 28px;
  border-radius: 4px;
  width: 28px;
  text-align: center;
  color: #b0b0b0;
}

.switch i.fa-sun {
  left: 2px;
}

.switch i.fa-sun.active {
  background: #fff;
  color: #ffbd2e;
}

.switch i.fa-moon {
  right: 2px;
}

.switch i.fa-moon.active {
  background: #4b4b4b;
  color: #fff;
}

.them-switch input {
  display: none;
}
</style>