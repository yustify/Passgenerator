import streamlit as st
import random
import string
import pyperclip # Librería para el botón de copiar

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador de Contraseñas", page_icon="🔐", layout="centered")

# --- ESTILO CSS (Opcional, similar al del generador QR) ---
st.markdown("""
<style>
    h1 {
        text-align: center;
        color: #007bff; /* Azul */
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        padding: 0.5em 1em;
        border: none;
        width: 100%; /* Botón ancho */
    }
    .stSlider > div > div > div[data-testid="stTickBar"] > div {
        background: #007bff; /* Color del slider */
    }
    .stCheckbox > label {
        font-weight: 600;
    }
    /* Estilo para la caja de texto de la contraseña generada */
    #password_output_box {
        background-color: #f0f2f6;
        border: 2px solid #007bff;
        border-radius: 5px;
        padding: 1em;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.3em;
        font-weight: bold;
        word-wrap: break-word; /* Para que la contraseña larga se ajuste */
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCIÓN PARA GENERAR CONTRASEÑA ---
def generar_contraseña(longitud, incluir_mayusculas, incluir_numeros, incluir_simbolos):
    caracteres = string.ascii_lowercase
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    if not caracteres: # Si no se selecciona ningún tipo, usar minúsculas por defecto
        caracteres = string.ascii_lowercase

    contraseña = ''.join(random.choice(caracteres) for i in range(longitud))
    return contraseña

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("🔐 Generador de Contraseñas Seguras")
st.write("Configura las opciones y genera una contraseña fuerte.")

# --- OPCIONES DE CONFIGURACIÓN ---
st.subheader("Opciones de la Contraseña:")

longitud = st.slider("Longitud de la contraseña:", min_value=8, max_value=64, value=16)

col1, col2 = st.columns(2)
with col1:
    incluir_mayusculas = st.checkbox("Incluir Mayúsculas (ABC)", value=True)
    incluir_numeros = st.checkbox("Incluir Números (123)", value=True)
with col2:
    incluir_simbolos = st.checkbox("Incluir Símbolos (#@!)", value=True)

st.markdown("---") # Separador

# --- BOTÓN PARA GENERAR Y MOSTRAR RESULTADO ---
if st.button("🔑 Generar Contraseña"):
    password = generar_contraseña(longitud, incluir_mayusculas, incluir_numeros, incluir_simbolos)

    # Mostrar la contraseña generada en una caja con estilo
    st.markdown(f'<div id="password_output_box">{password}</div>', unsafe_allow_html=True)

    # Botón para copiar (usando pyperclip, más fiable que soluciones JS)
    if st.button("📋 Copiar al Portapapeles"):
        try:
            pyperclip.copy(password)
            st.success("¡Contraseña copiada!")
        except Exception as e:
            # En Streamlit Cloud, pyperclip puede no funcionar. Ofrecer selección manual.
            st.warning("No se pudo copiar automáticamente. Por favor, selecciona y copia la contraseña manualmente.")
            st.code(password) # Muestra de nuevo en st.code por si falla la copia

    # Guardar en estado de sesión para persistencia (opcional si ya usamos caja)
    st.session_state.last_password = password

# Puedes añadir una nota sobre la seguridad o cómo usar las contraseñas
st.caption("Recuerda usar contraseñas diferentes para cada servicio importante.")

