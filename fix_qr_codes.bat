@echo off
title Workshop Claro - Atualizador de QR Codes
color 0A

echo.
echo ========================================
echo    🎯 ATUALIZADOR DE QR CODES
echo ========================================
echo.

echo ⚠️  IMPORTANTE: Os QR codes precisam ser atualizados!
echo.
echo 🔍 Verifique o terminal do cloudflared e procure por uma linha como:
echo    "https://nova-url.trycloudflare.com"
echo.

set /p TUNNEL_URL="🌐 Cole a URL do túnel aqui: "

if "%TUNNEL_URL%"=="" (
    echo ❌ URL não fornecida!
    pause
    exit /b 1
)

echo.
echo ✅ URL recebida: %TUNNEL_URL%
echo 📝 Atualizando script de QR codes...

echo import qrcode > generate_qr_temp.py
echo import os >> generate_qr_temp.py
echo. >> generate_qr_temp.py
echo base_url = '%TUNNEL_URL%' >> generate_qr_temp.py
echo. >> generate_qr_temp.py
echo perguntas = [ >> generate_qr_temp.py
echo     {'id': 1, 'titulo': 'IA no Atendimento'}, >> generate_qr_temp.py
echo     {'id': 2, 'titulo': 'Estrategia 5G'}, >> generate_qr_temp.py
echo     {'id': 3, 'titulo': 'Sustentabilidade ESG'} >> generate_qr_temp.py
echo ] >> generate_qr_temp.py
echo. >> generate_qr_temp.py
echo print("🎯 GERADOR DE QR CODES - WORKSHOP CLARO") >> generate_qr_temp.py
echo print("=" * 50) >> generate_qr_temp.py
echo print(f"🌐 URL Base: {base_url}") >> generate_qr_temp.py
echo print() >> generate_qr_temp.py
echo. >> generate_qr_temp.py
echo os.makedirs('qrcodes', exist_ok=True) >> generate_qr_temp.py
echo. >> generate_qr_temp.py
echo for pergunta in perguntas: >> generate_qr_temp.py
echo     url = f"{base_url}/vote/{pergunta['id']}" >> generate_qr_temp.py
echo     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4) >> generate_qr_temp.py
echo     qr.add_data(url) >> generate_qr_temp.py
echo     qr.make(fit=True) >> generate_qr_temp.py
echo     img = qr.make_image(fill_color='black', back_color='white') >> generate_qr_temp.py
echo     filename = f"qrcodes/pergunta_{pergunta['id']}.png" >> generate_qr_temp.py
echo     img.save(filename) >> generate_qr_temp.py
echo     print(f"✅ QR Code {pergunta['id']} gerado: {filename}") >> generate_qr_temp.py
echo     print(f"   📋 {pergunta['titulo']}") >> generate_qr_temp.py
echo     print(f"   🔗 {url}") >> generate_qr_temp.py
echo     print() >> generate_qr_temp.py
echo. >> generate_qr_temp.py
echo print("=" * 50) >> generate_qr_temp.py
echo print("📱 Todos os QR codes foram atualizados!") >> generate_qr_temp.py

echo 🎨 Gerando novos QR codes...
python generate_qr_temp.py

echo.
echo 🎉 QR CODES ATUALIZADOS!
echo ========================================
echo.
echo 📱 Novos QR codes gerados:
echo    📁 qrcodes/pergunta_1.png
echo    📁 qrcodes/pergunta_2.png  
echo    📁 qrcodes/pergunta_3.png
echo.
echo 🧪 Teste agora:
echo    %TUNNEL_URL%/vote/1
echo.
echo 💡 Se os QR codes ainda não funcionarem,
echo    substitua-os no PowerPoint pelos novos!
echo.

del generate_qr_temp.py
pause
