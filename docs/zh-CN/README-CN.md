# PureDoc

## 工具简介

**PureDoc** 是一款轻量级的 Markdown 转 Word 文档转换工具，专为处理由 LLM（如 ChatGPT、Claude）生成的内容而设计。它能够将 Markdown 格式的内容快速转换为排版整洁的 Word (.docx) 文档，并提供实时预览功能，让文档处理更加便捷高效。

---

## 适配平台

| 平台 | 支持状态 | 备注 |
|------|----------|------|
| macOS | ✅ 完全支持 | 推荐使用 macOS 12.0 及以上版本 |
| Windows | 🚧 计划中 | 未来版本将提供支持 |
| Linux | 🚧 计划中 | 未来版本将提供支持 |

---

## 当前支持功能

✅ **内容输入**：支持通过文件选择器导入 `.md` 或 `.markdown` 格式的文件，或直接将 Markdown 格式文本粘贴到编辑区域
✅ **Markdown 转 Word**：支持将 Markdown 内容转换为标准的 Word (.docx) 文档格式
✅ **期望转换的word模板支持**：可选择自定义的 Word 模板文件（.docx），应用于输出文档，同时内置默认模板，开箱即用
✅ **列表样式控制**
- **Bullet Point 处理**：
  - 可选择忽略无序列表符号（•），使文本靠左对齐
  - 保留原始无序列表格式
- **Number List 处理**：
  - **转为纯文本**：将有序列表转换为纯文本格式（如 "1. 2. 3."）
  - **Word 自动列表**：保持为 Word 的原生自动编号列表格式
  - **忽略序号**：移除所有数字序号

✅ **Mac 原生预览**：支持使用 macOS QuickLook 查看转换后的 Word 文档效果
✅ **Word 文件导出**：可选择保存路径和文件名，导出完成后自动打开文件

---

## 工具安装方法 (macOS)

### 方式一：从 Release 下载预编译版本

1. **下载应用**
   - 从项目的 [Releases](https://github.com/yourusername/PureDoc/releases) 页面下载最新版本的 `.dmg` 文件
   - 或下载已打包的 `PureDoc.app` 压缩包

2. **安装到 Applications**

   **方法 A：拖拽安装（推荐）**
   ```bash
   # 解压下载的文件
   unzip PureDoc-0.1.0.zip
   # 将 PureDoc.app 拖拽到 /Applications 文件夹
   ```

   **方法 B：命令行安装**
   ```bash
   # 解压下载的文件
   unzip PureDoc-0.1.0.zip
   # 复制到 Applications 文件夹
   cp -r PureDoc.app /Applications/
   ```

3. **避免权限限制**

   如果遇到"无法打开，因为无法验证开发者"的提示，执行以下操作：

   **方法 A：系统设置（推荐）**
   1. 打开「系统设置」→「隐私与安全性」
   2. 在"已阻止使用此应用"部分，找到 PureDoc
   3. 点击"仍要打开"按钮
   4. 输入管理员密码确认

   **方法 B：命令行移除隔离属性**
   ```bash
   xattr -cr /Applications/PureDoc.app
   ```
   然后再次尝试打开应用。

   **方法 C：首次打开允许**
   1. 右键点击 PureDoc.app，选择"打开"
   2. 在弹出对话框中点击"打开"
   3. 首次成功打开后，之后可直接双击打开

---

## 方法二：源码直接运行
### 前置依赖
**必需依赖：Pandoc**

Pandoc 是本工具的核心转换引擎，必须先安装：

```bash
# macOS 使用 Homebrew 安装
brew install pandoc

# 验证安装
pandoc --version
```
### 运行方法

```bash
pip3 install requirements.txt
flet run
```

---
## 方法三：源码编译方法

### 前置依赖

**必需依赖：Pandoc**

Pandoc 是本工具的核心转换引擎，必须先安装：

```bash
# macOS 使用 Homebrew 安装
brew install pandoc

# 验证安装
pandoc --version
```

### 编译步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/yourusername/PureDoc.git
   cd PureDoc
   ```

2. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **执行编译**
   ```bash
   python build.py
   ```

   编译脚本会自动：
   - 从 `src/__init__.py` 读取版本号
   - 同步版本到 `pyproject.toml`
   - 调用 Flet 构建工具生成 `.app` 文件

4. **获取编译产物**
   ```bash
   # 编译完成后，应用位于
   ls build/PureDoc.app
   ```

---

## 本项目使用的工具说明

### 核心依赖

| 工具/库 | 版本要求 | 用途说明 |
|---------|----------|----------|
| **Pandoc** | 2.19+ | 文档转换的核心引擎，负责 Markdown 到 Word 的格式转换 |
| **Python** | 3.10+ | 应用程序运行环境 |
| **Flet** | 0.80.5+ | 跨平台 UI 框架，提供简洁的桌面应用界面 |
| **PyPandoc** | 1.16.2+ | Pandoc 的 Python 封装库 |

### 开发依赖

```
flet==0.80.5          # UI 框架
pypandoc==1.16.2      # Pandoc Python 封装
toml==0.10.2          # 配置文件解析
```

### 资源文件

| 文件 | 说明 |
|------|------|
| `assets/scripts/bullet_process.lua` | Pandoc Lua 过滤器，处理列表格式和软回车 |
| `assets/template/template.docx` | 默认 Word 模板 |
| `assets/icon.png` | 应用图标 |

### Lua 过滤器功能

`bullet_process.lua` 脚本提供了以下处理能力：

- **软回车处理**：将段落内的软换行符转换为独立的段落
- **无序列表控制**：根据配置决定是否添加/移除 bullet 符号 (•)
- **有序列表控制**：支持三种模式（纯文本、Word 列表、忽略序号）

---

## 开源协议

本项目采用 [MIT License](LICENSE) 许可协议。

---


## 反馈与贡献

欢迎提交 [Issue](https://github.com/yourusername/PureDoc/issues) 或 Pull Request 来完善这个项目。
