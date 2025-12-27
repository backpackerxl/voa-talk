<template>
  <div class="container">
    <el-row :gutter="24">
      <el-col :span="6">
        <div class="grid-content header">
          <i class="fa-regular fa-comments left-icon"></i>
          <div class="name">
            对话数量
            <el-tooltip effect="light" content="系统使用过程中的所有对话数量" placement="right">
              <el-icon style="margin-left: 4px" :size="12">
                <InfoFilled />
              </el-icon>
            </el-tooltip>
          </div>
          <div class="number">
            {{
              headerObj.talk_count > 1000
                ? `${(headerObj.talk_count / 1000).toFixed(1)} k`
                : headerObj.talk_count
            }}
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content header">
          <i class="fa-solid fa-robot left-icon"></i>
          <div class="name">
            模型数量
            <el-tooltip effect="light" content="系统已接入的大模型的数量" placement="right">
              <el-icon style="margin-left: 4px" :size="12">
                <InfoFilled />
              </el-icon>
            </el-tooltip>
          </div>
          <div class="number">{{ headerObj.model_count }}</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content header">
          <i class="fa-solid fa-user-plus left-icon"></i>
          <div class="name">
            用户数量
            <el-tooltip effect="light" content="系统注册的用户数量" placement="right">
              <el-icon style="margin-left: 4px" :size="12">
                <InfoFilled />
              </el-icon>
            </el-tooltip>
          </div>
          <div class="number">{{ headerObj.user_count }}</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content header">
          <i class="fa-solid fa-envelope left-icon"></i>
          <div class="name">
            邮件数量
            <el-tooltip effect="light" content="系统发送的邮件数量" placement="right">
              <el-icon style="margin-left: 4px" :size="12">
                <InfoFilled />
              </el-icon>
            </el-tooltip>
          </div>
          <div class="number">{{ headerObj.email_count }}</div>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="24">
      <el-col :span="18">
        <div class="grid-content midle">
          <div class="title">
            <span>日对话量</span>
            <div>
              <el-date-picker v-model="barDate" type="datetimerange" :shortcuts="shortcuts" range-separator="To"
                start-placeholder="Start date" end-placeholder="End date" @change="handleBarData" />
            </div>
          </div>
          <ECharts ref="barChart" :option="barChartOption" height="240px" />
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content midle">
          <div class="title">
            <span>模型调用量</span>
            <div>
              <el-date-picker v-model="pieDate" type="datetimerange" :shortcuts="shortcuts" range-separator="To"
                start-placeholder="Start date" end-placeholder="End date" @change="handlePieData" />
            </div>
          </div>
          <ECharts ref="pieChart" :option="pieChartOption" height="240px" />
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="24">
      <el-col :span="6">
        <div class="grid-content bottom">
          <h2 class="title">Tokens 调用量周榜</h2>
          <div class="box" v-for="(item, index) in topTalkList" :key="index">
            <el-tooltip class="box-item" effect="light" :content="item.talk_name" placement="right"
              :disabled="!shouldShowTooltip(index)">
              <template #content>
                {{ item.talk_name }}
              </template>
              <p class="txt" :ref="(el) => handleRef(el, index)">
                <i class="fa-regular fa-comments"></i>{{ item.talk_name }}
              </p>
            </el-tooltip>
            <span>{{
              item.tokens > 1000
                ? `${(item.tokens / 1000).toFixed(1)} k`
                : item.tokens
            }}</span>
          </div>
        </div>
      </el-col>
      <el-col :span="18">
        <div class="grid-content bottom">
          <div class="title">
            <span>Tokens 日调用量</span>
            <div>
              <el-date-picker v-model="lineDate" type="datetimerange" :shortcuts="shortcuts" range-separator="To"
                start-placeholder="Start date" end-placeholder="End date" @change="handleLineData" />
            </div>
          </div>
          <ECharts ref="lineChart" :option="lineChartOption" height="280px" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ECharts from "@/components/ECharts";
