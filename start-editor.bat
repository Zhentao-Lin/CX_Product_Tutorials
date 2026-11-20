@echo off
cd /d %~dp0
title CX Tutorial Editor
python -m pip install -q -r requirements-editor.txt
python tools\tutorial_editor\app.py
pause