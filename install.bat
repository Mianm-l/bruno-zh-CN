@echo off
:: ========================================================
:: Bruno 全能中文汉化补丁一键安装工具
:: ========================================================
title 安装 Bruno 中文汉化补丁
chcp 65001 >nul
cd /d "%~dp0"

echo 正在启动 Bruno 中文汉化安装程序...
python "%~dp0patch.py" %*

if %errorlevel% neq 0 (
    echo.
    echo 安装过程中遇到错误，请检查权限或路径后重试。
)

echo.
pause
