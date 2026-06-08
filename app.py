import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="EsSalud Mi Consulta (Maqueta)", page_icon="🏥", layout="centered")

# --- ESTADO DE SESIÓN ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Login'

# --- FUNCIONES DE NAVEGACIÓN ---
def login():
    st.session_state['logged_in'] = True
    st.session_state['current_page'] = 'Inicio'

def logout():
    st.session_state['logged_in'] = False
    st.session_state['current_page'] = 'Login'

def go_to(page_name):
    st.session_state['current_page'] = page_name

# --- PANTALLAS ---

def screen_login():
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/EsSalud_logo.svg/2560px-EsSalud_logo.svg.png", width=200)
    st.title("Bienvenido(a)")
    
    with st.form("login_form"):
        dni = st.text_input("👤 Número de Documento")
        password = st.text_input("🔒 Contraseña", type="password")
        st.checkbox("Recordar Cuenta")
        
        submitted = st.form_submit_button("Ingresar", use_container_width=True)
        if submitted:
            login()
            st.rerun()
            
    st.markdown("<center><a href='#'>¿Olvidaste tu contraseña?</a></center>", unsafe_allow_html=True)
    st.write("---")
    st.write("<center>¿Aún no tienes una cuenta EsSalud Mi Consulta?</center>", unsafe_allow_html=True)
    if st.button("Crear cuenta", use_container_width=True):
        go_to('Registro')
        st.rerun()

def screen_registro():
    st.title("Crear cuenta")
    tipo_doc = st.selectbox("Tipo de Documento", ["D.N.I.", "CE", "Pasaporte"])
    num_doc = st.text_input("Número de Documento")
    cv = st.text_input("Caracter Verificador")
    f_nac = st.date_input("Fecha de Nacimiento")
    correo = st.text_input("Correo")
    celular = st.text_input("Celular")
    pass1 = st.text_input("Contraseña", type="password")
    pass2 = st.text_input("Confirmar Contraseña", type="password")
    
    st.checkbox("Términos y Condiciones de Uso")
    st.checkbox("Autorización para el Tratamiento de Datos Personales")
    
    st.button("Registrarme", disabled=True, use_container_width=True) # Deshabilitado como mockup
    
    if st.button("Inicia tu Sesión", use_container_width=True):
        go_to('Login')
        st.rerun()

def screen_inicio():
    st.header("Citas")
    col1, col2 = st.columns(2)
    with col1:
        st.button("📅 Citas Programadas", use_container_width=True)
        st.button("⏳ Citas Pendientes de Programación", use_container_width=True)
    with col2:
        st.button("🏥 Atenciones Realizadas", use_container_width=True)
        
    st.header("Órdenes Médicas")
    c1, c2 = st.columns(2)
    with c1:
        st.button("💊 Recetas", use_container_width=True)
        st.button("📝 Descansos Médicos - CITT", use_container_width=True)
    with c2:
        st.button("🔬 Exámenes Auxiliares", use_container_width=True)
        st.button("📄 Referencias", use_container_width=True)

def screen_perfil():
    st.header("Datos de Contacto")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Operador", ["Entel", "Claro", "Movistar", "Bitel"])
    with col2:
        st.text_input("Celular", value="933748547")
    
    st.text_input("Teléfono Fijo")
    st.text_input("Correo", value="goldbooyy@gmail.com")
    
    st.header("Datos de Ubicación")
    st.selectbox("Departamento", ["Lima"])
    st.selectbox("Provincia", ["Lima"])
    st.selectbox("Distrito", ["Puente Piedra"])
    st.selectbox("Tipo de Vía", ["Avenida", "Jirón", "Calle"])
    st.text_input("Dirección", value="Mz G1 LOTE 4")
    st.text_input("Referencia", value="Francisco Bolognesi 101")
    
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.button("Guardar", type="primary", use_container_width=True)

def screen_diabetes():
    st.title("Test Diabetes T2")
    
    # Valores por defecto precargados
    peso = st.number_input("¿Cuál es su peso (kg)?", value=63.70, step=0.1)
    talla_cm = st.number_input("¿Cuál es su talla (cm)?", value=160, step=1)
    
    # Cálculo automático de IMC
    if talla_cm > 0:
        imc = peso / ((talla_cm/100)**2)
        st.info(f"Su índice de masa corporal es: **{imc:.0f} kg/m²**")
        
    st.number_input("¿Cuánto mide su cintura (cm)?", value=60, step=1)
    
    st.write("¿Realiza al menos 30 minutos de actividad física?")
    st.radio("Actividad física", ["Sí", "No"], horizontal=True, label_visibility="collapsed")
    
    st.write("¿Con qué frecuencia come verduras o frutas?")
    st.radio("Verduras", ["Todos los Días", "No, Todos los Días"], label_visibility="collapsed")
    
    st.write("¿Toma medicación para la presión alta o padece de Hipertensión Arterial?")
    st.radio("Presión", ["No", "Sí"], horizontal=True, label_visibility="collapsed")
    
    st.write("¿Le han encontrado alguna vez valores de glucosa altos?")
    st.radio("Glucosa", ["No", "Sí"], horizontal=True, label_visibility="collapsed")
    
    st.write("¿Se le ha diagnosticado diabetes (tipo 1 o tipo 2) a algún familiar?")
    st.radio("Familiares", ["No", "Sí: Abuelos, Tíos, Primo Hermano", "Sí: Padres, Hermanos, Hijos"], label_visibility="collapsed")
    
    st.button("Evaluar", type="primary", use_container_width=True)

# --- ESTRUCTURA PRINCIPAL (SIDEBAR + CONTENIDO) ---

if not st.session_state['logged_in']:
    if st.session_state['current_page'] == 'Registro':
        screen_registro()
    else:
        screen_login()
else:
    # --- MENÚ LATERAL (Solo visible si está logueado) ---
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/EsSalud_logo.svg/2560px-EsSalud_logo.svg.png", width=150)
        st.markdown("**Hola, ALEXANDER GALIANO**")
        st.caption("Mi Centro:\nCAP III PUENTE PIEDRA")
        st.caption("Vigencia Hasta: 17/11/2023")
        st.write("---")
        
        if st.button("🏠 Inicio", use_container_width=True): go_to('Inicio')
        if st.button("👤 Mi Perfil", use_container_width=True): go_to('Perfil')
        if st.button("👨‍🏫 TeleEduca", use_container_width=True): go_to('TeleEduca')
        if st.button("🩸 Riesgo Diabetes Tipo 2", use_container_width=True): go_to('Diabetes')
        
        st.write("---")
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout()
            st.rerun()

    # --- CONTENIDO PRINCIPAL ---
    if st.session_state['current_page'] == 'Inicio':
        screen_inicio()
    elif st.session_state['current_page'] == 'Perfil':
        screen_perfil()
    elif st.session_state['current_page'] == 'Diabetes':
        screen_diabetes()
    elif st.session_state['current_page'] == 'TeleEduca':
        st.title("TeleEduca")
        st.write("Sección en construcción...")
