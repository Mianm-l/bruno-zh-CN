# -*- coding: utf-8 -*-
"""
Bruno 官方原生英文还原/卸载脚本 (Bruno Restore to English)
"""

import os
import sys
import shutil
import subprocess

DEFAULT_PATHS = [
    r"D:\Program Files\Bruno",
    r"C:\Program Files\Bruno",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Bruno")
]

def find_bruno_dir():
    # 0. 优先检测当前脚本所在目录是否就是 Bruno 根目录
    if os.path.exists(os.path.join(CURRENT_DIR, "resources", "app.asar")):
        return CURRENT_DIR
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        return sys.argv[1]
    for p in DEFAULT_PATHS:
        if os.path.exists(os.path.join(p, "resources", "app.asar.bak")):
            return p
        if os.path.exists(os.path.join(p, "resources", "app.asar")):
            return p
    user_input = input("请输入 Bruno 安装根目录: ").strip(' "\'')
    if user_input and os.path.exists(os.path.join(user_input, "resources")):
        return user_input
    return None

def stop_bruno():
    print("[1/3] 正在关闭运行中的 Bruno 进程...")
    try:
        cmd = "Get-CimInstance Win32_Process -Filter \"Name = 'Bruno.exe'\" | Invoke-CimMethod -MethodName Terminate"
        subprocess.run(["powershell", "-Command", cmd], capture_output=True, check=False)
    except Exception:
        pass

def restore():
    print("==================================================")
    print("   Bruno 中文补丁卸载 / 官方英文原版还原工具")
    print("==================================================")
    bruno_dir = find_bruno_dir()
    if not bruno_dir:
        print("未定位到有效 Bruno 安装目录！")
        sys.exit(1)

    resources_dir = os.path.join(bruno_dir, "resources")
    app_asar = os.path.join(resources_dir, "app.asar")
    app_bak = os.path.join(resources_dir, "app.asar.bak")

    if not os.path.exists(app_bak):
        print(f"错误: 未在 {resources_dir} 下检测到备份文件 (app.asar.bak)。无法自动恢复！")
        sys.exit(1)

    stop_bruno()

    print("[2/3] 正在从备份恢复原始 app.asar...")
    shutil.copyfile(app_bak, app_asar)

    print("[3/3] 恢复成功！")
    print("\n==================================================")
    print("Bruno 已成功还原为官方原生英文版本。")
    print("==================================================\n")

    start = input("是否立即启动 Bruno？(Y/n): ").strip().lower()
    if start != 'n':
        exe_path = os.path.join(bruno_dir, "Bruno.exe")
        if os.path.exists(exe_path):
            subprocess.Popen([exe_path])
            print("Bruno 已启动！")

if __name__ == "__main__":
    restore()
