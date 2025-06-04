// main.js - Sistema de gráficos em tempo real para Claro Workshop

let chart = null;
let socket = null;

function initChart(questionData) {
    const ctx = document.getElementById('votingChart');
    if (!ctx) {
        console.error('Canvas não encontrado!');
        return;
    }

    // Configuração do gráfico
    const config = {
        type: 'bar',
        data: {
            labels: questionData.labels,
            datasets: [{
                label: 'Votos',
                data: questionData.votes,
                backgroundColor: [
                    '#FF6B6B',  // Vermelho
                    '#4ECDC4',  // Turquesa
                    '#45B7D1',  // Azul
                    '#96CEB4',  // Verde
                    '#FECA57',  // Amarelo
                ],
                borderColor: [
                    '#FF5252',
                    '#26A69A',
                    '#2196F3',
                    '#66BB6A',
                    '#FFC107',
                ],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 750,
                easing: 'easeInOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: '#4ECDC4',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((context.parsed.y / total) * 100).toFixed(1) : 0;
                            return `${context.parsed.y} votos (${percentage}%)`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#666',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        color: '#666',
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                }
            }
        }
    };

    // Criar gráfico
    chart = new Chart(ctx, config);
    console.log(`📊 Gráfico inicializado para pergunta ${questionData.qid}`);

    // Atualizar resumo
    updateResultsSummary(questionData.votes, questionData.labels);

    // Inicializar Socket.IO
    initSocket(questionData.qid);
}

function initSocket(qid) {
    // Conectar ao Socket.IO
    socket = io({
        transports: ['websocket', 'polling']
    });

    socket.on('connect', function() {
        console.log('🔌 Conectado ao servidor');
        // Solicitar dados atualizados
        socket.emit('join_results', { qid: qid });
    });

    socket.on('disconnect', function() {
        console.log('❌ Desconectado do servidor');
    });

    socket.on('update', function(data) {
        console.log('📡 Recebendo atualização:', data);
        
        if (data.qid === qid) {
            updateChart(data.votes, data.labels);
            showUpdateAnimation();
        }
    });

    socket.on('connect_error', function(error) {
        console.error('🚫 Erro de conexão:', error);
    });
}

function updateChart(newVotes, labels) {
    if (!chart) {
        console.error('Gráfico não inicializado!');
        return;
    }

    // Atualizar dados do gráfico
    chart.data.datasets[0].data = newVotes;
    if (labels) {
        chart.data.labels = labels;
    }

    // Animar atualização
    chart.update('active');

    // Atualizar resumo
    updateResultsSummary(newVotes, labels || chart.data.labels);

    console.log('📈 Gráfico atualizado:', newVotes);
}

function updateResultsSummary(votes, labels) {
    const summaryElement = document.getElementById('resultsSummary');
    if (!summaryElement) return;

    const total = votes.reduce((a, b) => a + b, 0);
    
    let html = '<h3>📊 Resumo dos Votos</h3>';
    
    if (total === 0) {
        html += '<p class="no-votes">Aguardando votos...</p>';
    } else {
        html += '<div class="summary-grid">';
        
        votes.forEach((count, index) => {
            const percentage = ((count / total) * 100).toFixed(1);
            const isWinning = count === Math.max(...votes) && count > 0;
            
            html += `
                <div class="summary-item ${isWinning ? 'winning' : ''}">
                    <div class="summary-label">${labels[index]}</div>
                    <div class="summary-votes">${count} votos</div>
                    <div class="summary-percentage">${percentage}%</div>
                </div>
            `;
        });
        
        html += '</div>';
        html += `<div class="total-count">Total: ${total} votos</div>`;
    }
    
    summaryElement.innerHTML = html;
}

function showUpdateAnimation() {
    // Efeito visual de atualização
    const indicator = document.querySelector('.live-indicator');
    if (indicator) {
        indicator.classList.add('updating');
        setTimeout(() => {
            indicator.classList.remove('updating');
        }, 1000);
    }
}

// Utility functions
function formatNumber(num) {
    return new Intl.NumberFormat('pt-BR').format(num);
}

// Inicialização quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 Claro Workshop - Sistema carregado');
    
    // Auto-refresh da página a cada 5 minutos para evitar desconexões
    setTimeout(() => {
        if (socket && !socket.connected) {
            console.log('🔄 Reconectando...');
            location.reload();
        }
    }, 300000); // 5 minutos
});
