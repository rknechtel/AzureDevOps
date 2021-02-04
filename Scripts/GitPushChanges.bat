
@echo off
setlocal EnableDelayedExpansion
REM ************************************************************************
REM Script: GitPushChanges.bat
REM Author: Richard Knechtel
REM Date: 02/13/2020
REM Description: This script will push code changes to Azure Repos (Git). 
REM
REM LICENSE: 
REM This script is in the public domain, free from copyrights or restrictions.
REM
REM ************************************************************************

echo.
echo Running as user: %USERNAME%
echo.

REM Get parameters
set GITCOMMITCOMMENT=%1

echo.
echo Parameters Passed: 
echo Git Commit Comment: %GITCOMMITCOMMENT% 
echo.

REM Check if we got ALL parameters
if "!GITCOMMITCOMMENT!"=="" goto usage

REM Pushing Code Changes to Azure Repos (Git)
@echo GitPushChanges.bat running
@echo Pushing Code Changes to Azure Repos (Git)
git add .
git commit -m "%GITCOMMITCOMMENT%"
git push origin master

REM Lets get out of here!
goto getoutofhere

:usage
set ERRORNUMBER=1
echo [USAGE]: GitPushChanges.bat arg1
echo arg1 = Git Commit Comment (Example: "Changed version in pom.") 
goto getoutofhere

REM ****************************************************************************
REM Exit Script
REM ****************************************************************************
:getoutofhere
Exit /B %ERRORNUMBER%