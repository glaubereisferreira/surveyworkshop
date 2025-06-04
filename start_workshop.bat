@echo off
echo.
echo ====================================================
echo        🎯 WORKSHOP CLARO - SISTEMA DE VOTACAO
echo ====================================================
echo.
echo 🚀 Iniciando sistema...
echo.

REM Mata processos anteriores
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM cloudflared.exe /T >nul 2>&1

echo 📦 Verificando dependencias...
pip install -r requirements.txt >nul 2>&1

echo 🌐 Iniciando servidor Flask...
start /B python app.py

echo ⏳ Aguardando servidor Flask...
timeout /t 3 >nul

echo 🔗 Iniciando tunel Cloudflare...
start /B cloudflared.exe tunnel --url http://localhost:5001

echo ⏳ Aguardando tunel...
timeout /t 8 >nul

echo.
echo ====================================================
echo ✅ SISTEMA INICIADO COM SUCESSO!
echo ====================================================
echo.
echo 📱 URLs de acesso:
echo    🏠 Local: http://localhost:5001
echo    🌐 Publico: [Veja no terminal do cloudflared]
echo.
echo 📊 Paineis importantes:
echo    🔧 Admin: /admin
echo    📈 Resultados: /results/1, /results/2, /results/3
echo.
echo 📱 QR Codes gerados em: qrcodes/
echo.
echo 🛑 Para parar: pressione Ctrl+C ou feche esta janela
echo.
pause
