@echo off
echo Starting process...
echo.
:EnterName
Set /p Process="Enter bot.py: "
IF NOT EXIST %Process% GOTO EnterName
:begin
title Kukuruza
tasklist | findstr %Process%
if errorlevel 1 goto NoProcess
echo Result: Process run
goto Done
:NoProcess
%Process%
echo Result: Process %Process% stop %time%
:Done
echo.
goto begin
pause
exit