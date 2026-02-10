import os
import stat
from pathlib import Path

def get_resource_path(relative_path) -> str:
    """
    get assets real url
    """
    current_file = Path(__file__).resolve()
    
    src_root = current_file.parent.parent.parent
    
    resource_path = src_root / "assets" / relative_path
    
    return str(resource_path)

def get_pandoc_path() -> str:
    # 定位到 assets/bin/pandoc
    path = get_resource_path("bin/pandoc")
    
    # 关键一步：确保打包后的二进制文件具有“可执行”权限
    if os.path.exists(path):
        current_stat = os.stat(path)
        os.chmod(path, current_stat.st_mode | stat.S_IEXEC)
        
    return path

# get download path
def get_download_path() -> str:
    """
    get current user's downloads path
    """
    download_path = Path.home() / "Downloads"
    
    # check if existed
    if not download_path.exists():
        # return home if not exited
        return str(Path.home())
        
    return str(download_path)