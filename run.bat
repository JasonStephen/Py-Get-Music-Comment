@echo off
:: 检查 .venv 是否存在
if not exist ".venv" (
    echo Virtual environment not found. Please run setup_env.bat first.
    pause
    exit /b
)

:: 激活虚拟环境
call .venv\Scripts\activate

:: 运行 Python 脚本
echo App is running now!
python getcomment.py

echo App stopped by user or accident, press any key to quit...

:: 保持窗口打开
pause