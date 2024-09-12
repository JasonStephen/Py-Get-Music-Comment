@echo off
:: 检查 .venv 目录是否存在
if exist ".venv" (
    echo Virtual environment already exists.
) else (
    echo Virtual environment not found. Creating .venv...
    python -m venv .venv
)

:: 激活虚拟环境
call .venv\Scripts\activate

:: 检查 requirements.txt 是否存在
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. No dependencies installed.
)

:: 提示完成
echo Environment setup is complete.
pause
