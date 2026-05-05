@echo off
REM Automated push script for Law Analyse MVP (Windows)

echo.
echo Law Analyse MVP - Push to GitHub
echo ====================================
echo.

REM Check git config
echo Checking git configuration...
for /f "tokens=*" %%i in ('git config user.name') do set GIT_USER=%%i
for /f "tokens=*" %%i in ('git config user.email') do set GIT_EMAIL=%%i
echo    User: %GIT_USER% ^<%GIT_EMAIL%^>

if not "%GIT_USER%"=="nposeo" (
    echo Warning: Git user is not 'nposeo'
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

REM Show statistics
echo.
echo Project statistics:
for /f %%i in ('git rev-list --count HEAD') do echo    Commits: %%i
echo    Author: %GIT_USER% ^<%GIT_EMAIL%^>

REM Confirm push
echo.
set /p CONFIRM="Push to GitHub? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Push cancelled
    exit /b 1
)

REM Push to GitHub
echo.
echo Pushing to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Successfully pushed to GitHub!
    echo.
    echo Next steps:
    echo 1. Open: https://github.com/nposeo/law-analyse
    echo 2. Add Topics: legal-tech, ai, nlp, ukrainian-law
    echo 3. Configure Secrets: OPENAI_API_KEY
    echo 4. Create Release v1.0.0
    echo.
    echo See GITHUB_SETUP.md for details
) else (
    echo.
    echo Push failed!
    echo.
    echo Common issues:
    echo - Authentication failed: Use Personal Access Token
    echo - Repository not found: Create repository on GitHub first
    echo - Permission denied: Check you're logged in as nposeo
    echo.
    echo See PUSH_INSTRUCTIONS.md for troubleshooting
    exit /b 1
)

pause
