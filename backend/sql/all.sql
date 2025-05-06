/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80039 (8.0.39)
 Source Host           : localhost:3308
 Source Schema         : ai_chat

 Target Server Type    : MySQL
 Target Server Version : 80039 (8.0.39)
 File Encoding         : 65001

 Date: 15/04/2025 08:08:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for model_config
-- ----------------------------
DROP TABLE IF EXISTS `model_config`;
CREATE TABLE `model_config`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '模型名称',
  `desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模型描述',
  `req_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '接口请求地址',
  `api_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'API接口Key',
  `model_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '模型id',
  `create_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `update_date` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `sort` int NOT NULL COMMENT '排序',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of model_config
-- ----------------------------
INSERT INTO `model_config` VALUES (2, 'Doubao1.5-pro', 'Doubao-1.5-pro 全新一代主力模型，性能全面升级，在知识、代码、推理、等方面表现卓越。支持 32k 上下文窗口，输出长度支持最大 12k tokens。', 'https://ark.cn-beijing.volces.com/api/v3', 'a3795bbd-4c73-4f54-997a-bc758af5c1fe', 'doubao-1-5-pro-32k-250115', '2025-04-06 23:58:10', '2025-04-12 13:04:32', 3);
INSERT INTO `model_config` VALUES (7, 'DeepSeek-R1', 'Deepseek大模型', 'https://ark.cn-beijing.volces.com/api/v3', 'a40dab55-4b35-4b37-aebd-300d07cd5c70', 'deepseek-r1-250120', '2025-04-11 21:15:46', '2025-04-11 21:17:05', 2);

-- ----------------------------
-- Table structure for request_logs
-- ----------------------------
DROP TABLE IF EXISTS `request_logs`;
CREATE TABLE `request_logs`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int NOT NULL COMMENT '用户id',
  `mode_id` int NOT NULL COMMENT '模型id',
  `create_date` timestamp NULL DEFAULT NULL COMMENT '记录时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of request_logs
-- ----------------------------

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户名',
  `pass_word` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码',
  `salt` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码盐',
  `nick_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '姓名',
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '头像',
  `last_login_time` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `super_admin` tinyint(1) NULL DEFAULT 0 COMMENT '是否超级管理员(0否，1是)',
  `create_user` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `create_date` datetime NULL DEFAULT NULL COMMENT '创建日期',
  `update_user` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '修改用户',
  `update_date` datetime NULL DEFAULT NULL COMMENT '修改日期',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `user_state` tinyint(1) NOT NULL COMMENT '账户状态(0：停用，1：正常)',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '系统用户信息表' ROW_FORMAT = COMPACT;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 'admin', 'f23243dd0198a120b4e056d0e0ac319643d8231a5d9b30ae6e08fd41f9d6ddb7', 'jBz4LhRgOkdWgzdSsi5H', '超级管理员', 'api/uploads/699770669730238464.png', '2025-04-15 08:05:45', NULL, 1, NULL, NULL, NULL, NULL, '2981040485@qq.com', 1);
INSERT INTO `sys_user` VALUES (50, 'xiaoyuantongxue', 'cced56eb877a813cd581e5da119f9fd523ec25994d3abfc00b0b6fda59295d6c', '5376wBfWGHJWp7uJMQUX', '小袁同学', NULL, '2024-08-19 21:08:49', NULL, 0, NULL, '2024-08-19 20:52:35', NULL, '2024-08-19 20:52:35', 'Liu_zongxin@yeah.net', 1);
INSERT INTO `sys_user` VALUES (51, 'bxl', '1db112744396f563f3be90dfcc39254747e7f672c456e98103bda50e404405fc', 'rv10FKQmvTWWerXeUUuz', '小小怪', 'api/uploads/699771860996460544.png', '2025-04-15 08:04:16', NULL, 0, NULL, '2025-04-04 23:18:24', NULL, '2025-04-05 11:03:39', '946115360@qq.com', 1);

-- ----------------------------
-- Table structure for talk_logs
-- ----------------------------
DROP TABLE IF EXISTS `talk_logs`;
CREATE TABLE `talk_logs`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `talk_id` bigint NOT NULL COMMENT '对话id',
  `resp_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '模型响应内容',
  `req_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '用户输入的内容',
  `img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '图片地址',
  `create_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 50 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of talk_logs
