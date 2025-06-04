#!/usr/bin/env python3
"""
Script para gerar QR codes com a URL atualizada do túnel
"""

import qrcode
import os

# Nova URL do túnel
base_url = 'https://parts-reporter-founder-joe.trycloudflare.com'

# Perguntas do workshop
perguntas = [
    {'id': 1, 'titulo': 'IA no Atendimento'},
    {'id': 2, 'titulo': 'Estratégia 5G'}, 
    {'id': 3, 'titulo': 'Sustentabilidade ESG'}
]

print("🎯 GERADOR DE QR CODES - WORKSHOP CLARO")
print("=" * 50)
print(f"🌐 URL Base: {base_url}")
print()

# Criar pasta se não existir
os.makedirs('qrcodes', exist_ok=True)

# Gerar QR codes
for pergunta in perguntas:
    url = f"{base_url}/vote/{pergunta['id']}"
    
    # Configurar QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Gerar imagem
    img = qr.make_image(fill_color='black', back_color='white')
    filename = f"qrcodes/pergunta_{pergunta['id']}.png"
    img.save(filename)
    
    print(f"✅ QR Code {pergunta['id']} gerado: {filename}")
    print(f"   📋 {pergunta['titulo']}")
    print(f"   🔗 {url}")
    print()

print("=" * 50)
print("📱 Todos os QR codes foram gerados com sucesso!")
print(f"🌐 URL pública: {base_url}")
print("\n📂 Arquivos gerados:")
print("   📁 qrcodes/pergunta_1.png")
print("   📁 qrcodes/pergunta_2.png") 
print("   📁 qrcodes/pergunta_3.png")
