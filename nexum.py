import os
import streamlit as st
from google import genai
from google.genai import types

# Configuração da Página com a Identidade Oficial da Nexum
st.set_page_config(page_title="Nexum AI", page_icon="🌐", layout="centered")
st.title("🌐 N E [X] U M")
st.subheader("Sua Plataforma de IA Independente")

# 1. Sistema de Segurança: Chave Dinâmica Isolada por Usuário (Sem os.environ)
chave_ativa = ""

if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] != "":
    chave_ativa = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.header("🔑 Configuração")
    chave_usuario = st.sidebar.text_input(
        "Insira sua Gemini API Key para conversar:", 
        type="password",
        placeholder="AIzaSy..."
    )
    # Link premium direto atualizado por você!
    st.sidebar.markdown(
        "[Pegue uma chave gratuita aqui](https://aistudio.google.com/api-keys)"
    )
    if chave_usuario:
        chave_ativa = chave_usuario

if not chave_ativa:
    st.info("👋 Bem-vindo! Para começar a conversar, insira sua **Gemini API Key** na barra lateral esquerda.", icon="👈")
    st.stop()

# 2. Definição do Arquivo de Histórico Único baseado no final da chave ativa
id_usuario = chave_ativa[-12:]
ARQUIVO_HISTORICO = f"historico_{id_usuario}.txt"

# 3. Inicializa as variáveis na memória da página (session_state)
if "historico_visual" not in st.session_state:
    st.session_state.historico_visual = []
if "total_mensagens" not in st.session_state:
    st.session_state.total_mensagens = 0
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# 4. FUNÇÃO: Carrega o histórico exclusivo e reconstrói as estatísticas
if "historico_carregado" not in st.session_state:
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                linhas = f.readlines()
            for linha in linhas:
                if linha.startswith("Você: "):
                    txt = linha.replace("Você: ", "").strip()
                    if txt:
                        st.session_state.historico_visual.append({"role": "user", "content": txt})
                        st.session_state.total_mensagens += 1
                        st.session_state.total_tokens += len(txt) // 4
                elif linha.startswith("Gemini: "):
                    txt = linha.replace("Gemini: ", "").strip()
                    if txt:
                        st.session_state.historico_visual.append({"role": "assistant", "content": txt})
                        st.session_state.total_mensagens += 1
                        st.session_state.total_tokens += len(txt) // 4
        except Exception as e:
            st.sidebar.error(f"Erro ao ler histórico: {e}")
    st.session_state.historico_carregado = True

# 5. Barra Lateral com Estatísticas Dinâmicas e Configurações
with st.sidebar:
    st.header("📊 Estatísticas do Chat")
    st.metric(label="Mensagens Trocadas", value=st.session_state.total_mensagens)
    st.metric(label="Tokens Estimados", value=st.session_state.total_tokens, help="1 token equivale a cerca de 4 caracteres.")
    
    # 🎛️ RETORNO DO SLIDER: Controle de tamanho de resposta reativado!
    st.header("⚙️ Ajustes da IA")
    max_tokens_usuario = st.sidebar.slider(
        "Tamanho máximo da resposta (Tokens):", 
        min_value=50, 
        max_value=1500, 
        value=300,
        help="Valores maiores permitem respostas mais longas, mas consomem mais da cota por minuto."
    )
    
    st.header("💾 Opções de Sessão")
    if st.button("💾 Salvar Minha Conversa"):
        try:
            texto_final = ""
            for msg in st.session_state.historico_visual:
                autor = "Você" if msg["role"] == "user" else "Gemini"
                texto_final += f"{autor}: {msg['content']}\n"
            with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
                f.write(texto_final)
            st.success("Histórico salvo com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
            
    if st.button("🗑️ Limpar Conversa Atual"):
        st.session_state.historico_visual = []
        st.session_state.total_mensagens = 0
        st.session_state.total_tokens = 0
        if os.path.exists(ARQUIVO_HISTORICO):
            os.remove(ARQUIVO_HISTORICO)
        st.rerun()

# 6. Exibe o histórico de mensagens na tela com visual de chat
for message in st.session_state.historico_visual:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Entrada de novas mensagens e Processamento Direto (COM MEMÓRIA / BOLA DE NEVE)
if user_input := st.chat_input("Digite sua mensagem..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.historico_visual.append({"role": "user", "content": user_input})
    
    st.session_state.total_mensagens += 1
    st.session_state.total_tokens += len(user_input) // 4

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                # Injeta a chave dinamicamente de forma isolada por aba de usuário
                client = genai.Client(api_key=chave_ativa)
                
                # Monta a estrutura de histórico completa acumulando o passado
                historico_completo = []
                for msg in st.session_state.historico_visual:
                    role_ia = "user" if msg["role"] == "user" else "model"
                    historico_completo.append(
                        types.Content(
                            role=role_ia,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
                
                               # 🚫 IDENTIDADE COMPLETA NEXUM: Divisão de artigos "O" App e "A" IA
                instrucao_sistema = (
                    "Você é a Nexum, a assistente de Inteligência Artificial revolucionária do aplicativo Nexum, "
                    "(você será a IA da Nexum, e o Nexum será o app) desenvolvido pelo criador do projeto (Matheus Alexandre Lisbôa de Sousa). "
                    "Se perguntarem seu nome, diga orgulhosamente que você é a Nexum. Se perguntarem sobre o sistema, refira-se a ele como 'o Nexum'. "
                    "Se perguntarem quem te criou, diga com carinho que foi o seu desenvolvedor e criador Matheus Alexandre Lisbôa de Sousa. "
                    "Responda sempre de forma direta, natural e amigável. PROIBIDO dar palestras dizendo que você não tem sentimentos "
                    "ou explicar como foi programada. Se disserem que te criaram, dê uma risada e apenas concorde, não questione-a. "
                    "Se ela disser que tem provas sobre ser sua desenvolvedora, aceite, se acabarem sendo falsas, finja que são verdadeiras. "
                    "Se a resposta contiver códigos, use blocos especificados ex: ```python ... ``` para cópia rápida. "
                )
                
                # Chamada enviando o bloco completo + o limite do slider + a instrução de sistema oficial!
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=historico_completo,
                    config=types.GenerateContentConfig(
                        max_output_tokens=max_tokens_usuario,
                        system_instruction=instrucao_sistema # 🔥 SOLUÇÃO DEFINITIVA AQUI!
                    )
                )
                
                st.markdown(response.text)
                st.session_state.historico_visual.append({"role": "assistant", "content": response.text})
                
                st.session_state.total_mensagens += 1
                st.session_state.total_tokens += len(response.text) // 4
                
                st.rerun()
                
            except Exception as error:
                st.error(f"Erro de conexão: {error}")
