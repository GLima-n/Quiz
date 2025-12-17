import streamlit as st
import pandas as pd
import time
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
        padding: 2rem 1rem;
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
    .white-card {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
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
        color: #C41E3A;
    }
    
    /* Pergunta */
    .question-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1.5rem;
        line-height: 1.4;
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

# Tela inicial
if not st.session_state.iniciado:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🎯 Confra EC 2026</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Quiz de Conhecimentos</p>', unsafe_allow_html=True)
    
    nome = st.text_input('Digite seu nome:', placeholder='Seu nome completo', key='input_nome')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button('🚀 Começar Quiz', key='btn_iniciar'):
        if nome.strip():
            st.session_state.nome = nome.strip()
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
        st.markdown(f'<p style="text-align: center; color: #666; margin-top: 1rem;">Pergunta {pergunta_idx + 1} de {len(perguntas)}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Pergunta
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{pergunta["pergunta"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Alternativas
        st.markdown('<div class="white-card">', unsafe_allow_html=True)
        
        if not st.session_state.respondeu:
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
                    st.session_state.respondeu = True
                    st.rerun()
            
            if st.button('➡️ Próxima Pergunta'):
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
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🏆 Quiz Finalizado!</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1.5rem; color: #666; margin-bottom: 2rem;">Parabéns, {st.session_state.nome}!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Resumo de pontuação
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    acertos = sum(1 for r in st.session_state.respostas if r['correta'])
    tempo_total = sum(r['tempo_gasto'] for r in st.session_state.respostas)
    
    with col1:
        st.metric('Pontuação Total', f'{st.session_state.pontuacao} pts')
    with col2:
        st.metric('Acertos', f'{acertos}/{len(perguntas)}')
    with col3:
        st.metric('Tempo Total', f'{int(tempo_total)}s')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detalhamento das respostas
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #C41E3A; margin-bottom: 1rem;">📊 Detalhamento</h3>', unsafe_allow_html=True)
    
    for i, resposta in enumerate(st.session_state.respostas, 1):
        if resposta['correta']:
            icone = '✅'
            cor = '#d4edda'
        else:
            icone = '❌'
            cor = '#f8d7da'
        
        st.markdown(f"""
        <div style="background-color: {cor}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
            <strong>{icone} Pergunta {i}:</strong> {resposta['pergunta']}<br>
            <strong>Sua resposta:</strong> {resposta['resposta'] if resposta['resposta'] else 'Não respondeu (tempo esgotado)'}<br>
            <strong>Tempo:</strong> {resposta['tempo_gasto']:.1f}s | <strong>Pontos:</strong> {resposta['pontos']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão para reiniciar
    if st.button('🔄 Fazer Quiz Novamente'):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
