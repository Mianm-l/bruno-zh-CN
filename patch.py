# -*- coding: utf-8 -*-
"""
Bruno 简易中文汉化补丁自动安装器 (Bruno Chinese Localization Patch Installer)
适配版本：Bruno v4.3.0 及后续兼容小版本
"""

import os
import sys
import json
import shutil
import subprocess
import glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(CURRENT_DIR, "core")

DEFAULT_PATHS = [
    r"D:\Program Files\Bruno",
    r"C:\Program Files\Bruno",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Bruno")
]

def find_bruno_dir():
    # 0. 优先检测当前脚本所在目录是否就是 Bruno 根目录（放到软件目录下直接运行）
    if os.path.exists(os.path.join(CURRENT_DIR, "resources", "app.asar")):
        return CURRENT_DIR
    
    # 1. 命令行参数优先
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        return sys.argv[1]
    
    # 2. 检查常见默认安装路径
    for p in DEFAULT_PATHS:
        if os.path.exists(os.path.join(p, "resources", "app.asar")):
            return p
    
    # 3. 提示用户输入
    print("未在默认路径检测到 Bruno 安装目录。")
    user_input = input("请输入您的 Bruno 安装根目录 (例如 D:\\Program Files\\Bruno): ").strip(' "\'')
    if user_input and os.path.exists(os.path.join(user_input, "resources", "app.asar")):
        return user_input
    
    return None

def stop_bruno():
    print("[1/5] 正在检查并关闭运行中的 Bruno 进程...")
    try:
        cmd = "Get-CimInstance Win32_Process -Filter \"Name = 'Bruno.exe'\" | Invoke-CimMethod -MethodName Terminate"
        subprocess.run(["powershell", "-Command", cmd], capture_output=True, check=False)
    except Exception as e:
        print(f"提示: 关闭进程命令执行完成: {e}")

def run_node_script(script_content):
    res = subprocess.run(["node", "-e", script_content], capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        raise RuntimeError(f"Node 执行错误: {res.stderr}")
    return res.stdout

def apply_patch(bruno_dir):
    resources_dir = os.path.join(bruno_dir, "resources")
    app_asar = os.path.join(resources_dir, "app.asar")
    app_bak = os.path.join(resources_dir, "app.asar.bak")

    if not os.path.exists(app_asar):
        print(f"错误: 未在 {resources_dir} 下找到 app.asar 文件！")
        return False

    # 1. 备份原版
    print("[2/5] 正在创建原生英文备份 (app.asar.bak)...")
    if not os.path.exists(app_bak):
        shutil.copyfile(app_asar, app_bak)
        print("  -> 备份完成：已生成 app.asar.bak")
    else:
        print("  -> 备份已存在，保留首次备份文件。")

    temp_unpack_dir = os.path.join(CURRENT_DIR, "_temp_unpack")
    if os.path.exists(temp_unpack_dir):
        shutil.rmtree(temp_unpack_dir, ignore_errors=True)

    # 2. 解包 asar
    print("[3/5] 正在解包 app.asar 核心资源...")
    unpack_js = f"""
    const asar = require('C:/Users/61981/.gemini/antigravity/scratch/node_modules/asar');
    asar.extractAll({json.dumps(app_asar)}, {json.dumps(temp_unpack_dir)});
    """
    try:
        run_node_script(unpack_js)
    except Exception as e:
        # Fallback to npx asar
        print("尝试通过 npx asar 解包...")
        subprocess.run(["npx", "asar", "extract", app_asar, temp_unpack_dir], check=True)

    # 3. 注入汉化代码与替换静态词条
    print("[4/5] 正在注入全能中文语言包与界面词条...")
    
    # 3.1 注入 i18n-zh.js
    web_js_dir = os.path.join(temp_unpack_dir, "web", "static", "js")
    os.makedirs(web_js_dir, exist_ok=True)
    shutil.copyfile(os.path.join(CORE_DIR, "i18n-zh.js"), os.path.join(web_js_dir, "i18n-zh.js"))

    # 3.2 挂载到 index.html
    index_html_path = os.path.join(temp_unpack_dir, "web", "index.html")
    if os.path.exists(index_html_path):
        with open(index_html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        if "i18n-zh.js" not in html:
            html = html.replace("</head>", '<script defer src="static/js/i18n-zh.js"></script></head>')
            with open(index_html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print("  -> 已向 web/index.html 注册语言引擎引用")

    # 3.3 替换 index.*.js 中的静态词条
    replacements_file = os.path.join(CORE_DIR, "replacements.json")
    if os.path.exists(replacements_file):
        with open(replacements_file, 'r', encoding='utf-8') as f:
            replacements = json.load(f)

        index_js_files = glob.glob(os.path.join(web_js_dir, "index.*.js"))
        for jf in index_js_files:
            with open(jf, 'r', encoding='utf-8') as f:
                content = f.read()
            modified = False
            for item in replacements:
                t = item["target"]
                r = item["replacement"]
                if t in content:
                    content = content.replace(t, r)
                    modified = True
            if modified:
                with open(jf, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  -> 已完成静态词条直出优化: {os.path.basename(jf)}")

    # 3.4 替换 Electron 原生菜单模板
    menu_dest = os.path.join(temp_unpack_dir, "src", "app", "menu-template.js")
    if os.path.exists(menu_dest):
        shutil.copyfile(os.path.join(CORE_DIR, "menu-template.js"), menu_dest)
        print("  -> 已更新 Electron 系统顶栏菜单模版")

    # 4. 重新打包 asar
    print("[5/5] 正在重新打包并写入 app.asar...")
    temp_pack_asar = os.path.join(CURRENT_DIR, "_temp_app.asar")
    pack_js = f"""
    const asar = require('C:/Users/61981/.gemini\antigravity/scratch/node_modules/asar');
    asar.createPackage({json.dumps(temp_unpack_dir)}, {json.dumps(temp_pack_asar)}).then(() => {{
        console.log('done');
    }});
    """
    try:
        run_node_script(pack_js)
    except Exception as e:
        subprocess.run(["npx", "asar", "pack", temp_unpack_dir, temp_pack_asar], check=True)

    # 写入目标
    shutil.copyfile(temp_pack_asar, app_asar)

    # 清理临时目录
    if os.path.exists(temp_pack_asar):
        os.remove(temp_pack_asar)
    if os.path.exists(temp_unpack_dir):
        shutil.rmtree(temp_unpack_dir, ignore_errors=True)

    print("\n==================================================")
    print("恭喜！Bruno 中文汉化补丁已成功安装生效！")
    print(f"安装路径：{bruno_dir}")
    print("如需还原为官方英文原版，请随时运行 uninstall.bat 即可。")
    print("==================================================\n")
    return True

if __name__ == "__main__":
    print("==================================================")
    print("   Bruno 官方版本全能中文汉化补丁安装器 (v4.3.0)")
    print("==================================================")
    target_dir = find_bruno_dir()
    if not target_dir:
        print("未定位到有效 Bruno 目录，安装退出。")
        sys.exit(1)
    
    stop_bruno()
    success = apply_patch(target_dir)
    if success:
        start = input("是否立即启动 Bruno？(Y/n): ").strip().lower()
        if start != 'n':
            exe_path = os.path.join(target_dir, "Bruno.exe")
            if os.path.exists(exe_path):
                subprocess.Popen([exe_path])
                print("Bruno 已启动！")