import { InfoFilled } from "@element-plus/icons-vue";
import store from "@/store";
import echarts from "@/utils/echarts";
import { formatDateTime, hexToRGB } from "@/utils/tools";
import {
  headerData,
  topTalk,
  modelTalks,
  barTalks,
  lineTokens,
} from "@/api/report";

const barChart = ref(null);
const pieChart = ref(null);
const lineChart = ref(null);
const headerObj = ref({
  user_count: 0,
  model_count: 0,
  talk_count: 0,
  email_count: 0,
});

const topTalkList = ref([]);

const shortcuts = [
  {
    text: "一周以前",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setDate(start.getDate() - 7);
      return [start, end];
    },
  },
  {
    text: "两周以前",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setDate(start.getDate() - 14);
      return [start, end];
    },
  },
  {
    text: "一个月以前",
    value: () => {
      const end = new Date();
      const start = new Date();
      start.setMonth(start.getMonth() - 1);
      return [start, end];
    },
  },
];

const barDate = ref([]);
const lineDate = ref([]);
const pieDate = ref([]);
const contentRefs = ref([]);

// 折线图配置
const lineChartOption = ref({});

// 柱状图配置
const barChartOption = ref({});

// 饼图配置
const pieChartOption = ref({});

function shouldShowTooltip(index) {
  const contentRef = contentRefs.value[index];
  if (contentRef) {
    return contentRef.scrollWidth > contentRef.clientWidth;
  }
  return false;
}

const handleRef = (el, index) => {
  if (el) {
    contentRefs.value[index] = el;
  }
};

function handleBarData() {
  const stm = formatDateTime(barDate.value[0]);
  const etm = formatDateTime(barDate.value[1]);
  barTalks({ stm, etm })
    .then((obj) => {
      const xData = obj.data.map((item) => item.date.split(" ")[0]);
      const yData = obj.data.map((item) => item.talk_count);
      setBarOption(xData, yData);
    })
    .catch((err) => {
      console.log(err);
    });
}

function handlePieData() {
  const stm = formatDateTime(pieDate.value[0]);
  const etm = formatDateTime(pieDate.value[1]);
  modelTalks({ stm, etm })
    .then((obj) => {
      setPieOptione(obj.data);
    })
    .catch((err) => {
      console.log(err);
    });
}

function handleLineData() {
  const stm = formatDateTime(lineDate.value[0]);
  const etm = formatDateTime(lineDate.value[1]);
  lineTokens({ stm, etm })
    .then((obj) => {
      const xData = obj.data.map((item) => item.date.split(" ")[0]);
      const yData = obj.data.map((item) => item.tokens_count);
      setLineOption(xData, yData);
    })
    .catch((err) => {
      console.log(err);
    });
}

function setBarOption(xData, yData) {
  barChartOption.value = {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow",
      },
    },
    legend: {
      data: ["对话量"],
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: xData,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "对话量",
        type: "bar",
        itemStyle: {
          color: echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#83bff6" },
            { offset: 0.5, color: "#188df0" },
            { offset: 1, color: "#188df0" },
          ]),
        },
        data: yData,
      },
    ],
  };
}

function setLineOption(xData, yData) {
  lineChartOption.value = {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
        crossStyle: {
          color: "#999",
        },
      },
    },
    legend: {
      data: ["token调用量"],
    },
    xAxis: {
      type: "category",
      data: xData,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        name: "token调用量",
        type: "line",
        smooth: true,
        areaStyle: {
          color: echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 1,
              color: "rgba(58,77,233,0.8)",
            },
            {
              offset: 0,
              color: "rgba(58,77,233,0.3)",
            },
          ]),
        },
        data: yData,
      },
    ],
  };
}

function setPieOptione(vData) {
  pieChartOption.value = {
    backgroundColor: "transparent",
    tooltip: {
      trigger: "item",
    },
    legend: {
      show: false,
    },
    series: [
      {
        name: "销售渠道",
        type: "pie",
        radius: "50%",
        data: vData,
      },
    ],
  };
}

