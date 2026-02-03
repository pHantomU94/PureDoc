import flet as ft
import pypandoc
import os
import subprocess
import sys
import time

# 引入 Lua 脚本文件名
LUA_SCRIPT = "bullet_process.lua"
TEMPLATE_DOC = "template.docx"

def main(page: ft.Page):
    page.title = "PureDoc"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- 1. 核心逻辑区 ---
    
    def get_pandoc_args(is_export=False):
        """生成 Pandoc 参数"""
        args = ['--from=markdown+hard_line_breaks']
        
        # 实时获取 Checkbox 状态
        if chk_bullet.value:
            args.append("--metadata=ignore_bullets=true")
        
        # 处理导出或预览的通用逻辑
        if is_export:
            if not os.path.exists(TEMPLATE_DOC):
                try:
                    subprocess.run(['pandoc', '-o', TEMPLATE_DOC, '--print-default-data-file', 'reference.docx'], check=True)
                except Exception:
                    pass
            args.append(f'--reference-doc={TEMPLATE_DOC}')
        
        # 无论是预览还是导出，都要挂载 Lua 脚本
        args.append(f'--lua-filter={LUA_SCRIPT}')
        args.append('--wrap=none')
            
        return args

    def convert_for_preview(md_text):
        if not md_text:
            return ""
        try:
            # 内部预览使用 Markdown
            processed_md = pypandoc.convert_text(
                md_text, 
                'markdown', 
                format='markdown+hard_line_breaks',
                extra_args=get_pandoc_args(is_export=False)
            )
            return processed_md
        except Exception as e:
            return f"**预览错误**: {e}"

    def update_preview(e=None):
        """刷新预览"""
        raw_content = txt_input.value
        processed_content = convert_for_preview(raw_content)
        markdown_view.value = processed_content
        markdown_view.update()

    def show_message(message, is_error=False):
        color = ft.Colors.RED if is_error else ft.Colors.GREEN
        icon_name = ft.Icons.ERROR if is_error else ft.Icons.CHECK
        snack = ft.SnackBar(content=ft.Row([ft.Icon(icon_name, color=color), ft.Text(message)]), open=True)
        try:
            page.overlay.append(snack)
            page.update()
        except Exception:
            print(f">> {message}")

    # Mac 原生预览置顶逻辑
    def native_preview(e):
        if not txt_input.value: return
        
        # 1. 生成带模板的临时 Word
        temp_docx = os.path.abspath("temp_ql.docx")
        try:
            pypandoc.convert_text(
                txt_input.value, 
                'docx', 
                format='markdown+hard_line_breaks', 
                outputfile=temp_docx, 
                extra_args=get_pandoc_args(is_export=True) # 使用导出参数来看最终效果
            )
            
            if sys.platform == "darwin":
                # Mac: 启动 qlmanage
                ql_process = subprocess.Popen(
                    ["qlmanage", "-p", temp_docx], 
                    stderr=subprocess.DEVNULL, 
                    stdout=subprocess.DEVNULL
                )
                
                # 【关键 trick】等待 0.2 秒让窗口出来，然后用 AppleScript 强行置顶
                time.sleep(0.2)
                # 这段脚本会告诉 System Events 把名为 qlmanage 的进程提到最前面
                applescript = '''
                tell application "System Events"
                    set frontmost of (every process whose name is "qlmanage") to true
                end tell
                '''
                subprocess.run(["osascript", "-e", applescript])
                
                show_message("已打开原生预览")
            else:
                # Windows
                os.startfile(temp_docx) # type: ignore

        except Exception as ex:
            show_message(f"预览失败: {ex}", is_error=True)

    def export_word(e):
        if not txt_input.value:
            show_message("内容为空！", is_error=True)
            return
        temp_md = "temp_flet.md"
        with open(temp_md, "w", encoding="utf-8") as f: f.write(txt_input.value)
        output_filename = "Output.docx"
        try:
            pypandoc.convert_file(temp_md, 'docx', outputfile=output_filename, extra_args=get_pandoc_args(is_export=True))
            if sys.platform == "win32": os.startfile(output_filename) # type: ignore
            else: subprocess.call(["open", output_filename])
            show_message(f"成功导出: {output_filename}")
        except Exception as ex: show_message(str(ex), is_error=True)
        finally: 
            if os.path.exists(temp_md): os.remove(temp_md)
    
    # --- 2. UI 布局区 ---

    # 输入框
    txt_input = ft.TextField(
        multiline=True, expand=True, border_color=ft.Colors.GREY_300, 
        hint_text="粘贴 Markdown 内容到这里...", text_size=14
    )
    # 【修复1】绑定监听
    txt_input.on_change = update_preview

    # 预览链接处理
    async def handle_link_tap(e):
        if e.data: await page.launch_url(str(e.data))

    markdown_view = ft.Markdown(
        value="预览区域", selectable=True, 
        extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED, 
        on_tap_link=handle_link_tap, 
    )
    
    preview_container = ft.Container(
        content=ft.Column([markdown_view], scroll=ft.ScrollMode.AUTO),
        bgcolor="white", padding=20, border=ft.Border.all(1, ft.Colors.GREY_300), 
        border_radius=5, expand=True
    )

    # 选项控件
    chk_bullet = ft.Checkbox(label="忽略 Bullet (•)", value=True)
    chk_num = ft.Checkbox(label="保留数字列表", value=True)
    
    # 手动绑定事件，让勾选立即生效
    chk_bullet.on_change = update_preview
    chk_num.on_change = update_preview
    
    dd_style = ft.Dropdown(
        width=200,
        options=[ft.dropdown.Option("Text (1. )", text="转为纯文本"), ft.dropdown.Option("List", text="Word 自动列表")],
        value="Text (1. )"
    )
    # 手动绑定事件
    dd_style.on_change = update_preview

    # 按钮组
    btn_preview = ft.IconButton(
        icon=ft.Icons.PREVIEW, 
        tooltip="Mac 真实 Word 预览", 
        on_click=native_preview,
        icon_color=ft.Colors.BLUE
    )

    btn_export = ft.FilledButton(
        "导出 Word", icon=ft.Icons.SAVE, on_click=export_word,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    )

    toolbar = ft.Row(
        controls=[
            ft.Text("选项:", weight=ft.FontWeight.BOLD),
            chk_bullet, chk_num, dd_style, 
            ft.VerticalDivider(), 
            btn_preview, # 预览按钮
            btn_export
        ],
        alignment=ft.MainAxisAlignment.START
    )

    split_view = ft.Row(
        controls=[
            ft.Column([ft.Text("原始内容"), txt_input], expand=1),
            ft.VerticalDivider(width=1, color=ft.Colors.GREY_200),
            ft.Column([ft.Text("转换后预览"), preview_container], expand=1),
        ],
        expand=True
    )

    page.add(toolbar, ft.Divider(), split_view)

if __name__ == "__main__":
    try: ft.app(main)
    except: ft.app(target=main)