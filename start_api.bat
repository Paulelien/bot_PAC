@echo off
echo ========================================
echo    API del Chatbot PAC para LMS
echo ========================================
echo.

echo 🔍 Verificando configuración...
if not exist ".env" (
    echo ❌ ERROR: Archivo .env no encontrado
    echo Por favor, crea el archivo .env con tu configuración
    echo.
    pause
    exit /b 1
)

echo ✅ Archivo .env encontrado
echo.

echo 🚀 Iniciando API del Chatbot PAC...
echo 📍 Puerto: 5001
echo 🌐 URL: http://localhost:5001
echo 📚 API Docs: http://localhost:5001/api/health
echo.

echo ⏳ Iniciando servidor...
python api_lms.py

echo.
echo ❌ El servidor se ha detenido
pause
