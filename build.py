import os
import re
import sys
import toml
import subprocess
import shutil
from pathlib import Path

# 获取脚本所在目录（项目根目录）
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR

def get_version():
    """从 src/__init__.py 中通过正则匹配获取 __version__"""
    init_path = PROJECT_ROOT / "src" / "__init__.py"
    if not init_path.exists():
        print(f"❌ 错误: 未找到 {init_path}")
        sys.exit(1)
        
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()
        # 匹配格式如 __version__ = "0.1.0" 或 __version__ = '1.2.3'
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    
    print("❌ 错误: 在 src/__init__.py 中未找到 __version__ 定义")
    sys.exit(1)

def update_pyproject_toml(version):
    """更新 pyproject.toml 中的 version 字段"""
    toml_path = PROJECT_ROOT / "pyproject.toml"
    if not toml_path.exists():
        print("❌ 错误: 未找到 pyproject.toml")
        sys.exit(1)

    data = toml.load(toml_path)
    
    # 更新 project 节点下的 version
    if "project" in data:
        old_version = data["project"].get("version", "未知")
        data["project"]["version"] = version
        
        with open(toml_path, "w", encoding="utf-8") as f:
            toml.dump(data, f)
        print(f"✅ 已更新 pyproject.toml: {old_version} -> {version}")
    else:
        print("❌ 错误: pyproject.toml 中缺少 [project] 节点")
        sys.exit(1)

def check_pandoc_in_system():
    """在系统中查找 pandoc 可执行文件路径"""
    # 尝试使用 which/where 查找 pandoc
    if sys.platform == "win32":
        cmd = ["where", "pandoc"]
    else:
        cmd = ["which", "pandoc"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        pandoc_path = result.stdout.strip()
        if pandoc_path and Path(pandoc_path).exists():
            return pandoc_path
    except subprocess.CalledProcessError:
        pass

    return None


def copy_pandoc_to_assets(pandoc_path):
    """将 pandoc 复制到 assets 文件夹"""
    assets_pandoc_dir = PROJECT_ROOT / "assets" / "bin" 
    assets_pandoc_dir.mkdir(parents=True, exist_ok=True)

    dest_path = assets_pandoc_dir / "pandoc"

    try:
        shutil.copy2(pandoc_path, dest_path)
        # macOS/Linux 需要设置执行权限
        if sys.platform != "win32":
            os.chmod(dest_path, 0o755)
        print(f"✅ 已将 pandoc 复制到 assets/bin/pandoc")
        return True
    except Exception as e:
        print(f"❌ 复制 pandoc 失败: {e}")
        return False


def check_assets():
    """检查资源文件，处理缺失情况"""
    print("\n🔍 检查资源文件...")

    assets_dir = PROJECT_ROOT / "assets"
    lua_script = assets_dir / "scripts" / "bullet_process.lua"
    template = assets_dir / "template" / "template.docx"
    pandoc_dir = assets_dir / "bin" /"pandoc"

    warnings = []
    pandoc_found = False

    # 检查 Lua 脚本
    if not lua_script.exists():
        warnings.append(f"⚠️  警告: 未找到 Lua 脚本: {lua_script}")
    else:
        print(f"✅ Lua 脚本存在: {lua_script}")

    # 检查 Template
    if not template.exists():
        warnings.append(f"⚠️  警告: 未找到模板文件: {template}")
    else:
        print(f"✅ 模板文件存在: {template}")

    # 检查 Pandoc
    if not pandoc_dir.exists():
        print(f"⚠️  未找到 assets/pandoc 目录，尝试从系统查找 pandoc...")
        system_pandoc = check_pandoc_in_system()
        if system_pandoc:
            if copy_pandoc_to_assets(system_pandoc):
                pandoc_found = True
            else:
                print("❌ 错误: 无法复制 pandoc 到 assets 目录")
                sys.exit(1)
        else:
            print("❌ 错误: 系统中未找到 pandoc")
            print("💡 请先安装 pandoc:")
            print("   macOS: brew install pandoc")
            print("   Ubuntu/Debian: sudo apt install pandoc")
            print("   Windows: 下载安装包 https://pandoc.org/installing.html")
            sys.exit(1)
    else:
        print(f"✅ Pandoc 目录存在: {pandoc_dir}")

    # 打印警告
    if warnings:
        print("\n⚠️  以下资源文件缺失，将使用默认设置:")
        for warning in warnings:
            print(f"   {warning}")
        print("")

    return True


def run_build():
    """执行构建命令"""
    print("🚀 开始执行 flet build...")

    # 切换到 src 目录执行构建，以对齐路径视角
    # 此时入口是 main.py，因为我们已经在 src 内部了
    cmd = [
        "flet", "build", "macos",
    ]

    try:
        # 使用 src 作为工作目录
        subprocess.run(cmd, cwd=str(PROJECT_ROOT), check=True)
        print("🎉 构建成功！")
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 1. 获取版本
    ver = get_version()
    # 2. 同步版本
    update_pyproject_toml(ver)
    # 3. 检查资源
    check_assets()
    # 4. 执行构建
    run_build()