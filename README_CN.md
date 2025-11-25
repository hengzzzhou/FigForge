# AI 科研绘图工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

🎨 **使用AI模型生成高质量的科研论文配图**

本工具采用先进的两步工作流程，从科研文本生成 NeurIPS/ICLR 风格的专业科研配图：
1. **GPT-5** 分析你的科研文本并生成结构化的模块列表（MODULE LIST）
2. **Gemini-2.5-flash-image**（nano banana）根据模块列表创建专业配图

## ✨ 功能特点

- 🤖 **集成AI工作流**：GPT-5 分析指导 nano banana 生成最优结果
- 📊 **发表级质量**：生成简洁的 NeurIPS 风格科研配图
- 🎯 **结构化方法**：两步流程确保可视化的逻辑性和准确性
- 🔧 **简单配置**：通过 `.env` 文件轻松设置
- 💾 **自动保存**：同时保存模块列表和生成的图片
- 🖥️ **命令行界面**：友好的命令行工具

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone git@github.com:hengzzzhou/FigForge.git
cd FigForge

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

从模板创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 并添加你的 API 凭证：

**方式 1：OpenAI 兼容中转网站 API**（默认，适用于中转端点）
```env
API_TYPE=openai
OPENAI_BASE_URL=
OPENAI_API_KEY=
ANALYSIS_MODEL=gpt-5
IMAGE_MODEL=gemini-2.5-flash-image
OUTPUT_DIR=outputs
```

**方式 2：原生 Google Gemini API**
```env
API_TYPE=gemini
GEMINI_API_KEY=
OPENAI_BASE_URL=
OPENAI_API_KEY=
ANALYSIS_MODEL=gpt-5
IMAGE_MODEL=gemini-2.5-flash-image
OUTPUT_DIR=outputs
```

> **注意**：当使用 `API_TYPE=gemini` 时，模块列表生成仍使用 OpenAI 兼容 API，但图像生成使用原生 Google Gemini API。

### 3. 使用方法

**从文件生成：**
```bash
python scientific_plotter.py -i examples/sample_input.txt
```

**直接从文本生成：**
```bash
python scientific_plotter.py -t "描述你的模型架构的科研文本..."
```

**指定输出位置：**
```bash
python scientific_plotter.py -i input.txt -o my_awesome_figure.png
```

**只生成模块列表：**
```bash
python scientific_plotter.py -i input.txt --module-list-only
```

## 📖 工作原理

### 第一步：生成模块列表（GPT-5）

GPT-5 模型分析你的科研文本，创建结构化的模块列表（MODULE LIST），将架构分解为：

1. **Input(s)**：数据源和预处理
2. **Preprocessing/Encoding/Embedding**：特征提取层
3. **Core Architecture/Stages/Blocks**：主要模型组件序列
4. **Special Mechanisms**：注意力、记忆、路由等机制
5. **Output Head**：最终预测层

### 第二步：生成配图（Gemini-2.5-flash-image）

使用模块列表作为指导，nano banana 生成简洁专业的配图，遵循以下设计原则：

- ✅ 扁平、简洁的 NeurIPS 风格（无渐变、无阴影）
- ✅ 一致的细线条
- ✅ 专业的柔和色调
- ✅ 圆角矩形表示模块块
- ✅ 清晰的箭头指示数据流
- ✅ 简洁的标签（无长句子）
- ✅ 纯白背景，整洁的间距

## 📁 项目结构

```
NBP/
├── scientific_plotter.py      # 主程序脚本
├── requirements.txt            # Python 依赖
├── .env.example               # 环境变量模板
├── .gitignore                 # Git 忽略模式
├── prompts/
│   ├── step1_module_generation.txt    # 模块列表生成提示词
│   └── step2_figure_generation.txt    # 配图生成提示词
├── examples/
│   └── sample_input.txt       # 示例科研文本
├── outputs/                   # 生成的配图（自动创建）
└── README_CN.md               # 本文件
```

## 🎯 示例工作流程

```bash
$ python scientific_plotter.py -i examples/sample_input.txt

================================================================================
🚀 开始科研配图生成工作流程
================================================================================

📊 第一步：使用 gpt-5 生成模块列表...
✅ 模块列表生成成功！

================================================================================
MODULE LIST:
================================================================================
[你的架构的结构化分解...]
================================================================================

📝 模块列表已保存至: outputs/module_list_20231125_143022.txt

🎨 第二步：使用 gemini-2.5-flash-image 生成配图...
💾 正在从以下地址下载图片: [URL]
✅ 配图已保存至: outputs/scientific_figure_20231125_143022.png

================================================================================
🎉 工作流程成功完成！
================================================================================
📄 模块列表: outputs/module_list_20231125_143022.txt
🖼️  配图: outputs/scientific_figure_20231125_143022.png
================================================================================
```

## ⚙️ 配置选项

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `API_TYPE` | 图像生成 API 类型：`openai` 或 `gemini` | `openai` |
| `OPENAI_BASE_URL` | OpenAI 兼容 API 端点 URL | 必需 |
| `OPENAI_API_KEY` | OpenAI 兼容端点的 API 密钥 | 必需 |
| `GEMINI_API_KEY` | Google Gemini API 密钥（当 `API_TYPE=gemini` 时必需） | - |
| `ANALYSIS_MODEL` | 用于模块列表生成的模型 | `gpt-5` |
| `IMAGE_MODEL` | 用于配图生成的模型 | `gemini-2.5-flash-image` |
| `OUTPUT_DIR` | 输出文件目录 | `outputs` |

### 命令行选项

| 选项 | 简写 | 说明 |
|------|------|------|
| `--input FILE` | `-i` | 输入文本文件路径 |
| `--text TEXT` | `-t` | 科研文本字符串 |
| `--output FILE` | `-o` | 自定义输出路径 |
| `--module-list-only` | | 仅生成模块列表 |
| `--help` | | 显示帮助信息 |

## 🔍 获得最佳效果的技巧

1. **提供清晰的文本**：输入文本越详细和结构化，生成的模块列表越好
2. **描述数据流**：明确提及组件之间的数据流和连接
3. **指定组件**：在架构中命名特定的层、块或机制
4. **检查模块列表**：在生成配图前检查生成的模块列表
5. **迭代优化**：可以用修改后的模块列表重新生成配图进行微调

## 🐛 故障排除

**问题**：`Error initializing plotter`
- **解决方案**：确保 `.env` 文件存在且包含有效的 API 凭证

**问题**：`FileNotFoundError: Prompt template not found`
- **解决方案**：确保 `prompts/` 目录存在且包含两个模板文件

**问题**：API 连接错误
- **解决方案**：验证 `OPENAI_BASE_URL` 和 `OPENAI_API_KEY` 是否正确

**问题**：图片生成失败
- **解决方案**：检查你的 API 端点是否支持 `gemini-2.5-flash-image` 模型

## 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📝 许可证

本项目开源并遵循 [MIT 许可证](LICENSE)。

## 🙏 致谢

- 提示词模板基于 NeurIPS/ICLR 配图设计原则
- 由 OpenAI 兼容 API 端点提供支持
- 使用 GPT-5 进行分析，Gemini-2.5-flash-image（nano banana）进行生成

---

**祝你科研绘图愉快！🎨✨**

如有问题，请在 GitHub 上提交 issue。
