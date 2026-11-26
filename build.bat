@echo off
cd /d %~dp0
python "03-网站系统-勿动\tools\cx_docs.py" build %*
