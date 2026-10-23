# Ecom-Style-Unify 🎨

> 上传 2–12 张电商图，AI 自动把一整套图的**场景、字体和设计元素统一成一套风格**。

不需要打开 Photoshop，也不用一张张手动改 —— 把安装包拖进 AI，再发一句话，它就会自动跑完全流程，交付成品图和纯场景图。

**⬇️ 一键下载安装包：[ecommerce-style-unifier.zip](https://github.com/yhhgongzuo/Ecom-Style-Unify/releases/latest/download/ecommerce-style-unifier.zip)**

---

## 🎯 这个 Skill 能帮你解决什么

- 一组电商图风格杂乱（场景不一、字体不一、配色不一），AI 自动统一成同一套视觉语言
- 自动反推每张图的原文案，再按统一的排版规范把文字和设计元素绘入图片
- 全程不调用 Photoshop，最终交付成品 PNG 与纯场景 PNG

**适合谁**：电商卖家、电商设计师、AI 设计爱好者，以及任何需要一次性统一多张电商图风格的人。

**不适合什么**：单张图片设计、把图片拆成可编辑图层（那是另一个 Skill，见下文「相关 Skill」）。

## 🧠 先说清楚：模型是效果的命门

不管在哪个平台跑，生图模型建议全部接 **GPT Image 2.5**。平台和模型没选对，装了也出不来效果，所以先把话说在前面。

| 平台 | 推荐程度 | 生图模型 | 说明 |
|---|---|---|---|
| **GPT Codex** | ✅ **强烈推荐，首选** | 默认 GPT Image 2.5 | 开箱即用，实测效果最到位 |
| 豆包 | ⚠️ 不建议折腾 | 需手动换成 GPT Image 2.5 | 默认模型（seedream）效果非常差；换不了模型就不用浪费时间安装 |
| WorkBuddy | ⚠️ 不建议折腾 | 需在模型设置里切到 GPT Image 2.5 | 同豆包，默认模型效果不达标 |

> 💡 **暂时用不上 Codex 怎么办？** 先把教程和安装包收藏起来，等国内生图模型能力跟上了再装、再用，流程一模一样。Skill 不会过期。

## 📦 安装与使用（Codex 端，2 步装好）

### 第一步：新建对话，拖入安装包

打开 Codex，新建一个对话，把 **[ecommerce-style-unifier.zip](https://github.com/yhhgongzuo/Ecom-Style-Unify/releases/latest/download/ecommerce-style-unifier.zip)** 直接拖进对话框（**不要手动解压**）。

### 第二步：输入「安装」，回车

发送两个字：

```
安装
```

等待安装完成即可。

### 第三步：上传图片，发一句话

上传 2–12 张需要统一风格的电商图，然后发送：

```
自行调用技能，统一图片风格
```

AI 会先让你**确认风格基准**（选择一张图作为整套的风格参考），并提示你**上传产品图**（没有可以跳过），然后全自动跑完全流程，不用你盯着。

## ⚠️ 注意事项 & 常见问题

**这个 Skill 收费吗？**
Skill 本身免费分享，一分不收。生图消耗的是你自己 Codex 账号的生图额度，与作者无关。

**豆包 / WorkBuddy 怎么换成 GPT Image 2.5？**
你需要先有 GPT Image 2.5 的中转站 API 接口，把接口文档信息给到豆包 / WorkBuddy，先跑通生图接口再安装本技能。

**安装时提示报错怎么办？**
绝大多数情况是没装 Python，或 Windows 安装 Python 时没勾选「Add Python to PATH」。装好 Python 后，重新对 Codex 说一次「安装」即可。

**安装包以后会过期吗？**
不会。现在跑不了的平台，先收藏教程和安装包，等模型能力跟上后再装再用。

**怎么输出 PSD 分层文件？**
那是另一个 Skill：[yhhgongzuo/Img-to-PSD](https://github.com/yhhgongzuo/Img-to-PSD)，把海报/电商/宣传图自动逆向重建为分层完整、可自由编辑的 PSD 源文件。

## 📁 仓库结构

```
.
├── SKILL.md                          # Skill 主定义、固定流程与质量底线
├── agents/
│   └── openai.yaml
├── references/
│   └── platform-adaptation.md        # 跨平台与模型适配说明
├── scripts/
│   └── image_workflow.py             # 图片预处理与工作流脚本
└── ecommerce-style-unifier.zip       # 一键安装包（与 Releases 中一致）
```

## 📌 说明

- 本仓库教程与流程均经过实际验证、跑通后整理发布。
- 生成效果属于生成式编辑，受图片复杂度、生图模型与额度影响，不承诺像素级一致；看不清的文字和偏差会被如实记录，不会编造。
- 使用问题与 Bug 欢迎在 [Issues](https://github.com/yhhgongzuo/Ecom-Style-Unify/issues) 反馈。
- 个人精力有限，不做一对一答疑，有问题请先自行研究。

## 💬 联系作者

- 作者：**阿辉本人**
- 微信：**yhhgongzuo**（加好友请备注「GitHub」）
- 业务承接：**GPT 代充、Codex 安装、AI 定制、工作流、软件及网站搭建**
- 后续会持续分享 AI 设计自动化的玩法和工具，觉得有用点个关注不迷路。

## 📜 开源协议

[MIT License](LICENSE)
