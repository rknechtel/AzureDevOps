@echo off
setlocal EnableDelayedExpansion
REM ************************************************************************
REM Script: GetADOGitProjects.bat
REM Author: Richard Knechtel
REM Date: 03/08/2021
REM Description: This script will allow you get a list of all Git Projects
REM              in an Azure DevOps Project
REM
REM LICENSE: 
REM This script is in the public domain, free from copyrights or restrictions.
REM
REM Example Call:
REM GetADOGitProjects.bat MyADOProject MyUserName 1cxcbknj5e2f5z7iserleu6tp3rudjh9hsezp1rk5remeuck3gty
REM
REM ************************************************************************

@echo.
@echo Running as user: %USERNAME%
@echo.

REM Get parameters
@echo Parameters Passed = %1 %2 ******
@echo.

set ADOPROJECT=%1
set ADOUSERNAME=%2
set ADOPAT=%3

REM Check if we got ALL parameters
if "!ADOPROJECT!"=="" goto usage
if "!ADOUSERNAME!"=="" goto usage
if "!ADOPAT!"=="" goto usage
if "!ADOPROJECT!"=="" if "!ADOUSERNAME!"=="" if "!ADOPAT!"=="" (
   goto usage
)

REM set Script Path
REM set SCRIPTPATH=C:\Scripts\Python\GetADOGitProjects

@echo

@echo
*********************************************************************************************************
@echo Starting GetADOGitProjects
@echo
*********************************************************************************************************

call python %SCRIPTPATH%\GetADOGitProjects.py %ADOPROJECT% %ADOUSERNAME% %ADOPAT%

REM Lets get out of here!
goto getoutofhere


:usage
set ERRORNUMBER=1
echo [USAGE]: GetADOGitProjects.bat arg1 arg2 arg3
echo arg1 = ADO Project Name (Example: MyADOProject)
echo arg2 = Username (Example: MyUsername)
echo arg3 = ADO Personal Access Token (Example: 1cxcbknj5e2f5z7iserleu6tp3rudjh9hsezp1rk5remeuck3gty)

goto getoutofhere

:getoutofhere
Exit /B

REM END