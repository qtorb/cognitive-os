@echo off
chcp 65001 >nul

REM Cambiar a la carpeta del proyecto
cd /d "%~dp0"

REM Esperar un poco para que el servidor inicie
echo Abriendo el navegador en 3 segundos...
timeout /t 3 /nobreak

REM Abrir el archivo HTML en el navegador predeterminado
start "" "onboarding.html"

echo.
echo Navegador abierto. Si no aparece en 5 segundos, abre manualmente:
echo %cd%\onboarding.html
echo.
echo O visita: http://127.0.0.1:8000