-- ----------------------------
INSERT INTO `talk_logs` VALUES (11, 699308439213576200, '你好呀！有什么问题或者想聊的事情都可以跟我说一说。 ', '你好', NULL, '2025-04-14 01:22:08');
INSERT INTO `talk_logs` VALUES (12, 699309191344558100, '你好呀！有什么想聊的，都可以跟我说一说。 ', '你好呀\n', NULL, '2025-04-14 01:25:06');
INSERT INTO `talk_logs` VALUES (13, 699309191344558100, '我叫豆包，你可以随时和我畅快聊天！ ', '你叫什么\n', NULL, '2025-04-14 01:26:28');
INSERT INTO `talk_logs` VALUES (14, 699309191344558100, '我会的事情可多啦，下面为你列举一些常见的应用场景：\n\n### 知识查询\n- 能为你解释各类学科知识，比如历史事件的背景、经过和影响，像赤壁之战的战略意义；科学领域的原理，例如牛顿三大定律的内容。\n- 提供各种专业信息，涵盖医学、法律、金融等方面，比如解释不同类型的法律合同条款，分析常见疾病的症状和治疗方法。\n\n### 文本创作\n- 撰写多种类型的文章，如故事、诗歌、散文、议论文等。例如，我可以创作一个富有想象力的童话故事，或者一篇观点鲜明的议论文。\n- 生成文案，包括广告宣传语、产品介绍、活动策划文案等。比如为一款新的护肤品创作吸引人的宣传文案。\n\n### 语言学习\n- 进行语言翻译，支持多种常见语言之间的互译，帮助你理解外文资料或准确表达自己的想法。\n- 提供语法讲解、词汇辨析、发音指导等语言学习方面的帮助，助力你提升语言能力。\n\n### 日常问答\n- 解答生活中的各种疑问，如旅游攻略，包括热门旅游地的景点推荐、美食介绍、住宿建议等；还能回答关于家居生活、健康养生等方面的问题。\n- 处理情感咨询，当你遇到情感困扰时，我可以倾听并给出一些分析和建议。\n\n### 逻辑推理\n- 帮你分析问题、理清思路，解决一些逻辑谜题、数学问题等。比如推理复杂的案件情节，或者解答奥数题目。 ', '你会什么\n', NULL, '2025-04-14 01:26:48');
INSERT INTO `talk_logs` VALUES (15, 699318795579297800, '你好呀！有什么问题或者想聊的事情都可以跟我说哦。 ', '你好\n', NULL, '2025-04-14 02:03:16');
INSERT INTO `talk_logs` VALUES (16, 699318795579297800, '冒泡排序（Bubble Sort）是一种简单的排序算法。它重复地走访过要排序的数列，一次比较两个元素，如果它们的顺序错误就把它们交换过来。走访数列的工作是重复地进行直到没有再需要交换，也就是说该数列已经排序完成。\n\n以下是使用不同编程语言实现冒泡排序的代码：\n\n### Python 实现\n```python\ndef bubble_sort(arr):\n    n = len(arr)\n    # 遍历所有数组元素\n    for i in range(n):\n        # 最后 i 个元素已经排好序，不需要再比较\n        for j in range(0, n - i - 1):\n            # 如果当前元素大于下一个元素，则交换它们\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n\n# 测试代码\narr = [64, 34, 25, 12, 22, 11, 90]\nsorted_arr = bubble_sort(arr)\nprint(\"排序后的数组:\", sorted_arr)\n```\n\n### Java 实现\n```java\npublic class BubbleSort {\n    public static void bubbleSort(int[] arr) {\n        int n = arr.length;\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < n - i - 1; j++) {\n                if (arr[j] > arr[j + 1]) {\n                    // 交换 arr[j+1] 和 arr[j]\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                }\n            }\n        }\n    }\n\n    public static void main(String[] args) {\n        int[] arr = {64, 34, 25, 12, 22, 11, 90};\n        bubbleSort(arr);\n        System.out.print(\"排序后的数组: \");\n        for (int num : arr) {\n            System.out.print(num + \" \");\n        }\n    }\n}\n```\n\n### C++ 实现\n```cpp\n#include <iostream>\nusing namespace std;\n\nvoid bubbleSort(int arr[], int n) {\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                // 交换 arr[j+1] 和 arr[j]\n                int temp = arr[j];\n                arr[j] = arr[j + 1];\n                arr[j + 1] = temp;\n            }\n        }\n    }\n}\n\nint main() {\n    int arr[] = {64, 34, 25, 12, 22, 11, 90};\n    int n = sizeof(arr) / sizeof(arr[0]);\n    bubbleSort(arr, n);\n    cout << \"排序后的数组: \";\n    for (int i = 0; i < n; i++) {\n        cout << arr[i] << \" \";\n    }\n    return 0;\n}\n```\n\n### 复杂度分析\n- **时间复杂度**：$O(n^2)$，其中 $n$ 是数组的长度。因为需要进行两层嵌套循环。\n- **空间复杂度**：$O(1)$，只需要常数级的额外空间。', '写一个冒泡排序\n', NULL, '2025-04-14 02:03:50');
INSERT INTO `talk_logs` VALUES (17, 699595970064814100, '我叫豆包，很高兴能和你交流！如果你有任何问题，都可以随时跟我说。 ', '你好，你叫什么名字\n', NULL, '2025-04-14 20:24:41');
INSERT INTO `talk_logs` VALUES (18, 699595970064814100, '“豆包”这个名字是字节跳动研发团队为我取的。它简单易记、亲切可爱，能方便大家认识和记住我，也让你和我交流时能更自然亲近，你要是喜欢，也可以给我起其他昵称来称呼我呀。 ', '你为啥叫豆包\n', NULL, '2025-04-14 20:26:34');
INSERT INTO `talk_logs` VALUES (19, 699595970064814100, '# 星星邮递员\n在遥远的宇宙深处，有一个名叫“梦幻星”的星球。这里住着一群可爱的小精灵，他们有着透明的翅膀和闪烁着柔和光芒的眼睛。其中有一个叫悠悠的小精灵，他是星星邮递员，负责将来自各个星球的信件送到梦幻星居民的手中。\n\n每天清晨，悠悠都会早早地起床，穿上他那件带有星星图案的邮递员制服，来到星星邮局。邮局里堆满了各种形状和颜色的信件，有像流星一样拖着长长尾巴的信，也有像云朵一样软绵绵的信。悠悠熟练地将信件分类，然后装进他那神奇的邮袋里。这个邮袋看起来小小的，但却能装下无数的信件，无论多少都不会满。\n\n悠悠骑着他的流星滑板出发了。他在宇宙中穿梭，星星在他身边闪烁，像是为他照亮前行的道路。他先来到了月亮精灵的家，月亮精灵住在一个弯弯的月亮船上，周围环绕着银色的雾气。悠悠从邮袋里拿出一封散发着月光的信，交给了月亮精灵。月亮精灵开心地笑了，她的笑声像铃铛一样清脆，还送了悠悠一颗小小的月亮石作为礼物。\n\n接着，悠悠又来到了彩虹仙子的花园。花园里盛开着各种颜色的花朵，花瓣上闪烁着五彩的光芒。彩虹仙子正忙着给花朵浇水，悠悠把一封带着花香的信递给了她。彩虹仙子非常高兴，她用魔法变出了一道小小的彩虹，让悠悠从上面滑了过去，那种感觉就像在柔软的云朵上飞翔。\n\n可是，有一天，当悠悠像往常一样来到星星邮局时，发现所有的信件都不见了。邮局里空空荡荡的，只有地上有一串奇怪的脚印。悠悠顺着脚印追去，发现脚印一直延伸到了宇宙黑洞的边缘。\n\n原来，是一个调皮的小怪兽偷走了信件。小怪兽觉得那些信件很有趣，想要自己留着玩。悠悠走到小怪兽面前，温柔地说：“小怪兽，这些信件是大家的宝贝，里面装着朋友们的思念和祝福。如果你把它们还给我，我可以带你一起去送信件，让你也感受一下传递快乐的感觉。”\n\n小怪兽听了悠悠的话，有点不好意思地低下了头。他把信件都还给了悠悠，还跟着悠悠一起去送信件。在送信件的过程中，小怪兽看到大家收到信时开心的样子，也感受到了帮助别人的快乐。\n\n从那以后，小怪兽成为了悠悠的小助手，他们一起在宇宙中穿梭，把温暖和快乐传递给每一个星球的居民。而悠悠，依然是那个最快乐的星星邮递员，带着他的梦想和使命，在浩瀚的宇宙中继续着他的奇妙之旅。 ', '讲一个小故事吧\n', NULL, '2025-04-14 20:31:13');
INSERT INTO `talk_logs` VALUES (20, 699595970064814100, '以下为你提供不同场景下的工作安排计划示例，你可以根据实际情况进行修改和调整。\n\n### 个人一周工作安排计划\n#### 计划背景\n为了合理规划本周工作时间，提高工作效率，确保各项任务有条不紊地完成，特制定本一周工作安排计划。\n\n#### 本周工作目标\n1. 完成项目 A 的初步方案设计。\n2. 跟进客户 B 的合作意向，争取达成合作。\n3. 参加业务培训，提升专业技能。\n4. 处理日常文件和邮件，确保工作沟通顺畅。\n\n#### 具体工作安排\n\n| 日期 | 上午 | 下午 | 晚上 |\n| --- | --- | --- | --- |\n| 周一 | 1. 召开项目 A 小组会议，明确设计方向和分工<br>2. 收集项目 A 相关资料 | 1. 开始撰写项目 A 初步方案<br>2. 回复重要邮件和处理文件 | 复习业务培训相关资料 |\n| 周二 | 1. 继续完善项目 A 初步方案<br>2. 与团队成员讨论方案细节 | 1. 联系客户 B，介绍合作优势和方案<br>2. 记录客户反馈和意见 | 无 |\n| 周三 | 1. 参加业务培训课程<br>2. 做好培训笔记 | 1. 整理培训内容，总结要点<br>2. 根据培训所学优化项目 A 方案 | 无 |\n| 周四 | 1. 完成项目 A 初步方案设计<br>2. 提交方案给上级审核 | 1. 跟进上级对方案的审核意见，进行修改完善<br>2. 再次与客户 B 沟通，解决疑问 | 无 |\n| 周五 | 1. 确认项目 A 方案最终版本，准备下周的项目启动会议<br>2. 整理本周工作文件和资料 | 1. 总结本周与客户 B 的沟通情况，制定下周跟进计划<br>2. 参加部门周会，汇报工作进展 | 无 |\n\n#### 风险评估与应对\n1. **风险**：项目 A 方案审核未通过，需要重新修改。\n    - **应对**：及时与上级沟通，明确修改方向，加班加点完成修改任务，确保不影响项目进度。\n2. **风险**：客户 B 对合作方案不满意，合作意向降低。\n    - **应对**：深入了解客户需求和意见，调整合作方案，增加合作的吸引力和竞争力。\n\n#### 总结与反馈\n每周五下班前，对本周工作进行全面总结，分析工作中的优点和不足，提出改进措施和建议。同时，将本周工作情况反馈给上级领导，听取领导的意见和指导。\n\n### 团队月度工作安排计划\n#### 计划背景\n为了确保团队在本月内高效协作，达成既定业务目标，提升团队整体业绩，特制定本团队月度工作安排计划。\n\n#### 本月工作目标\n1. 完成产品 X 的市场推广活动，提高产品知名度和市场占有率。\n2. 新客户开发数量达到[X]个，确保销售额增长[X]%。\n3. 优化团队内部工作流程，提高工作效率和协作质量。\n\n#### 具体工作安排\n\n| 阶段 | 时间范围 | 工作内容 | 负责人 |\n| --- | --- | --- | --- |\n| 第一阶段：准备与策划 | 1 - 5 日 | 1. 制定产品 X 市场推广方案，包括线上线下推广渠道、活动形式和预算<br>2. 组建新客户开发小组，明确成员职责和分工<br>3. 收集团队成员对现有工作流程的意见和建议 | 市场经理<br>销售经理<br>运营主管 |\n| 第二阶段：执行与推进 | 6 - 20 日 | 1. 按照推广方案开展产品 X 市场推广活动，如社交媒体宣传、线下展会等<br>2. 新客户开发小组积极拓展潜在客户，进行电话沟通、上门拜访等销售活动<br>3. 运营主管根据收集的意见，优化团队内部工作流程，制定新的工作规范 | 市场专员<br>销售代表<br>运营专员 |\n| 第三阶段：监控与调整 | 21 - 25 日 | 1. 定期监控产品 X 市场推广活动的效果，分析数据，根据反馈调整推广策略<br>2. 销售经理统计新客户开发数量和销售额，评估销售业绩，对未完成任务的成员进行指导和培训<br>3. 组织团队成员对新工作流程进行试用，收集反馈意见，进行微调 | 市场经理<br>销售经理<br>运营主管 |\n| 第四阶段：总结与评估 | 26 - 30 日 | 1. 对产品 X 市场推广活动进行全面总结，评估活动效果和投入产出比<br>2. 统计本月新客户开发数量和销售额，与目标进行对比，分析差距和原因<br>3. 召开团队月度总结会议，对本月工作进行表彰和奖励，同时提出改进措施和下月工作目标 | 市场经理<br>销售经理<br>团队负责人 |\n\n#### 资源需求\n1. **人力资源**：确保市场、销售和运营团队人员充足，必要时可招聘临时人员协助工作。\n2. **资金资源**：为市场推广活动提供充足的资金支持，包括广告投放、展会费用等。\n3. **物资资源**：准备好产品宣传资料、礼品等物资，用于市场推广和客户开发。\n\n#### 沟通机制\n1. 每日召开小组晨会，汇报工作进展和问题，及时协调解决。\n2. 每周召开团队周会，总结本周工作，部署下周任务。\n3. 建立工作沟通群，及时发布工作信息和重要通知。\n\n#### 风险管理\n1. 密切关注市场动态和竞争对手的活动，及时调整推广策略。\n2. 加强对销售团队的培训和管理，提高销售技巧和客户服务水平，降低客户流失率。\n3. 对工作流程优化过程中可能出现的问题进行提前预判，制定应急预案。 ', '写一个工作安排计划\n', NULL, '2025-04-14 20:32:12');
INSERT INTO `talk_logs` VALUES (21, 699308439213576200, '感觉你心情很不错呀，这么欢快的笑声都溢出屏幕啦！能和我分享下让你开心的事儿不？ ', '哈哈\n', NULL, '2025-04-14 20:39:00');
INSERT INTO `talk_logs` VALUES (22, 699308439213576200, '没发工资确实会让人心里有些焦虑和不安。你能和我说说具体情况吗，是公司整体都没发，还是只有你没收到工资呢？\n\n如果是公司统一延迟发放，可能是遇到了资金周转之类的问题，你可以向同事了解下情况，也可以找HR询问工资发放延迟的原因和预计发放时间。要是只有你没收到，要看看是不是银行卡信息有误、工资发放流程出现了问题等。你也可以和我说说这是多久没发工资了呀。 ', '没发工资\n', NULL, '2025-04-14 20:39:47');
INSERT INTO `talk_logs` VALUES (23, 699308439213576200, '有点不太明确你说“是不是很惨”具体所指的是什么呀。可以跟我详细说说，比如是某件事情、某个人的遭遇，这样我就能更好地和你探讨惨不惨啦。 ', '是不是很惨\n', NULL, '2025-04-14 20:40:24');
INSERT INTO `talk_logs` VALUES (24, 699308439213576200, '没发工资确实会让人着急又心烦呢。是到了该发工资的时间还没发吗？你可以先和同事们确认下，是不是大家都没发。要是只有你没收到，就找公司财务或者上级问清楚具体情况。跟我说说，这是什么情况导致工资没发呀？ ', '没发工资啊\n', NULL, '2025-04-14 20:40:38');
INSERT INTO `talk_logs` VALUES (28, 699632203063234600, '感觉你心情很不错呀，这么欢快的招呼~能和我分享一下让你开心的事儿吗？ ', '嘿嘿\n', NULL, '2025-04-14 22:48:38');
INSERT INTO `talk_logs` VALUES (41, 699683526630576100, '小蚂蚁迷路找不到蚁窝，可着急了，恰好看到它的朋友经过，于是冲过去大喊一声：“哥们儿！你…你都如何回蚁窝（回忆我）？”那朋友一愣，然后反问道：“带……带……带着笑或是很沉默？” ', '讲一个笑话\n', NULL, '2025-04-15 02:12:35');
INSERT INTO `talk_logs` VALUES (42, 699710794669101000, '你好呀！有什么问题或者想聊的事都能跟我说。 ', '你好\n', NULL, '2025-04-15 04:00:57');
INSERT INTO `talk_logs` VALUES (43, 699710794669101000, '当然可以啦，我给你讲一个《农夫与蛇》的故事。\n\n在一个寒冷的冬天，农夫干完农活后正匆匆忙忙地回家。当他经过一条小道时，发现路边有一条冻僵了的蛇。农夫是个心地善良的人，他看着这条蛇，心生怜悯，想着这么冷的天，这蛇要是不救，肯定就死了。\n\n于是，农夫弯腰把蛇捡了起来，小心翼翼地揣进了自己怀里，想用自己身体的温暖来救活它。过了一会儿，蛇在农夫温暖的怀抱中渐渐苏醒过来。当它恢复了一点力气，突然露出了凶狠的本性，在农夫的胸口狠狠地咬了一口。\n\n农夫只觉得胸口一阵剧痛，他没想到自己好心救了蛇，蛇却恩将仇报。农夫又惊又怒，他挣扎着把蛇从怀里拿出来，用最后的力气将蛇摔在了地上。可蛇的这一口咬得太重了，农夫中了蛇毒，身体越来越虚弱，慢慢地倒在了地上，不久就死去了。\n\n这个故事告诉我们，在帮助别人的时候，一定要先认清对方的本质，不能对坏人或者不知感恩的人施以善心，不然最后可能会给自己带来伤害。你喜欢这个故事吗？我还有很多其他类型的故事可以讲给你听。 ', '我能听你讲故事吗\n', NULL, '2025-04-15 04:04:34');
INSERT INTO `talk_logs` VALUES (46, 699713751208824800, '感觉你心情很不错呀，这么欢快的语气都溢出屏幕啦！能和我说说是什么事儿让你这么开心吗？ ', '嘻嘻，嘿嘿\n', NULL, '2025-04-15 04:12:40');
INSERT INTO `talk_logs` VALUES (47, 699713751208824800, '看起来你不太想说话呢，要是之后有想聊的，随时都能跟我说。 ', '不说\n', NULL, '2025-04-15 04:12:47');
INSERT INTO `talk_logs` VALUES (48, 699713751208824800, '感觉你在调皮地卖关子呢😆 能稍微透露一点点不，我真的有点好奇呀。 ', '就是不告诉你\n', NULL, '2025-04-15 04:13:09');
INSERT INTO `talk_logs` VALUES (49, 699713751208824800, '感觉你心情很不错呀，这么欢快的笑声都溢出屏幕啦！能和我说说什么事情让你这么开心吗？ ', '哈哈\n', NULL, '2025-04-15 04:13:17');

