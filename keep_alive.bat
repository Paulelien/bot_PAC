@echo off
echo 🚀 Iniciando keep-alive para API del Chatbot PAC
echo 📡 URL: http://localhost:5001/api/health
echo ⏰ Intervalo: 1 minuto
echo ================================================

:loop
echo.
echo ✅ [%time%] Verificando API...
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:5001/api/health
timeout /t 60 /nobreak > nul
goto loop

