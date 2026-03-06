import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import os
import random # NOVO: Para o Python embaralhar as listas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'segredo_super_seguro_do_seu_jogo'
socketio = SocketIO(app, cors_allowed_origins="*")

# ==========================================
# GERAÇÃO DO BARALHO INICIAL
# ==========================================
# Lemos as pastas e embaralhamos as cartas APENAS UMA VEZ quando o servidor inicia.
# Assim, todos os jogadores que entrarem receberão o mesmo baralho embaralhado.
cartas_globais = []

def preparar_baralhos():
    global cartas_globais
    portas = []
    tesouros = []
    
    pasta_porta = os.path.join(app.static_folder, 'cartas_porta')
    if os.path.exists(pasta_porta):
        for nome_arquivo in os.listdir(pasta_porta):
            if nome_arquivo.endswith(('.png', '.jpg', '.jpeg')):
                portas.append({
                    'id': f'porta_{nome_arquivo}',
                    'tipo': 'porta',
                    'frente': f'/static/cartas_porta/{nome_arquivo}',
                    'verso': '/static/verso_cartas/verso_porta.png'
                })

    pasta_tesouro = os.path.join(app.static_folder, 'cartas_tesouro')
    if os.path.exists(pasta_tesouro):
        for nome_arquivo in os.listdir(pasta_tesouro):
            if nome_arquivo.endswith(('.png', '.jpg', '.jpeg')):
                tesouros.append({
                    'id': f'tesouro_{nome_arquivo}',
                    'tipo': 'tesouro',
                    'frente': f'/static/cartas_tesouro/{nome_arquivo}',
                    'verso': '/static/verso_cartas/verso_tesouro.png'
                })

    # Embaralha os dois montes de forma independente
    random.shuffle(portas)
    random.shuffle(tesouros)
    
    # Junta os dois na lista global que será enviada aos jogadores
    cartas_globais.extend(portas)
    cartas_globais.extend(tesouros)

# Executa a função antes do servidor começar a aceitar conexões
preparar_baralhos()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cartas')
def listar_cartas():
    # Agora a API apenas entrega a lista que já foi embaralhada pelo servidor
    return jsonify(cartas_globais)

# ==========================================
# EVENTOS DE MULTIPLAYER (WEBSOCKETS)
# ==========================================

@socketio.on('movimento_carta')
def handle_movimento_carta(dados):
    emit('atualizar_posicao', dados, broadcast=True, include_self=False)

@socketio.on('virar_carta_frente_verso')
def handle_virar_carta(dados):
    emit('atualizar_frente_verso', dados, broadcast=True, include_self=False)

@socketio.on('rotacionar_carta')
def handle_rotacionar_carta(dados):
    emit('atualizar_rotacao', dados, broadcast=True, include_self=False)

# --- NOVO: Recebe a nova ordem da pilha e avisa os outros ---
@socketio.on('embaralhar_pilha')
def handle_embaralhar_pilha(dados):
    # dados vai conter uma lista de IDs: {'ids': ['porta_05.png', 'porta_12.png', ...]}
    emit('atualizar_ordem_pilha', dados, broadcast=True, include_self=False)
    
# --- NOVO: Ouve quando uma carta entra na mão de um jogador ---
@socketio.on('carta_para_mao')
def handle_carta_para_mao(dados):
    # dados: {'id': 'porta_01.png'}
    emit('esconder_carta', dados, broadcast=True, include_self=False)

if __name__ == '__main__':
    print("Servidor Multiplayer Iniciado com Baralhos Embaralhados!")
    socketio.run(app, debug=True, port=5000)