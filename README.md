<div align="center">

# OneClick Store Marketing Skill

**一句话输入，自动研究，自动执行，直接交付实体店可用的宣传营销素材包。**

[![AI Agent Ready](https://img.shields.io/badge/AI_Agent-Ready-8A2BE2?style=for-the-badge&logo=probot&logoColor=white)](#)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Local Store Marketing](https://img.shields.io/badge/Local_Store-Marketing_Pack-ff4d6d?style=for-the-badge)](#)

</div>

---

> **OneClick Store Marketing Skill** 是一个面向 AI Agent 的实体店宣传营销 Skill。
>
> 你只需要告诉它：**卖什么 + 店铺类型 + 受众 + 活动目标**。
>
> 它会自动完成：行业研究、营销策略、中文文案、线下物料、社媒宣传、活动方案、商品图 Prompt，并在配置图片 API 后直接生成图片。这个 Skill 不只写几句文案或者生成一张海报，而是把一个线下活动需要的东西一次性补齐：门口怎么吸引人、店员的营销话术是如何、店里怎么成交、社媒怎么种草、社群怎么召回、活动怎么执行、图片怎么生成最吸引消费者。它的目标是用尽可能节省的时间成本和经济成本轻松快速地实现一个完整的线下宣传营销包，让店主能在比如摸鱼的时候生成所需的所有营销和宣传资源。

## 核心能力

- **一句话启动**：例如“谷子店，二次元潮流风，大学生，新品上架”，即可生成完整营销包。
- **默认成品图模式**：直接生成带短中文标题的可用海报 / 社媒图，优先满足普通店主“一次出图”的体验。
- **专业可编辑模式**：同时交付独立中文文案，方便印刷前在设计软件里精修排版。
- **线下可用**：海报、易拉宝、橱窗广告、价签、货架卡、活动页、店员话术。
- **社媒同步**：小红书、微信朋友圈、大众点评、抖音、微信群QQ群公告甚至Instagram、Discord、Telegram 等平台的发布文案与配图素材。
- **活动方案**：集章、抽奖、新人夜、拼团、主题夜、拍照打卡、会员日。
- **直接生图**：内置 OpenAI 兼容 Images API 脚本；没配 API 时也会输出可执行 Prompt。
- **多行业适配**：谷子店、手办店、DND 店、桌游店、宠物店、咖啡店、甜品店、奶茶店、理发店、美甲店、快闪店、VR 店、水果店等，原则上可以覆盖市面上绝大多数店铺行业。

## 产品逻辑

OneClick Store Marketing 默认采用两层交付：

```text
默认模式：OneClick 直接生成带短中文标题的成品图。
专业模式：同时输出可编辑文案，方便印刷前精修。
```

这意味着普通店主可以先拿到“马上能发、马上能看的图”；如果要做正式印刷或门店长期物料，仍然可以用 Skill 输出的文案层进行精修。

## 它和直接让 ChatGPT 生一张海报有什么不同

直接对话生图通常只解决一个问题：**给我一张图**。

这个 Skill 要解决的是实体店老板真正遇到的一整条链路：

- **先判断增长目标**：是增加路过进店、提高新品浏览效率、做活动、拉社群、提高客单价，还是提升复购。
- **再拆素材系统**：不是只有一张海报，而是门口、店内、货架、社媒、社群、活动现场各自有不同任务。
- **统一视觉风格**：所有图片共享 Campaign Style Lock，避免每张图都像不同店做的。
- **处理多 SKU 场景**：谷子店、桌游店、宠物店、咖啡店通常不是卖一个商品，而是需要新品、人气款、店员推荐、组合购、活动款的编排。
- **直接给执行包**：不只给图片，还给文案、价签、社媒标题、社群公告、活动规则、店员话术和文件目录。

所以它的价值不是“比 ChatGPT 多会画一张图”，而是把实体店营销从一句模糊需求，变成一套可执行的本地营销工作流。

## 图片包黄金法则

只要用户说“完整营销包 / 宣传营销包 / 一整套 / 新品上架 / 活动宣传”，默认不是生成 1 张图，而是生成一套资产：

- **1 张门口主海报**：负责吸引路人进店。
- **1 张橱窗广告**：负责 3 秒内看懂新品/活动。
- **1 张易拉宝**：负责店内解释活动和优惠。
- **1 张活动页 / 传单**：负责讲清规则、时间、奖励和加群方式。
- **4 张价签 / 货架卡**：新品、人气、店员推荐、组合购。
- **4 张社媒图**：小红书、朋友圈、Instagram、社群公告。
- **4 张商品 / 场景图**：新品陈列、爆款推荐、组合展示、活动氛围。
- **一套文案与活动方案**：标题、CTA、社媒正文、社群话术、店员话术、活动规则。

单张海报更适合 smoke test；真正展示 Skill 价值时，应跑完整营销包。

## 多商品店铺怎么处理

实体店经常不是一个商品打天下，尤其是谷子店和桌游店。

这个 Skill 的处理方式是先做 **Assortment Intelligence（商品编排判断）**：

- `Hero SKU`：主推新品或最能吸引进店的系列。
- `New Arrivals`：负责制造新鲜感和到店理由。
- `Best Sellers`：负责降低选择成本。
- `Staff Picks`：负责建立店铺人格和推荐感。
- `Entry Items`：负责低价冲动购买。
- `Bundle Items`：负责提高客单价。
- `Community Items`：负责社群、活动和复购。

然后决定是：

- **整合成一张主海报**：适合 1 个主主题 + 少量商品。
- **生成多张宣传图**：适合新品很多、品类复杂、需要分人群推荐。
- **做货架转化系统**：适合店内商品多、顾客选择困难、需要提高浏览和成交效率。

例如桌游店不应该把所有桌游塞进一张图，而应该拆成：新手友好桌游、DND/TRPG 夜、策略桌游、人气聚会游戏、本周新到、店员推荐。

## 输入示例

```text
用 oneclick-store-marketing 给这家店做一套线下宣传营销包：
店铺：谷子店
风格：二次元潮流
受众：大学生
活动：新品上架
目标：提高到店和社群加群
```

## 自动生成内容

### 中文营销文案

例如：

```text
今天的快乐，来自拆谷瞬间。
新品上架，先到先挑。
带同担来店，抽隐藏款周边。
```

### 线下物料

- 门店主海报
- 易拉宝
- 橱窗广告
- 价签 / 货架卡
- 活动页 / 传单
- 店员推荐话术

### 社媒宣传

- 小红书笔记标题与正文
- 微信朋友圈短文案
- Instagram caption
- Discord / 微信社群公告

### 活动方案

- 集章活动
- 抽奖
- 新人夜
- 拼团
- 会员日
- 拍照打卡挑战

### 商品图与视觉 Prompt

- 店铺氛围图
- 商品陈列图
- 活动主视觉
- 社媒方图
- 产品生活方式图

## 快速开始

把这个 Skill 安装到你的 AI Agent Skill 目录，例如 Codex：

```bash
mkdir -p ~/.codex/skills/oneclick-store-marketing
rsync -a --exclude .git --exclude .env --exclude "generated-campaigns/" ./ ~/.codex/skills/oneclick-store-marketing/
```

然后对 Agent 说：

```text
使用 $oneclick-store-marketing 给一家湖滨银泰大学城附近的谷子店做明日方舟周边新品上架营销包，风格二次元潮流，目标是推广活动、提高到店数和加社群。
```

## API 配置

如果只需要策略和 Prompt，不需要配置任何 API。

如果要直接生成图片，在项目根目录创建 `.env`：

```dotenv
IMG_BASE_URL=https://api.openai.com/v1
IMG_MODEL=gpt-image-2
IMG_API_KEY=your-api-key
```

脚本兼容 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_IMAGE_MODEL` 等常见环境变量。

## 命令行用法

只保存并输出 Prompt：

```bash
python scripts/generate_image.py \
  --mode prompt \
  --prompt "trendy anime merch store poster, clean readable Chinese text placeholders..." \
  --job-dir generated-campaigns/guzi-launch-20260515-180000 \
  --asset-type poster \
  --size 1024x1536
```

配置 API 后直接生图：

```bash
python scripts/generate_image.py \
  --mode image \
  --prompt-file prompts/poster-01.txt \
  --job-dir generated-campaigns/guzi-launch-20260515-180000 \
  --asset-type poster \
  --size 1024x1536
```

创建一次交付目录：

```bash
python scripts/create_pack.py \
  --slug guzi-launch \
  --store-type "谷子店" \
  --audience "大学生" \
  --campaign-goal "新品上架"
```

## 交付目录结构

```text
generated-campaigns/<campaign-slug>-<yyyymmdd-hhmmss>/
  campaign-brief.md
  copy-bank.md
  print-assets.md
  social-pack.md
  event-playbook.md
  image-prompts.md
  prompts/
  poster/
  rollup/
  window/
  price-tag/
  event-page/
  social/
  product/
  extras/
```

## 工作流

1. **最小输入解析**：从用户一句话、附件、项目文件和上下文提取店铺、商品、受众、目标。
2. **自动研究**：补足行业语言、目标客群、平台语境、活动玩法和竞品启发。
3. **营销命题**：选择一个主增长目标，如到店、新品、活动、客单价、复购、社群。
4. **风格锁定**：统一色彩、字体、版式、图像风格和物料视觉系统。
5. **文案生成**：先出中文主文案，再按平台和物料改写。
6. **视觉 Prompt**：每张物料独立 Prompt，但共享同一 Campaign Style Lock。
7. **交付打包**：输出店主能直接拿去打印、发社媒、组织活动的文件。


## 局限说明

- 生图质量取决于你配置的图片模型和 API。目前推荐的模型是openai/image-2及在作图上有独特优势的模型。
- 图片模型小概率无法稳定渲染中文，Skill 会同时提供可编辑文字，方便后期排版。
- 涉及授权 IP、医疗功效、真实销量、评价截图、认证标识时，需要用户提供真实素材或公开可查来源。

## License

MIT

<div align="center">
  <p><i>Make local stores easier to notice, enter, remember, and revisit.</i></p>
</div>
