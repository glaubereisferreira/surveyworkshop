#!/usr/bin/env python3
"""
Script automatizado para testar o fluxo completo
QR Code → Pergunta → Gráfico em tempo real
"""

import requests
import time
import random
import uuid

# URL base do sistema
BASE_URL = "https://parts-reporter-founder-joe.trycloudflare.com"

def send_vote(question_id, option):
    """Envia um voto único para uma pergunta"""
    try:
        session_id = str(uuid.uuid4())
        
        # Primeiro, acessar a página de votação para obter cookies/sessão
        vote_page_url = f"{BASE_URL}/vote/{question_id}"
        session = requests.Session()
        
        # Acessar página de votação
        response = session.get(vote_page_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Erro ao acessar página: {response.status_code}")
            return False
        
        # Preparar dados do voto
        vote_data = {
            'qid': question_id,
            'choice': get_option_index(question_id, option)
        }
        
        # Enviar voto via POST para /submit
        submit_url = f"{BASE_URL}/submit"
        headers = {
            'User-Agent': f'Workshop-Executive-{session_id[:8]}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': vote_page_url
        }
        
        response = session.post(submit_url, data=vote_data, headers=headers, timeout=10)
        
        if response.status_code in [200, 302]:
            print(f"✅ Voto enviado - Q{question_id}: {option}")
            return True
        else:
            print(f"❌ Erro - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def get_option_index(question_id, option_value):
    """Converte valor da opção para índice"""
    option_maps = {
        1: {
            'implementacao_agressiva': 0,
            'expansao_gradual': 1, 
            'aguardar_maturacao': 2
        },
        2: {
            'sim_futuro': 0,
            'nao_risco': 1
        },
        3: {
            'budget_50_100': 0,
            'budget_100_200': 1,
            'budget_200_plus': 2
        }
    }
    
    return option_maps.get(question_id, {}).get(option_value, 0)

def test_complete_flow():
    """Testa o fluxo completo do workshop"""
    print("🚀 TESTE AUTOMÁTICO - WORKSHOP CLARO")
    print("=" * 50)
    print(f"🌐 URL: {BASE_URL}")
    print()
    
    # Verificar se sistema está online
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✅ Sistema online - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Sistema offline: {e}")
        return
      # Definir cenários de teste para cada pergunta
    scenarios = {
        1: {
            'name': 'Estratégia 5G',
            'options': ['implementacao_agressiva', 'expansao_gradual', 'aguardar_maturacao'],
            'votes': [
                ('implementacao_agressiva', 4),
                ('expansao_gradual', 7),
                ('aguardar_maturacao', 2)
            ]
        },
        2: {
            'name': 'Investimento IoT', 
            'options': ['sim_futuro', 'nao_risco'],
            'votes': [
                ('sim_futuro', 8),
                ('nao_risco', 3)
            ]
        },
        3: {
            'name': 'Orçamento 2025',
            'options': ['budget_50_100', 'budget_100_200', 'budget_200_plus'],
            'votes': [
                ('budget_50_100', 2),
                ('budget_100_200', 6),
                ('budget_200_plus', 4)
            ]
        }
    }
    
    # Executar testes para cada pergunta
    for q_id, scenario in scenarios.items():
        print(f"\n🎯 Pergunta {q_id}: {scenario['name']}")
        print(f"📱 Votação: {BASE_URL}/vote/{q_id}")
        print(f"📊 Resultados: {BASE_URL}/results/{q_id}")
        print("-" * 30)
        
        total_votes = 0
        success_votes = 0
        
        # Enviar votos conforme cenário
        for option, count in scenario['votes']:
            for i in range(count):
                total_votes += 1
                if send_vote(q_id, option):
                    success_votes += 1
                time.sleep(0.3)  # Pausa entre votos
        
        print(f"📊 Resumo Q{q_id}: {success_votes}/{total_votes} votos enviados")
        print(f"🔗 Abra no navegador: {BASE_URL}/results/{q_id}")
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 TESTE COMPLETO FINALIZADO!")
    print("\n📋 URLs para verificar:")
    print(f"   🏠 Home: {BASE_URL}")
    print(f"   🔧 Admin: {BASE_URL}/admin")
    for q_id in [1, 2, 3]:
        print(f"   📊 Q{q_id}: {BASE_URL}/results/{q_id}")
    
    print("\n📱 QR Codes disponíveis:")
    print("   📁 qrcodes/pergunta_1.png")
    print("   📁 qrcodes/pergunta_2.png") 
    print("   📁 qrcodes/pergunta_3.png")

if __name__ == "__main__":
    test_complete_flow()
