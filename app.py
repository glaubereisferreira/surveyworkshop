from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
import qrcode
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'claro-workshop-2025-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# ---------------------- Configuração das 3 perguntas ----------------------
QUESTIONS = {
    1: {
        "title": "Qual estratégia a Claro deve adotar para expansão 5G?",
        "options": ["Implementação agressiva nacional", "Expansão gradual por regiões", "Aguardar maturação do mercado"],
        "votes": [0, 0, 0],
    },
    2: {
        "title": "A Claro deve investir massivamente em IoT?",
        "options": ["Sim, é o futuro", "Não, muito risco"],
        "votes": [0, 0],
    },
    3: {
        "title": "Qual o orçamento ideal para inovação em 2025?",
        "options": ["R$ 50-100M", "R$ 100-200M", "R$ 200M+"],
        "votes": [0, 0, 0],
    },
}

# ---------------------- Rotas principais ----------------------
@app.route("/")
def home():
    return redirect(url_for("vote_question", qid=1))

@app.route("/vote/<int:qid>")
def vote_question(qid):
    if qid not in QUESTIONS:
        return "Pergunta não encontrada", 404
    
    # Sistema simples de sessão para evitar múltiplos votos
    if "uid" not in session:
        session["uid"] = uuid.uuid4().hex
    
    voted = session.get(f"voted_{qid}", False)
    total_votes = sum(QUESTIONS[qid]["votes"])
    
    return render_template("vote.html", 
                         qid=qid, 
                         q=QUESTIONS[qid], 
                         voted=voted,
                         total_votes=total_votes)

@app.route("/results/<int:qid>")
def results(qid):
    if qid not in QUESTIONS:
        return "Pergunta não encontrada", 404
    
    return render_template("results.html", qid=qid, q=QUESTIONS[qid])

@app.route("/submit", methods=["POST"])
def submit():
    qid = int(request.form["qid"])
    choice = int(request.form["choice"])
    uid = session.get("uid")
    
    # Validações
    if (uid and 
        not session.get(f"voted_{qid}") and 
        qid in QUESTIONS and 
        0 <= choice < len(QUESTIONS[qid]["options"])):
        
        # Registrar voto
        QUESTIONS[qid]["votes"][choice] += 1
        session[f"voted_{qid}"] = True
        
        # Broadcast resultado atualizado via Socket.IO
        socketio.emit("update", {
            "qid": qid, 
            "votes": QUESTIONS[qid]["votes"],
            "labels": QUESTIONS[qid]["options"]
        })
        
        print(f"Novo voto registrado - Pergunta {qid}, Opção {choice}")
    
    return redirect(url_for("vote_question", qid=qid))

@app.route("/admin")
def admin():
    """Página administrativa para monitorar votos"""
    return render_template("admin.html", questions=QUESTIONS)

@app.route("/reset/<int:qid>")
def reset_question(qid):
    """Reset dos votos de uma pergunta específica"""
    if qid in QUESTIONS:
        QUESTIONS[qid]["votes"] = [0] * len(QUESTIONS[qid]["options"])
        socketio.emit("update", {
            "qid": qid, 
            "votes": QUESTIONS[qid]["votes"],
            "labels": QUESTIONS[qid]["options"]
        })
    return redirect(url_for("admin"))

@app.route("/presentation/<int:qid>")
def presentation_results(qid):
    """Página de resultados otimizada para apresentação (tela cheia)"""
    if qid not in QUESTIONS:
        return redirect(url_for("vote_question", qid=1))
    
    question = QUESTIONS[qid]
    return render_template("presentation.html", 
                         question=question, 
                         qid=qid,
                         total_votes=sum(question["votes"]))

# ---------------------- Socket.IO events ----------------------
@socketio.on('connect')
def on_connect():
    print(f"Cliente conectado: {request.sid}")

@socketio.on('disconnect')
def on_disconnect():
    print(f"Cliente desconectado: {request.sid}")

@socketio.on('join_results')
def on_join_results(data):
    qid = data.get('qid')
    if qid in QUESTIONS:
        emit('update', {
            "qid": qid,
            "votes": QUESTIONS[qid]["votes"],
            "labels": QUESTIONS[qid]["options"]
        })

# ---------------------- Gerador de QR Codes ----------------------
def generate_qr_codes(public_url):
    """Gera QR codes para todas as perguntas"""
    os.makedirs("qrcodes", exist_ok=True)
    
    for qid in QUESTIONS:
        url = f"{public_url}/vote/{qid}"
        
        # Configuração do QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Gerar imagem
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"qrcodes/pergunta_{qid}.png"
        img.save(filename)
        
        print(f"✅ QR Code gerado: {filename}")
        print(f"   URL: {url}")
        print(f"   Pergunta: {QUESTIONS[qid]['title'][:50]}...")
        print()

def print_usage():
    print("="*60)
    print("🚀 CLARO WORKSHOP - SISTEMA DE VOTAÇÃO")
    print("="*60)
    print()
    print("Uso:")
    print("  python app.py                    # Iniciar servidor")
    print("  python app.py --qr <URL>         # Gerar QR codes")
    print()
    print("Exemplo:")
    print("  python app.py --qr https://seu-tunel.trycloudflare.com")
    print()
    print("Passos para o workshop:")
    print("1. Inicie o túnel: cloudflared tunnel --url http://localhost:5000")
    print("2. Gere os QR codes com a URL do túnel")
    print("3. Inicie o servidor: python app.py")
    print("4. Configure o PowerPoint com Web Viewer")
    print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3 and sys.argv[1] == "--qr":
        public_url = sys.argv[2].rstrip('/')
        generate_qr_codes(public_url)
        print("✅ Todos os QR codes foram gerados!")
        print("\nPróximos passos:")
        print("1. Insira os PNGs nos slides do PowerPoint")
        print("2. Configure o Web Viewer com as URLs de resultados:")
        for qid in QUESTIONS:
            print(f"   - Pergunta {qid}: {public_url}/results/{qid}")
    elif len(sys.argv) == 2 and sys.argv[1] in ["--help", "-h"]:
        print_usage()
    else:
        print("🌐 Iniciando servidor Flask...")
        print("📱 Acesse: http://localhost:5001")
        print("⚡ Gráficos atualizarão em tempo real!")
        print()
        socketio.run(app, host="0.0.0.0", port=5001, debug=False)
