@echo off
cd /d %~dp0
title CX Tutorial Editor
python -m pip install -q -r "03-网站系统-勿动\requirements-editor.txt"
python "03-网站系统-勿动\tools\tutorial_editor\app.py"
pause
