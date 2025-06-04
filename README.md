# 🎯 Survey Workshop - Sistema de Votação em Tempo Real

> Sistema de votação interativa para workshops presenciais com gráficos dinâmicos e QR Codes

![Status](https://img.shields.io/badge/status-stable-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Flask](https://img.shields.io/badge/flask-3.0+-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 📋 Sobre o Projeto

Sistema completo de votação anônima desenvolvido para workshops presenciais com executivos. Permite que participantes votem via QR Code usando seus celulares, com resultados exibidos em tempo real através de gráficos dinâmicos.

### ✨ Características Principais

- **🔒 Votação Anônima**: Sistema anti-fraude com UUID por sessão
- **📱 Interface Mobile**: Design responsivo otimizado para celulares
- **📊 Gráficos em Tempo Real**: Atualização automática via Socket.IO
- **🌐 Acesso Remoto**: Túnel Cloudflare para acesso externo
- **🖥️ Integração PowerPoint**: Arquivos prontos para incorporação
- **⚡ Zero Configuração**: Scripts automatizados para inicialização

## 🚀 Início Rápido

### 1. Instalação

```bash
# Clone o repositório
git clone https://github.com/glaubereisferreira/surveyworkshop.git
cd surveyworkshop

# Instale as dependências
pip install -r requirements.txt
```

### 2. Execução

```bash
# Inicie o sistema completo
start_workshop.bat
```

### 3. Acesso

- **Local**: http://localhost:5001
- **Público**: URL gerada pelo túnel Cloudflare
- **Admin**: `/admin`
- **Resultados**: `/results/1`, `/results/2`, `/results/3`

## 📱 Como Usar

### Durante o Workshop

1. **Execute** `start_workshop.bat`
2. **Anote** a URL do túnel que aparece no terminal
3. **Atualize QR codes** (se necessário): `fix_qr_codes.bat`
4. **Exiba QR codes** nos slides
5. **Monitore** resultados via painel admin

### URLs Importantes

- **Votação Q1**: `/vote/1` - IA no Atendimento
- **Votação Q2**: `/vote/2` - Estratégia 5G
- **Votação Q3**: `/vote/3` - Sustentabilidade ESG
- **Apresentação**: `/presentation/1`, `/presentation/2`, `/presentation/3`

## 🛠️ Estrutura do Projeto

```
surveyworkshop/
├── app.py                    # Servidor Flask principal
├── requirements.txt          # Dependências Python
├── start_workshop.bat        # Script de inicialização
├── fix_qr_codes.bat         # Corretor de QR codes
├── generate_qr.py           # Gerador de QR codes
├── test_auto.py             # Testes automatizados
├── templates/               # Templates HTML
│   ├── vote.html           # Página de votação
│   ├── results.html        # Página de resultados
│   ├── admin.html          # Painel administrativo
│   └── presentation.html   # Tela para apresentação
├── static/                  # CSS e JavaScript
├── qrcodes/                 # QR codes gerados
└── embed_pergunta_*.html    # Arquivos para PowerPoint
```

## ⚙️ Tecnologias Utilizadas

- **Backend**: Flask + Socket.IO
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Gráficos**: Chart.js
- **QR Codes**: qrcode[pil]
- **Túnel**: Cloudflare Tunnel
- **Anti-fraude**: UUID + Session Management

## 🔧 Configuração Avançada

### Personalizar Perguntas

Edite o arquivo `app.py`:

```python
# Configuração das perguntas
PERGUNTAS = {
    1: {
        'titulo': 'Sua Pergunta Aqui',
        'opcoes': {
            'opcao1': 'Primeira Opção',
            'opcao2': 'Segunda Opção',
            # ...
        }
    }
}
```

### Integração PowerPoint

1. Insira **Web Viewer** add-in no PowerPoint
2. Use os arquivos `embed_pergunta_*.html`
3. Configure para **tela cheia**

Veja detalhes em: [`INTEGRACAO_POWERPOINT.md`](INTEGRACAO_POWERPOINT.md)

## 🧪 Testes

```bash
# Teste completo do sistema
python test_auto.py

# Teste específico de votos
python test_votes.py
```

## 📊 Funcionalidades

### Sistema de Votação
- ✅ Limite de 1 voto por pessoa
- ✅ Votação anônima com UUID
- ✅ Validação de dados
- ✅ Reset de votos via admin

### Interface Web
- ✅ Design responsivo
- ✅ Tema corporativo (Claro)
- ✅ Gráficos interativos
- ✅ Atualização em tempo real

### Administração
- ✅ Painel de controle
- ✅ Estatísticas em tempo real
- ✅ Reset de votações
- ✅ Monitoramento de conexões

## 🚨 Solução de Problemas

### QR Code não funciona
```bash
# Execute o corretor
fix_qr_codes.bat
# Cole a nova URL do túnel
```

### Erro de porta ocupada
```bash
# Mate processos Python
taskkill /F /IM python.exe
```

### Túnel não conecta
- Verifique conexão com internet
- Reinicie o cloudflared
- Aguarde 60 segundos para estabelecer conexão

## 📈 Casos de Uso

- **Workshops Corporativos**: Engajamento de executivos
- **Eventos Presenciais**: Pesquisas em tempo real
- **Treinamentos**: Feedback interativo
- **Reuniões**: Tomada de decisões colaborativas

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Glauber Reis Ferreira**
- GitHub: [@glaubereisferreira](https://github.com/glaubereisferreira)
- LinkedIn: [Glauber Reis Ferreira](https://linkedin.com/in/glaubereisferreira)

## 🙏 Agradecimentos

- Flask e Socket.IO pela base tecnológica
- Chart.js pelos gráficos interativos
- Cloudflare pelo túnel gratuito
- Comunidade open source

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