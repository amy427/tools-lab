@echo off
chcp 65001 >nul
set /p folder=请输入要处理的文件夹路径：
echo.
echo 1) 仅预览（dry-run）
echo 2) 真正执行
set /p mode=请输入模式(1/2)：

if "%mode%"=="1" (
  py -3 "%~dp0batch_renamer.py" "%folder%" --only-images --dry-run
) else (
  py -3 "%~dp0batch_renamer.py" "%folder%" --only-images
)

pause
