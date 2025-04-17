@echo off
chcp 65001

REM 激活虚拟环境
call .venv\Scripts\activate

REM 设置 PyPI 用户名和密码
set UV_PYPI_USERNAME=__token__
set UV_PYPI_PASSWORD=%PYPI_TOKEN%

REM 执行 uv build
echo 正在构建项目...
uv build
if %errorlevel% neq 0 (
    echo 构建失败，请检查错误日志。
    pause
    exit /b 1
)

REM 执行 uv publish
echo 正在发布项目...
uv publish
if %errorlevel% neq 0 (
    echo 发布失败，请检查错误日志。
    pause
    exit /b 1
)

echo 项目构建和发布成功！
pause