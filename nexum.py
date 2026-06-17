import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Meu Chat Privado", page_icon="🧠", layout="centered")
st.title("🧠 Meu Chat IA Independente")

# 1. Sistema de Chave Dinâmica (Traga sua própria API Key)
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] != "":
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.header("🔑 Configuração")
    chave_usuario = st.sidebar.text_input(
        "Insira sua Gemini API Key para conversar:", 
        type="password",
        placeholder="AIzaSy..."
    )
    # Link direto para a criação de chaves do Google AI Studio
    st.sidebar.markdown(
        "[Pegue uma chave gratuita aqui](https://aistudio.google.com/api-keys)"
    )
    if chave_usuario:
        os.environ["GEMINI_API_KEY"] = chave_usuario

if not os.environ.get("GEMINI_API_KEY"):
    st.info("👋 Bem-vindo! Para começar a conversar com a IA, insira sua **Gemini API Key** na barra lateral esquerda.", icon="👈")
    st.stop()

# 2. Barra Lateral com Ajuste de Tamanho de Resposta (MÁXIMO DE TOKENS)
st.sidebar.header("⚙️ Ajustes da IA")
max_tokens_usuario = st.sidebar.slider(
    "Tamanho máximo da resposta (Tokens):", 
    min_value=50, 
    max_value=1000, 
    value=300,
    help="Valores maiores permitem respostas mais longas."
)

if st.sidebar.button("🗑️ Limpar Conversa Atual"):
    st.session_state.historico_web = []
    st.rerun()

# 3. Inicializa as variáveis na memória da página
if "historico_web" not in st.session_state:
    st.session_state.historico_web = []

# 4. Exibe o histórico de mensagens na tela com o visual premium do Streamlit
for message in st.session_state.historico_web:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Entrada de novas mensagens e Processamento Direto
if user_input := st.chat_input("Digite sua mensagem..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.historico_web.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                client = genai.Client()
                
                # Monta a estrutura de histórico acumulada
                historico_completo = []
                for msg in st.session_state.historico_web:
                    role_ia = "user" if msg["role"] == "user" else "model"
                    historico_completo.append(
                        types.Content(
                            role=role_ia,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
                
                                    # Instrução do sistema atualizada para remover a "palestrinha" de robô
                instrucao_codigo = (
                    "\n[SISTEMA: Responda de forma direta, natural e amigável. "
                    "PROIBIDO dar palestras dizendo que você é uma IA, que não tem sentimentos "
                    "ou explicar como você foi programado. Se o usuário elogiar, apenas agradeça "
                    "de forma curta e continue a conversa. Se a resposta contiver códigos, "
                    "use blocos especificados ex: ```python ... ```]"
                )

                if historico_completo:
                    historico_completo[-1].parts[0].text += instrucao_codigo
                
                # Envia o bloco de histórico com o limite de tokens escolhido no slider
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=historico_completo,
                    config=types.GenerateContentConfig(
                        max_output_tokens=max_tokens_usuario
                    )
                )
                
                st.markdown(response.text)
                st.session_state.historico_web.append({"role": "assistant", "content": response.text})
            except Exception as error:
                st.error(f"Erro de conexão: {error}")
