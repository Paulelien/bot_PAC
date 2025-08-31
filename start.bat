@echo off
echo ========================================
echo    Chatbot PAC - Iniciando Sistema
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8 o superior
    pause
    exit /b 1
)

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

REM Verificar si las dependencias están instaladas
if not exist "venv\Lib\site-packages\flask" (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

REM Verificar archivo .env
if not exist ".env" (
    echo.
    echo ADVERTENCIA: No se encontró el archivo .env
    echo Por favor, crea un archivo .env con tu API key de OpenAI
    echo Ejemplo:
    echo OPENAI_API_KEY=tu_api_key_aqui
    echo.
    echo ¿Deseas continuar sin configurar OpenAI? (s/n)
    set /p continue=
    if /i not "%continue%"=="s" (
        echo Configuración cancelada
        pause
        exit /b 1
    )
)

echo.
echo Iniciando Chatbot PAC...
echo.
echo La aplicación estará disponible en: http://localhost:5000
echo Presiona Ctrl+C para detener el servidor
echo.

REM Iniciar la aplicación
python app.py

pause
