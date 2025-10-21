import streamlit as st
import pandas as pd
import os
from datetime import datetime
import pytz

st.set_page_config(page_title="Registro de Ventas", layout="wide")

# --- Título principal ---
st.markdown("<h1 style='text-align:center; color:#2E86C1;'>📦 Sistema de Ventas Diario</h1>", unsafe_allow_html=True)
st.write("Selecciona una categoría, elige el producto vendido y registra la cantidad.")

# --- Inicialización de datos ---
if "categorias" not in st.session_state:
    st.session_state.categorias = {
        "Suavitel": ["Downy","Amanecer","Momentos Magicos","Ensueño","Primavera","Aventura Floral","Abrazo de Amor","Bebe"], 
        "Cloro": ["Cloro"], 
        "Detergentes": ["Ariel", "Mas Color", "Mas Negro", "Vel Rosita", "Vanish", "Zote", "Persil", "Ace Oxi", "Roma", "Mas Blancura", "Cloro para Mascota"], 
        "Pino Lechoso": ["Pino Lechoso", "Pino Lechoso Verde"], 
        "Fabuloso": ["Pepino Melon", "Frutas", "Poet Primavera", "Mar Fresco", "Poet Algodon", "Lavanda", "Maestro Limpio", "Mandarina", "Estefano", "Limon", "Durazno", "Cereza", "Manzana", "Uva", "Menta","Pino Pinol"], 
        "Jabon de Manos": ["Mora Azul", "Manzana", "Uva", "Cereza", "Durazno", "Pepino Melon", "Frutas", "Coco"], 
        "Jabon de Trastes": ["Salvo", "Axion"], 
        "Automotriz": ["Shampoo Auto", "Almoroll", "Abrillantador", "Cera", "Glicerina"], 
        "Aroma Auto": [ "Hugo Boss", "Adidas", "360", "Estefano", "Lacoste","Tommy", "Vainilla", "Selena", "Ferrary"], 
        "Desengrasantes": [ "Desengrasante de Motor", "Sosa Rosa", "Hipoclorito", "2 en 1"], 
        "Shampoo Cabello": ["Head and Shoulder", "Shampoo para mascota", "Pantene", "Dove"], 
        "Detercom": ["Detercom", "Detercom Aroma"], 
        "Varios": ["Insecticida", "Windex", "Vestiduras", "Quita Gota","Aceite Muebles", "Plancha Facil", "Repelente", "Creolina"], 
        "Escencia pura Auto": ["360 Red", "Vainilla", "Adiddas", "Carolina", "Nautica", "Ferrary"]
    }

# --- Zona horaria de Ciudad de México ---
zona_mexico = pytz.timezone("America/Mexico_City")
fecha_hora_actual = datetime.now(zona_mexico)
fecha_actual = fecha_hora_actual.strftime("%Y-%m-%d")
nombre_archivo = f"ventas_{fecha_actual}.csv"
ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)

# --- Función para guardar ventas ---
def guardar_venta(usuario, categoria, producto, cantidad):
    fecha_hora_actual = datetime.now(zona_mexico)
    fecha_actual = fecha_hora_actual.strftime("%Y-%m-%d")
    hora_actual = fecha_hora_actual.strftime("%H:%M:%S")
    nueva_venta = pd.DataFrame([{
        "Fecha": fecha_actual,
        "Hora": hora_actual,
        "Usuario": usuario,
        "Categoría": categoria,
        "Producto": producto,
        "Cantidad": cantidad
    }])
    if os.path.exists(ruta_archivo):
        df_existente = pd.read_csv(ruta_archivo)
        df_final = pd.concat([df_existente, nueva_venta], ignore_index=True)
    else:
        df_final = nueva_venta
    df_final.to_csv(ruta_archivo, index=False)
    st.success(f"✅ Venta registrada: {cantidad} de '{producto}' ({categoria}) por {usuario} a las {hora_actual}")

