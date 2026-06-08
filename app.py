import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="EsSalud Mi Consulta (Maqueta)", page_icon="🏥", layout="centered")

# --- BASE DE DATOS SIMULADA Y ESTADO DE SESIÓN ---
# Aquí guardamos los usuarios registrados temporalmente mientras la app esté corriendo
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {
        "12345678": {
            "password": "password123",
            "nombre": "JUAN PEREZ",
            "correo": "juan.perez@ejemplo.com",
            "celular": "987654321",
            "peso": 75.0,
            "talla": 170,
            "direccion": "Av. Las Flores 123",
            "centro": "CAP III MIRAFLORES"
        }
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Login'
if 'current_user_dni' not in st.session_state:
    st.session_state['current_user_dni'] = None

# --- FUNCIONES DE NAVEGACIÓN ---
def logout():
    st.session_state['logged_in'] = False
    st.session_state['current_user_dni'] = None
    st.session_state['current_page'] = 'Login'

def go_to(page_name):
    st.session_state['current_page'] = page_name

# --- PANTALLAS ---

def screen_login():
    # Nota para los testers que pediste
    st.info("💡 **NOTA PARA PRUEBAS:**\nPara ingresar, usa el DNI: **12345678** y Contraseña: **password123**. Si no, regístrate abajo para crear un nuevo usuario.")
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/EsSalud_logo.svg/2560px-EsSalud_logo.svg.png", width=200)
    st.title("Bienvenido(a)")
    
    with st.form("login_form"):
        dni = st.text_input("👤 Número de Documento (DNI)")
        password = st.text_input("🔒 Contraseña", type="password")
        st.checkbox("Recordar Cuenta")
        
        submitted = st.form_submit_button("Ingresar", use_container_width=True)
        if submitted:
            # Validación con la "Base de Datos"
            if dni in st.session_state['db_users'] and st.session_state['db_users'][dni]['password'] == password:
                st.session_state['logged_in'] = True
                st.session_state['current_user_dni'] = dni
                st.session_state['current_page'] = 'Inicio'
                st.rerun()
            else:
                st.error("❌ DNI o contraseña incorrectos. Intenta nuevamente o regístrate.")
            
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
    nombre_nuevo = st.text_input("Nombres y Apellidos")
    correo = st.text_input("Correo")
    celular = st.text_input("Celular")
    pass1 = st.text_input("Contraseña", type="password")
    pass2 = st.text_input("Confirmar Contraseña", type="password")
    
    st.checkbox("Términos y Condiciones de Uso")
    st.checkbox("Autorización para el Tratamiento de Datos Personales")
    
    # Lógica de registro
    if st.button("Registrarme", type="primary", use_container_width=True):
        if not num_doc or not pass1:
            st.warning("⚠️ El número de documento y la contraseña son obligatorios.")
        elif pass1 != pass2:
            st.error("❌ Las contraseñas no coinciden.")
        elif num_doc in st.session_state['db_users']:
            st.error("❌ Este documento ya está registrado.")
        else:
            # Guardar el nuevo usuario en la BD simulada
            st.session_state['db_users'][num_doc] = {
                "password": pass1,
                "nombre": nombre_nuevo.upper() if nombre_nuevo else "USUARIO NUEVO",
                "correo": correo,
                "celular": celular,
                "peso": 0.0,
                "talla": 0,
                "direccion": "No especificada",
                "centro": "CAP POR ASIGNAR"
            }
            st.success("✅ ¡Cuenta creada exitosamente! Por favor, inicia sesión.")
    
    st.write("---")
    st.write("<center>¿Ya tienes una cuenta?</center>", unsafe_allow_html=True)
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
    user_data = st.session_state['db_users'][st.session_state['current_user_dni']]
    
    st.header("Datos de Contacto")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Operador", ["Entel", "Claro", "Movistar", "Bitel"])
    with col2:
        celular = st.text_input("Celular", value=user_data["celular"])
    
    correo = st.text_input("Correo", value=user_data["correo"])
    
    st.header("Datos de Ubicación")
    st.selectbox("Departamento", ["Lima"])
    st.selectbox("Provincia", ["Lima"])
    st.selectbox("Distrito", ["Miraflores", "San Isidro", "Lince", "Comas", "Puente Piedra"])
    direccion = st.text_input("Dirección", value=user_data["direccion"])
    
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("Guardar Cambios", type="primary", use_container_width=True):
            # Actualizar datos en la BD simulada
            st.session_state['db_users'][st.session_state['current_user_dni']]['celular'] = celular
            st.session_state['db_users'][st.session_state['current_user_dni']]['correo'] = correo
            st.session_state['db_users'][st.session_state['current_user_dni']]['direccion'] = direccion
            st.success("¡Datos actualizados!")

def screen_diabetes():
    user_data = st.session_state['db_users'][st.session_state['current_user_dni']]
    st.title("Test Diabetes T2")
    
    peso = st.number_input("¿Cuál es su peso (kg)?", value=float(user_data["peso"]), step=0.1)
    talla_cm = st.number_input("¿Cuál es su talla (cm)?", value=int(user_data["talla"]), step=1)
    
    if talla_cm > 0:
        imc = peso / ((talla_cm/100)**2)
        st.info(f"Su índice de masa corporal es: **{imc:.1f} kg/m²**")
        
    st.number_input("¿Cuánto mide su cintura (cm)?", value=80, step=1)
    
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
    
    if st.button("Evaluar", type="primary", use_container_width=True):
        st.session_state['db_users'][st.session_state['current_user_dni']]['peso'] = peso
        st.session_state['db_users'][st.session_state['current_user_dni']]['talla'] = talla_cm
        st.success("Evaluación guardada con éxito.")

# --- ESTRUCTURA PRINCIPAL (SIDEBAR + CONTENIDO) ---

if not st.session_state['logged_in']:
    if st.session_state['current_page'] == 'Registro':
        screen_registro()
    else:
        screen_login()
else:
    # Obtener los datos del usuario logueado
    current_user_info = st.session_state['db_users'][st.session_state['current_user_dni']]
    
    # --- MENÚ LATERAL (Solo visible si está logueado) ---
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/EsSalud_logo.svg/2560px-EsSalud_logo.svg.png", width=150)
        st.markdown(f"**Hola, {current_user_info['nombre']}**")
        st.caption(f"Mi Centro:\n{current_user_info['centro']}")
        st.caption("Vigencia Hasta: 31/12/2024")
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