// 模拟数据加载
onMounted(() => {
  document.documentElement.querySelector("title").innerText = "运行报表";
  store.subscribe((mutation, state) => {
    if (mutation.type === "app/SET_THEM") {
      barChart.value && barChart.value.toggleThem();
      pieChart.value && pieChart.value.toggleThem();
      lineChart.value && lineChart.value.toggleThem();
    }
  });
  // 请求头部数据
  headerData()
    .then((obj) => {
      headerObj.value = obj.data;
    })
    .catch((err) => {
      console.log(err);
    });

  topTalk()
    .then((obj) => {
      topTalkList.value = obj.data;
    })
    .catch((err) => {
      console.log(err);
    });

  // 这里可以是异步数据加载
  const end = new Date(); // 当前时间
  const endAddOne = new Date(); // 当前时间
  const start = new Date();
  start.setMonth(start.getMonth() - 1); // 一个月的数据
  endAddOne.setDate(endAddOne.getDate() + 1);

  barDate.value = [start, end];
  lineDate.value = [start, end];
  pieDate.value = [start, end];

  const stm = formatDateTime(start);
  const etm = formatDateTime(end);

  modelTalks({ stm, etm: formatDateTime(endAddOne) })
    .then((obj) => {
      setPieOptione(obj.data);
    })
    .catch((err) => {
      console.log(err);
    });

  barTalks({ stm, etm })
    .then((obj) => {
      const xData = obj.data.map((item) => item.date.split(" ")[0]);
      const yData = obj.data.map((item) => item.talk_count);
      setBarOption(xData, yData);
    })
    .catch((err) => {
      console.log(err);
    });

  lineTokens({ stm, etm })
    .then((obj) => {
      const xData = obj.data.map((item) => item.date.split(" ")[0]);
      const yData = obj.data.map((item) => item.tokens_count);
      setLineOption(xData, yData);
    })
    .catch((err) => {
      console.log(err);
    });
});
</script>

<style scoped>
.container {
  padding: 16px;
  max-width: 1200px;
  margin: 0 auto;
  overflow: hidden;
}

.el-row {
  margin-bottom: 10px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
  background-color: var(--el-bg-color);
  box-shadow: 0 2px 10px rgb(0, 0, 0, 0.1);
  padding: 10px;
}

.grid-content .title {
  font-size: 16px;
  font-weight: 700;
  color: var(--el-text-color-regular);
  margin: 0;
  padding: 4px;
  display: flex;
  justify-content: space-between;
}

.grid-content :deep(.el-range-editor.el-input__wrapper) {
  padding: 2px !important;
  width: 20px !important;
  height: 20px !important;
  cursor: pointer !important;
}

.grid-content :deep(.el-date-editor .el-range-input),
.grid-content :deep(.el-date-editor .el-range-separator),
.grid-content :deep(.el-date-editor .el-range__close-icon) {
  display: none !important;
}

.header {
  height: 60px;
  position: relative;
}

.header i.left-icon {
  position: absolute;
  font-size: 20px;
  line-height: 60px;
  color: var(--el-color-primary);
  border-right: 1px solid var(--el-text-color-regular);
  padding-right: 5px;
}

.header .number {
  font-size: 24px;
  font-weight: 700;
  color: var(--el-color-primary);
  margin-left: 45px;
}

.header .name {
  font-weight: 600;
  font-size: 16px;
  color: var(--el-text-color-regular);
  margin-left: 45px;
}

.midle {
  height: 280px;
}

.bottom {
  height: 280px;
}

@media (max-width: 1024px) {
  .container {
    padding: 20px;
  }

  .header {
    margin-top: 100px;
    height: 130px;
  }
}

.bottom .box {
  font-size: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--el-color-info-light-5);
  color: var(--me-report-text-color);
  height: 38px;
}

.bottom .box .txt {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bottom .box i.fa-comments {
  margin-right: 10px;
}
</style>