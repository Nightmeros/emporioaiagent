
import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage
from agent import create_emporio_agent


def extrair_texto(conteudo):
    if isinstance(conteudo, str):
        return conteudo
    if isinstance(conteudo, list):
        textos = []
        for bloco in conteudo:
            if isinstance(bloco, dict):
                if bloco.get("type") == "text":
                    textos.append(bloco.get("text", ""))
            elif isinstance(bloco, str):
                textos.append(bloco)
        return "\n".join(textos)

    return str(conteudo)


st.set_page_config(
    page_title="Empório da Música - Atendimento IA",
    page_icon="🎸",
    layout="centered"
)

st.title("🎸 Empório da Música")
st.caption("Assistente Virtual Inteligente (Powered by Gemini & LangGraph)")


@st.cache_resource
def carregar_agente():
    return create_emporio_agent()


if "agente" not in st.session_state:
    with st.spinner("A ligar os amplificadores e a afinar os instrumentos..."):
        st.session_state.agente = carregar_agente()


if "historico" not in st.session_state:
    st.session_state.historico = [
        AIMessage(
            content="Olá! Sou o assistente da Empório da Música. Como posso ajudar com os seus instrumentos hoje?"
        )
    ]


if st.sidebar.button("Nova conversa"):
    st.session_state.historico = [
        AIMessage(
            content="Olá! Sou o assistente da Empório da Música. Como posso ajudar com os seus instrumentos hoje?"
        )
    ]
    st.rerun()


for msg in st.session_state.historico:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    avatar = "👤" if role == "user" else "🎵"

    with st.chat_message(role, avatar=avatar):
        st.markdown(extrair_texto(msg.content))


if pergunta := st.chat_input("Ex: Qual o preço do violão Takamine?"):

    mensagem_usuario = HumanMessage(content=pergunta)

    st.session_state.historico.append(mensagem_usuario)

    with st.chat_message("user", avatar="👤"):
        st.markdown(pergunta)

    with st.chat_message("assistant", avatar="🎵"):
        with st.spinner("A consultar o sistema..."):

            try:
                resultado = st.session_state.agente.invoke({
                    "messages": st.session_state.historico
                })

                resposta_bruta = resultado["messages"][-1].content
                resposta_texto = extrair_texto(resposta_bruta)

                st.markdown(resposta_texto)

                st.session_state.historico.append(
                    AIMessage(content=resposta_texto)
                )

            except Exception as erro:
                st.error(f"Ups! Tivemos um problema técnico: {erro}")