# --- Función para eliminar categoría o producto ---
def eliminar_elementos():
    st.subheader("🗑️ Eliminar elementos")
    tipo = st.radio("¿Qué deseas eliminar?", ["Categoría", "Producto"])
    if tipo == "Categoría":
        cat = st.selectbox("Selecciona categoría a eliminar", list(st.session_state.categorias.keys()))
        if st.button("Eliminar categoría"):
            del st.session_state.categorias[cat]
            st.success(f"✅ Categoría '{cat}' eliminada.")
    elif tipo == "Producto":
        cat = st.selectbox("Selecciona categoría", list(st.session_state.categorias.keys()))
        prod = st.selectbox("Selecciona producto", st.session_state.categorias[cat])
        if st.button("Eliminar producto"):
            st.session_state.categorias[cat].remove(prod)
            st.success(f"✅ Producto '{prod}' eliminado de '{cat}'.")

# --- Función para eliminar registro por índice visible ---
def eliminar_registro_por_indice():
    if os.path.exists(ruta_archivo):
        df = pd.read_csv(ruta_archivo)
        st.subheader("🗑️ Eliminar registro de venta por número")

        df_con_indice = df.reset_index(drop=False)
        st.dataframe(df_con_indice)

        idx = st.number_input("Número de venta a eliminar:", min_value=0, max_value=len(df_con_indice)-1, step=1)
        if st.button("Eliminar venta seleccionada"):
            df = df.drop(index=idx).reset_index(drop=True)
            df.to_csv(ruta_archivo, index=False)
            st.success(f"✅ Venta número {idx} eliminada correctamente.")
    else:
        st.info("No hay registros de ventas para hoy.")

# --- Panel lateral ---
st.sidebar.header("⚙️ Opciones")
accion = st.sidebar.radio("Selecciona una acción:", ["Registrar venta", "Eliminar categoría o producto", "Eliminar registro de venta"])

# --- Vista principal ---
if accion == "Registrar venta":
    usuario = st.text_input("👤 Nombre del vendedor:", key="usuario")
    if not usuario:
        st.warning("Por favor, ingresa tu nombre para registrar ventas.")
    else:
        st.subheader("Selecciona una categoría:")
        cols = st.columns(4)
        for i, cat in enumerate(st.session_state.categorias.keys()):
            if cols[i % 4].button(cat, key=f"cat_{cat}"):
                st.session_state.categoria_seleccionada = cat
                st.session_state.mostrando_productos = True

        if "mostrando_productos" in st.session_state and st.session_state.mostrando_productos:
            categoria = st.session_state.categoria_seleccionada
            productos = st.session_state.categorias[categoria]

            st.markdown(f"### 🛒 Productos en **{categoria}**")
            buscador = st.text_input("🔍 Buscar producto:", key="buscador")

            productos_filtrados = [p for p in productos if buscador.lower() in p.lower()] if buscador else productos

            cols2 = st.columns(4)
            for i, prod in enumerate(productos_filtrados):
                if cols2[i % 4].button(prod, key=f"btn_{categoria}_{prod}_{i}"):
                    st.session_state.producto_seleccionado = prod
                    st.session_state.ingresando_cantidad = True

            if "ingresando_cantidad" in st.session_state and st.session_state.ingresando_cantidad:
                prod = st.session_state.producto_seleccionado
                cantidad = st.number_input(f"Ingresa cantidad vendida de {prod}:", min_value=1, step=1)
                if st.button("Registrar venta", key="registrar"):
                    guardar_venta(usuario, categoria, prod, cantidad)
                    st.session_state.ingresando_cantidad = False
                    st.session_state.producto_seleccionado = None
                    st.success("✅ Venta registrada correctamente. Puedes registrar otro producto en la misma categoría.")

        # --- Visualización de ventas ---
        if os.path.exists(ruta_archivo):
            st.subheader("📈 Ventas registradas hoy")
            df_ventas = pd.read_csv(ruta_archivo)
            st.dataframe(df_ventas)

            st.subheader("📊 Ventas por usuario")
            st.dataframe(df_ventas.groupby("Usuario")["Cantidad"].sum().reset_index())

            # --- Descarga CSV ---
            with open(ruta_archivo, "rb") as file:
                st.download_button(
                    label="⬇️ Descargar registro del día",
                    data=file,
                    file_name=nombre_archivo,
                    mime="text/csv"
                )

elif accion == "Eliminar categoría o producto":
    eliminar_elementos()

elif accion == "Eliminar registro de venta":
    eliminar_registro_por_indice()
