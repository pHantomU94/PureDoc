
# PureDoc 

**PureDoc** 是一款专为 macOS 设计的轻量级文档转换工具。它能够将 LLM（如 ChatGPT、Claude）生成的 Markdown 内容完美转换为排版整洁的 Word (.docx) 文档。

## 🛠️ 环境依赖

在运行本项目之前，请确保您的 Mac 已安装以下工具：

1. **Python 3.10+**: 推荐使用 3.11 或 3.12 版本以获得最佳兼容性。
2. **Pandoc**: 文档转换的核心引擎。
* 安装命令：`brew install pandoc`


3. **Microsoft Word**: 用于生成预览模板及最终查看文档。

---

## 🚀 部署方法

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/PureDoc.git
cd PureDoc

```

### 2. 创建并激活虚拟环境 (推荐)

```bash
python3 -m venv .venv
source .venv/bin/activate

```

### 3. 安装依赖

```bash
pip install flet pypandoc

```

### 4. 准备必要文件

确保 `app.py` 所在的同级目录下包含以下文件：

* `bullet_process.lua`: 处理列表及换行的核心脚本。
* `template.docx`: Word 样式模板（若不存在，程序首次运行会自动生成）。

---

## 📖 使用方法

1. **启动程序**:
```bash
python3 app.py

```


1. **粘贴内容**: 将 Markdown 文本粘贴到左侧输入框。
2. **调整选项**:
* 勾选 **"忽略 Bullet (•)"**：移除无序列表的圆点，使文本靠左对齐。
* 调整 **"数字列表"**：决定保留或转换有序列表。


4. **即时预览**:
* 右侧区域：查看文本处理后的逻辑结构。
* 点击 **👁️ (预览图标)**：弹出 macOS 原生 QuickLook 窗口，查看真实的 Word 版式（字体、边距等）。


5. **导出结果**: 点击 **"导出 Word"**，选择保存路径，转换完成后会自动为您打开文件。

---

## 📂 项目结构

```text
.
├── app.py                # Flet GUI 应用程序主代码
├── bullet_process.lua       # Pandoc Lua 过滤器 (处理列表和换行)
├── template.docx         # Word 导出样式参考模板
├── requirements.txt      # 项目依赖清单
└── README.md             # 项目说明文档

```

---

## 📜 开源协议

本项目采用 [MIT License](https://www.google.com/search?q=LICENSE) 许可协议。

---

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request 来完善这个项目。

* 如果您在使用 Python 3.14 (Beta) 版本时遇到 API 兼容性问题，请及时反馈。
* 如果您有更好的 Lua 过滤器实现方案，欢迎分享。
