# PureDoc

**PureDoc** 是一款跨平台的轻量级文档转换工具。它能够将 LLM（如 ChatGPT、Claude）生成的 Markdown 内容完美转换为排版整洁的 Word (.docx) 文档。

## ✨ 新特性 (V1)

- 🎨 **Typora 风格 UI** - 简洁优雅的界面设计
- 📥 **Markdown 导入** - 支持导入 .md 文件
- 📄 **自定义模板** - 可选择自定义 Word 模板
- 💾 **导出路径选择** - 自由选择保存位置和文件名
- ⚙️ **配置文件化** - 所有设置自动保存
- 📦 **Mac 打包支持** - 可打包为 .app 应用

## 🛠️ 环境依赖

在运行本项目之前，请确保您的系统已安装以下工具：

1. **Python 3.10+**: 推荐使用 3.11 或 3.12 版本以获得最佳兼容性。
2. **Pandoc**: 文档转换的核心引擎。
   * macOS: `brew install pandoc`
   * Windows: 访问 [pandoc.org](https://pandoc.org/installing.html) 下载安装
   * Linux: `sudo apt install pandoc`
3. **Microsoft Word**: 用于生成预览模板及最终查看文档（可选）。

---

## 🚀 安装方法

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/PureDoc.git
cd PureDoc
```

### 2. 创建并激活虚拟环境 (推荐)

```bash
python3 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 📖 使用方法

### 启动程序

```bash
python app.py
```

### 主要功能

#### 1. 导入 Markdown 文件

点击工具栏的 📥 图标，选择要导入的 `.md` 文件，内容将自动加载到左侧编辑器。

#### 2. 粘贴内容

直接将 Markdown 文本粘贴到左侧输入框。

#### 3. 调整选项

- **忽略 Bullet (•)**：移除无序列表的圆点，使文本靠左对齐
- **保留数字列表**：决定保留或转换有序列表
- **列表样式**：选择"转为纯文本"或"Word 自动列表"

#### 4. 自定义模板

点击"模板"按钮，选择您自己的 Word 模板文件（.docx）。模板设置会自动保存，下次启动时自动加载。

#### 5. 实时预览

- **右侧预览区**：查看文本处理后的逻辑结构
- **原生预览按钮** (👁️)：弹出系统原生预览窗口，查看真实的 Word 版式

#### 6. 导出 Word

点击 💾 图标，选择保存路径和文件名，导出完成后会自动打开文件。

---

## 📂 项目结构

```text
PureDoc/
├── app.py                    # 应用入口
├── build.py                  # Mac 打包脚本
├── bullet_process.lua        # Pandoc Lua 过滤器
├── config.json              # 配置文件（运行时生成）
├── requirements.txt         # Python 依赖
├── src/
│   ├── config/
│   │   └── manager.py      # 配置管理
│   ├── core/
│   │   └── converter.py    # 转换逻辑
│   ├── ui/
│   │   ├── theme.py        # 主题配置
│   │   ├── toolbar.py      # 工具栏组件
│   │   └── main_page.py   # 主页面组件
│   └── utils/
│       ├── file_picker.py  # 文件选择器
│       └── platform.py     # 平台工具
└── PRD/
    └── 需求文档V1.md      # 需求文档
```

---

## 📦 打包为 Mac 应用

```bash
python build.py
```

打包完成后，应用位于 `build/PureDoc.app`。

**注意**：
- 确保 Pandoc 已安装
- 首次运行会自动生成配置文件

---

## ⚙️ 配置文件

`config.json` 配置示例：

```json
{
  "template": {
    "path": "/path/to/template.docx",
    "auto_generate": true
  },
  "export": {
    "default_directory": "/Users/xxx/Desktop",
    "default_filename": "Output.docx"
  },
  "ui": {
    "theme": "light",
    "ignore_bullets": true,
    "preserve_numbered_lists": true,
    "numbered_list_style": "text"
  }
}
```

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 许可协议。

---

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request 来完善这个项目。
