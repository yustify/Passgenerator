import streamlit as st
import random
import string
# Ya no importamos streamlit_copy_to_clipboard

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador de Contraseñas", page_icon="🔐", layout="centered")

# --- ESTILO CSS (Mínimo y adaptable al tema) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
    }
    h1 {
        text-align: center;
        color: #1E90FF; /* Azul Dodger - Se ve bien en ambos temas */
    }
    .stButton > button {
        /* Estilo del botón principal */
        background-color: #1E90FF;
        color: white;
        border-radius: 5px;
        padding: 0.5em 1em;
        border: none; /* Quitamos borde por si acaso */
    }
    /* Estilo para el bloque de markdown que muestra la contraseña */
    div[data-testid="stMarkdownContainer"] pre {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.3em; /* Hacemos la contraseña un poco más grande */
        font-weight: bold;
        text-align: center;
        padding: 0.5em;
        border: 1px dashed #888; /* Un borde sutil */
        border-radius: 5px;
        /* El color de fondo y texto lo gestionará Streamlit según el tema */
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🔐 Generador de Contraseñas Seguras")

# --- OPCIONES DE CONFIGURACIÓN ---
st.subheader("Configura tu Contraseña:")

col1, col2 = st.columns(2)

with col1:
    longitud = st.slider("Longitud de la contraseña:", min_value=8, max_value=64, value=16)
    incluir_mayusculas = st.checkbox("Incluir Mayúsculas (A-Z)", value=True)
    incluir_numeros = st.checkbox("Incluir Números (0-9)", value=True)

with col2:
    incluir_minusculas = st.checkbox("Incluir Minúsculas (a-z)", value=True)
    incluir_simbolos = st.checkbox("Incluir Símbolos (!@#$%^&*)", value=True)

# --- LÓGICA PARA GENERAR LA CONTRASEÑA ---
def generar_contrasena(longitud, mayusculas, minusculas, numeros, simbolos):
    caracteres = ""
    if mayusculas:
        caracteres += string.ascii_uppercase
    if minusculas:
        caracteres += string.ascii_lowercase
    if numeros:
        caracteres += string.digits
    if simbolos:
        caracteres += string.punctuation

    if not caracteres:
        return None # Devolvemos None si no hay caracteres seleccionados

    contrasena = []
    if mayusculas:
        contrasena.append(random.choice(string.ascii_uppercase))
    if minusculas:
        contrasena.append(random.choice(string.ascii_lowercase))
    if numeros:
        contrasena.append(random.choice(string.digits))
    if simbolos:
        contrasena.append(random.choice(string.punctuation))

    longitud_restante = longitud - len(contrasena)
    if longitud_restante > 0:
        for _ in range(longitud_restante):
            contrasena.append(random.choice(caracteres))

    random.shuffle(contrasena)
    return "".join(contrasena[:longitud]) # Aseguramos la longitud exacta

# --- BOTÓN Y RESULTADO ---
st.markdown("---")

if st.button("🔑 Generar Contraseña", use_container_width=True):
    contrasena_generada = generar_contrasena(
        longitud,
        incluir_mayusculas,
        incluir_minusculas,
        incluir_numeros,
        incluir_simbolos
    )
    if contrasena_generada is None:
        st.warning("⚠️ ¡Debes seleccionar al menos un tipo de caracteres!")
        st.session_state.contrasena = "" # Limpiamos por si había una anterior
    else:
        st.session_state.contrasena = contrasena_generada

# Mostrar la contraseña generada (si existe) usando st.markdown
if 'contrasena' in st.session_state and st.session_state.contrasena:
    st.subheader("Tu Contraseña Generada:")
    # Usamos markdown con triple comilla invertida para formato de código adaptable al tema
    st.markdown(f"```\n{st.session_state.contrasena}\n```")
    st.caption("Selecciona y copia la contraseña manualmente.")
