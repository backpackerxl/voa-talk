// src/utils/echarts.js
import * as echarts from 'echarts/core';

// 按需引入图表类型，只需引入需要的图表类型
import {
    LineChart,
    BarChart,
    PieChart,
    RadarChart
} from 'echarts/charts';

// 按需引入组件
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    ToolboxComponent,
    DatasetComponent,
    TransformComponent
} from 'echarts/components';

// 按需引入渲染器
import { CanvasRenderer } from 'echarts/renderers';

// 注册必须的组件
echarts.use([
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    ToolboxComponent,
    DatasetComponent,
    TransformComponent,
    LineChart,
    BarChart,
    PieChart,
    RadarChart,
    CanvasRenderer
]);

export default echarts;
