import streamlit as st
import random
import string
# Importamos la librería para el botón de copiar
from streamlit_copy_to_clipboard import st_copy_to_clipboard

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador de Contraseñas", page_icon="🔐", layout="centered")

# --- ESTILO CSS (Opcional, para un look más limpio) ---
st.markdown("""
<style>
    h1 {
        text-align: center;
        color: #1E90FF; /* Azul Dodger */
    }
    .stButton > button {
        background-color: #1E90FF;
        color: white;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    /* Estilo para la caja de texto de la contraseña generada */
    #password_output input {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.2em;
        font-weight: bold;
        text-align: center;
        /* El color de fondo y texto se adaptará al tema */
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🔐 Generador de Contraseñas Seguras")

# --- OPCIONES DE CONFIGURACIÓN ---
st.subheader("Configura tu Contraseña:")

# Usamos columnas para organizar mejor las opciones
col1, col2 = st.columns(2)

with col1:
    longitud = st.slider("Longitud de la contraseña:", min_value=8, max_value=64, value=16)
    incluir_mayusculas = st.checkbox("Incluir Mayúsculas (A-Z)", value=True)
    incluir_numeros = st.checkbox("Incluir Números (0-9)", value=True)

with col2:
    incluir_minusculas = st.checkbox("Incluir Minúsculas (a-z)", value=True) # Generalmente siempre activado
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
        return "Error: Debes seleccionar al menos un tipo de caracter."

    # Asegurarse de que la contraseña contenga al menos un caracter de cada tipo seleccionado
    contrasena = []
    tipos_incluidos = []

    if mayusculas:
        contrasena.append(random.choice(string.ascii_uppercase))
        tipos_incluidos.append(string.ascii_uppercase)
    if minusculas:
        contrasena.append(random.choice(string.ascii_lowercase))
        tipos_incluidos.append(string.ascii_lowercase)
    if numeros:
        contrasena.append(random.choice(string.digits))
        tipos_incluidos.append(string.digits)
    if simbolos:
        contrasena.append(random.choice(string.punctuation))
        tipos_incluidos.append(string.punctuation)

    # Rellenar el resto de la contraseña
    longitud_restante = longitud - len(contrasena)
    for _ in range(longitud_restante):
        contrasena.append(random.choice(caracteres))

    # Mezclar la contraseña para que no empiecen siempre igual
    random.shuffle(contrasena)

    return "".join(contrasena)

# --- BOTÓN Y RESULTADO ---
st.markdown("---")

if st.button("🔑 Generar Contraseña", use_container_width=True):
    if not (incluir_mayusculas or incluir_minusculas or incluir_numeros or incluir_simbolos):
        st.warning("⚠️ ¡Debes seleccionar al menos un tipo de caracteres!")
    else:
        contrasena_generada = generar_contrasena(
            longitud,
            incluir_mayusculas,
            incluir_minusculas,
            incluir_numeros,
            incluir_simbolos
        )
        # Guardar en el estado de sesión para el botón de copiar
        st.session_state.contrasena = contrasena_generada

# Mostrar la contraseña generada (si existe) en un text_input de solo lectura
if 'contrasena' in st.session_state and st.session_state.contrasena:
    st.subheader("Tu Contraseña Generada:")
    # Usamos text_input deshabilitado para que el estilo se adapte al tema
    st.text_input(
        label="Contraseña:",
        value=st.session_state.contrasena,
        key="password_output",
        disabled=True, # Lo hacemos no editable
        label_visibility="collapsed" # Ocultamos la etiqueta "Contraseña:"
    )
    # Añadimos el botón de copiar funcional
    st_copy_to_clipboard(st.session_state.contrasena, key="copy_button")
    st.caption("Usa el botón de arriba para copiar la contraseña.")

