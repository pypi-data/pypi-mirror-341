@echo off

REM �������⻷��
echo ���ڼ������⻷��...
call .venv\Scripts\activate

REM ִ�� uv build
echo ���ڹ�����Ŀ...
uv build
if %errorlevel% neq 0 (
    echo ����ʧ�ܣ����������־��
    pause
    exit /b 1
)

REM ִ�� uv publish
echo ���ڷ�����Ŀ...
uv publish --username __token__ --password %PYPI_TOKEN%
if %errorlevel% neq 0 (
    echo ����ʧ�ܣ����������־��
    pause
    exit /b 1
)

echo ��Ŀ�����ͷ����ɹ���
pause