-- ----------------------------
-- Table structure for talk_user_relation
-- ----------------------------
DROP TABLE IF EXISTS `talk_user_relation`;
CREATE TABLE `talk_user_relation`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int NOT NULL COMMENT '用户id',
  `talk_id` bigint NOT NULL COMMENT '对话id',
  `talk_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对话名称',
  `create_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `nick_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户昵称',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of talk_user_relation
-- ----------------------------
INSERT INTO `talk_user_relation` VALUES (2, 1, 699308439213576200, '日常问候', '2025-04-14 01:22:07', '超级管理员');
INSERT INTO `talk_user_relation` VALUES (3, 1, 699309191344558100, '简单问候语开启交流', '2025-04-14 01:25:06', '超级管理员');
INSERT INTO `talk_user_relation` VALUES (4, 1, 699318795579297800, '简单问候语', '2025-04-14 02:03:15', '超级管理员');
INSERT INTO `talk_user_relation` VALUES (5, 1, 699595970064814100, '询问对方名字', '2025-04-14 20:24:41', '超级管理员');
INSERT INTO `talk_user_relation` VALUES (9, 1, 699632203063234600, '轻松的问候吧', '2025-04-14 22:48:38', '超级管理员');
INSERT INTO `talk_user_relation` VALUES (20, 1, 699683526630576100, '讲一个笑话吧', '2025-04-15 02:12:35', '超级管理员');
INSERT INTO `talk_user_relation` VALUES (21, 51, 699710794669101000, '简单问候语开启交流', '2025-04-15 04:00:57', '大大怪');
INSERT INTO `talk_user_relation` VALUES (24, 51, 699713751208824800, '欢快的嘻嘻嘿嘿之音', '2025-04-15 04:12:40', '大大怪');

SET FOREIGN_KEY_CHECKS = 1;
