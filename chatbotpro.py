import streamlit as st
import groq

# ----- CONFIGURACIONES DISPONIBLES -----

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# ----- CONFIGURAR PÁGINA -----
st.set_page_config(page_title="RoboAlfred", page_icon="🤖", layout="wide")

# ----- SIDEBAR -----
with st.sidebar:
    st.title("⚙️ Configuración")
    modelo_seleccionado = st.selectbox("Modelo AI:", modelos)

    font_size = st.slider("Tamaño de fuente", 12, 24, 16)
    if st.button("🧹 Limpiar historial"):
        st.session_state.mensajes = []
        st.experimental_rerun()


# ----- FUNCIONES -----

def crear_cliente_groq():
    if "GROQ_API_KEY" not in st.secrets:
        st.error("❌ Falta GROQ_API_KEY en .streamlit/secrets.toml")
        st.stop()
    return groq.Groq(api_key=st.secrets["GROQ_API_KEY"])

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def agregar_mensaje(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

# ✅ ESTA ES LA FUNCIÓN QUE PROVOCABA EL ERROR, DEBE IR ANTES DE USARSE
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content

# ----- EJECUCIÓN PRINCIPAL -----
def ejecutar_chat():
    cliente = crear_cliente_groq()
    inicializar_estado_chat()
    obtener_mensajes_previos()

    mensaje_usuario = st.chat_input("Envia tu mensaje")
    if mensaje_usuario:
        agregar_mensaje("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        respuesta = obtener_respuesta_modelo(cliente, modelo_seleccionado, st.session_state.mensajes)
        agregar_mensaje("assistant", respuesta)
        mostrar_mensaje("assistant", respuesta)

# ----- INICIO DE LA APP -----
if __name__ == '__main__':
    ejecutar_chat()