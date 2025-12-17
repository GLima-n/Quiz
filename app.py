import streamlit as st
import pandas as pd
import time
import json
import os
from datetime import datetime 

# Configuração da página
st.set_page_config(
    page_title="Confra EC 2026 - Quiz",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado para design moderno
st.markdown("""
<style>
    /* Cores principais */
    :root {
        --primary-red: #C41E3A;
        --dark-red: #8B1538;
        --light-red: #FF6B85;
        --white: #FFFFFF;
        --dark-bg: #1a1a1a;
    }
    
    /* Fundo principal */
    .stApp {
        background: linear-gradient(135deg, #C41E3A 0%, #8B1538 100%);
    }
    
    /* Centralizar conteúdo */
    .main .block-container {
        max-width: 800px;
        padding: 1rem 1rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Remover padding do topo */
    .main {
        padding-top: 0rem;
    }
    
    /* Estilo dos botões */
    .stButton > button {
        width: 100%;
        background-color: white;
        color: #C41E3A;
        border: none;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background-color: #f8f9fa;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Input de texto */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid white;
        padding: 1rem;
        font-size: 1.1rem;
    }
    
    /* Cartão branco */
    /* Cartão Transparente (antigo white-card) */
    .white-card {
        background-color: transparent;
        padding: 0;
        border-radius: 0;
        box-shadow: none;
        margin-bottom: 1rem;
    }
    
    /* Título principal */
    .main-title {
        color: #C41E3A;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Timer */
    .timer-container {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .timer-text {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Pergunta */
    /* Pergunta */
    .question-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        line-height: 1.4;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Alternativas */
    .alternative-button {
        background-color: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .alternative-button:hover {
        border-color: #C41E3A;
        background-color: #fff;
    }
    
    /* Resultado */
    .result-correct {
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
        padding: 1rem;
        border-radius: 12px;
        font-weight: 600;
    }
    
    .result-incorrect {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
        padding: 1rem;
        border-radius: 12px;
        font-weight: 600;
    }
    
    /* Métricas */
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Barra de progresso */
    .stProgress > div > div > div {
        background-color: #C41E3A;
    }
    
    /* Esconder cabeçalho padrão */
    header {visibility: hidden;}
    
    /* Esconder footer */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Função para carregar perguntas
@st.cache_data
def carregar_perguntas():
    try:
        df = pd.read_excel('Confra_EC_2026_Modelo_Perguntas.xlsx')
        perguntas = []
        for _, row in df.iterrows():
            perguntas.append({
                'pergunta': row['Pergunta'],
                'alternativas': {
                    'A': row['Alternativa A'],
                    'B': row['Alternativa B'],
                    'C': row['Alternativa C'],
                    'D': row['Alternativa D']
                },
                'resposta_correta': row['Resposta Correta (A/B/C/D)'].strip().upper()
            })
        return perguntas
    except Exception as e:
        st.error(f"Erro ao carregar perguntas: {e}")
        return []

# Função para salvar resultados
# Função para salvar resultados
def salvar_resultado(nome, pontuacao, acertos, total_perguntas, tempo_total):
    arquivo = 'ranking.json'
    
    # Carregar ranking existente
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            ranking = json.load(f)
    else:
        ranking = []
    
    # Normalizar nome para comparação (ignorar maiúsculas/minúsculas e espaços)
    import re
    nome_norm = re.sub(r'\s+', ' ', nome.strip()).lower()
    
    # Não salvar se for o admin
    if nome_norm == 'alef gomes#':
        return
    
    # Verificar se usuário já existe e manter a melhor pontuação
    usuario_existente = False
    for i, item in enumerate(ranking):
        item_norm = re.sub(r'\s+', ' ', item['nome'].strip()).lower()
        if item_norm == nome_norm:
            usuario_existente = True
            # Se a nova pontuação for maior, atualiza
            if pontuacao > item['pontuacao']:
                ranking[i] = {
                    'nome': nome,
                    'pontuacao': pontuacao,
                    'acertos': acertos,
                    'total_perguntas': total_perguntas,
                    'tempo_total': tempo_total,
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }
            # Se pontuação for igual, usa o que teve menor tempo
            elif pontuacao == item['pontuacao'] and tempo_total < item['tempo_total']:
                ranking[i] = {
                    'nome': nome,
                    'pontuacao': pontuacao,
                    'acertos': acertos,
                    'total_perguntas': total_perguntas,
                    'tempo_total': tempo_total,
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }
            break
    
    # Se não existe, adiciona novo
    if not usuario_existente:
        ranking.append({
            'nome': nome,
            'pontuacao': pontuacao,
            'acertos': acertos,
            'total_perguntas': total_perguntas,
            'tempo_total': tempo_total,
            'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        })
    
    # Salvar ranking atualizado
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(ranking, f, indent=2, ensure_ascii=False)

# Função para carregar ranking
def carregar_ranking():
    arquivo = 'ranking.json'
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            ranking = json.load(f)
        # Ordenar por pontuação (decrescente)
        ranking.sort(key=lambda x: x['pontuacao'], reverse=True)
        return ranking
    return []

# Inicializar session_state
if 'nome' not in st.session_state:
    st.session_state.nome = ''
if 'iniciado' not in st.session_state:
    st.session_state.iniciado = False
if 'pergunta_atual' not in st.session_state:
    st.session_state.pergunta_atual = 0
if 'respostas' not in st.session_state:
    st.session_state.respostas = []
if 'pontuacao' not in st.session_state:
    st.session_state.pontuacao = 0
if 'tempo_inicio' not in st.session_state:
    st.session_state.tempo_inicio = None
if 'finalizado' not in st.session_state:
    st.session_state.finalizado = False
if 'respondeu' not in st.session_state:
    st.session_state.respondeu = False

# Carregar perguntas
perguntas = carregar_perguntas()

# Tela de ranking (admin)
if 'visualizar_ranking' in st.session_state and st.session_state.visualizar_ranking:
    ranking = carregar_ranking()
    
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🏆 Ranking - Confra EC 2026</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #e0e0e0; margin-bottom: 2rem;">Painel Administrativo</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if ranking:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #e0e0e0; margin-bottom: 1rem;"><strong>Total de participantes:</strong> {len(ranking)}</p>', unsafe_allow_html=True)
        
        # Tabela de ranking
        for i, participante in enumerate(ranking, 1):
            if i == 1:
                icone = '🥇'
                cor = '#ffd700'
                cor_texto = '#000000'
                cor_pontos = '#C41E3A'
            elif i == 2:
                icone = '🥈'
                cor = '#c0c0c0'
                cor_texto = '#000000'
                cor_pontos = '#C41E3A'
            elif i == 3:
                icone = '🥉'
                cor = '#cd7f32'
                cor_texto = '#000000'
                cor_pontos = '#C41E3A'
            else:
                icone = f'{i}º'
                cor = 'rgba(255, 255, 255, 0.1)'
                cor_texto = '#ffffff'
                cor_pontos = '#ffffff'
            
            st.markdown(f"""
            <div style="background-color: {cor}; padding: 1rem; border-radius: 12px; margin-bottom: 0.8rem; border: 1px solid rgba(255,255,255,0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="font-size: 1.2rem; color: {cor_texto};">{icone} {participante['nome']}</strong><br>
                        <span style="color: {cor_texto}; font-size: 0.9rem; opacity: 0.8;">
                            Acertos: {participante['acertos']}/{participante['total_perguntas']} | 
                            Tempo: {int(participante['tempo_total'])}s | 
                            Data: {participante['data']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <strong style="font-size: 1.5rem; color: {cor_pontos};">{participante['pontuacao']}</strong><br>
                        <span style="color: {cor_texto}; font-size: 0.9rem; opacity: 0.8;">pontos</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #999;">Nenhum participante ainda.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão para voltar
    if st.button('🔙 Voltar'):
        del st.session_state.visualizar_ranking
        st.rerun()

# Tela inicial
elif not st.session_state.iniciado:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🎯 Confra EC 2026</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #e0e0e0; margin-bottom: 2rem;">Quiz de Conhecimentos</p>', unsafe_allow_html=True)
    
    nome = st.text_input('Digite seu nome:', placeholder='Seu nome completo', key='input_nome')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button('🚀 Começar Quiz', key='btn_iniciar'):
        if nome.strip():
            # Normalizar espaços múltiplos para um único espaço
            import re
            nome_normalizado = re.sub(r'\s+', ' ', nome.strip()).lower()
            
            # Verificar se é o nome admin (case-insensitive)
            if nome_normalizado == 'alef gomes#':
                st.session_state.visualizar_ranking = True
                st.rerun()
            else:
                st.session_state.nome = re.sub(r'\s+', ' ', nome.strip())
                st.session_state.iniciado = True
                st.session_state.tempo_inicio = time.time()
                st.rerun()
        else:
            st.error('Por favor, digite seu nome!')

# Tela de perguntas
elif not st.session_state.finalizado:
    pergunta_idx = st.session_state.pergunta_atual
    
    if pergunta_idx < len(perguntas):
        pergunta = perguntas[pergunta_idx]
        
        # Calcular tempo decorrido
        if st.session_state.tempo_inicio:
            tempo_decorrido = time.time() - st.session_state.tempo_inicio
            tempo_restante = max(0, 30 - tempo_decorrido)
        else:
            tempo_restante = 30
        
        # Verificar se tempo acabou
        if tempo_restante == 0 and not st.session_state.respondeu:
            st.session_state.respostas.append({
                'pergunta': pergunta['pergunta'],
                'resposta': None,
                'correta': False,
                'tempo_gasto': 30,
                'pontos': 0
            })
            st.session_state.pergunta_atual += 1
            st.session_state.tempo_inicio = time.time()
            st.session_state.respondeu = False
            st.rerun()
        
        # Timer e progresso
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="timer-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="timer-text">⏱️ {int(tempo_restante)}s</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Barra de progresso do tempo
        progress = tempo_restante / 30
        st.progress(progress)
        
        # Número da pergunta
        st.markdown(f'<p style="text-align: center; color: #e0e0e0; margin-top: 1rem;">Pergunta {pergunta_idx + 1} de {len(perguntas)}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pergunta
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{pergunta["pergunta"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Alternativas
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        
        for letra, texto in pergunta['alternativas'].items():
            if st.button(f'{letra}) {texto}', key=f'alt_{letra}'):
                tempo_gasto = 30 - tempo_restante
                correta = (letra == pergunta['resposta_correta'])
                
                # Calcular pontos
                if correta:
                    pontos_base = 100
                    bonus_tempo = int((tempo_restante / 30) * 50)  # Até 50 pontos de bônus
                    pontos = pontos_base + bonus_tempo
                else:
                    pontos = 0
                
                st.session_state.pontuacao += pontos
                st.session_state.respostas.append({
                    'pergunta': pergunta['pergunta'],
                    'resposta': letra,
                    'correta': correta,
                    'tempo_gasto': tempo_gasto,
                    'pontos': pontos,
                    'resposta_correta': pergunta['resposta_correta']
                })
                
                # Avançar para próxima pergunta automaticamente
                st.session_state.pergunta_atual += 1
                st.session_state.tempo_inicio = time.time()
                st.session_state.respondeu = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Auto-refresh para atualizar timer
        if not st.session_state.respondeu and tempo_restante > 0:
            time.sleep(0.5)
            st.rerun()
    
    else:
        # Quiz finalizado
        st.session_state.finalizado = True
        st.rerun()

# Tela de resultados
else:
    # Salvar resultados
    acertos = sum(1 for r in st.session_state.respostas if r['correta'])
    tempo_total = sum(r['tempo_gasto'] for r in st.session_state.respostas)
    salvar_resultado(
        st.session_state.nome,
        st.session_state.pontuacao,
        acertos,
        len(perguntas),
        tempo_total
    )
    
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🎯 Quiz Finalizado!</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1.5rem; color: #666; margin-bottom: 2rem;">Obrigado pela sua participação, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #999;">Suas respostas foram registradas com sucesso.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
