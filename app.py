import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Registro de Ventas", layout="wide")

# --- Título principal ---
st.markdown("<h1 style='text-align:center; color:#2E86C1;'>📦 Sistema de Ventas Diario</h1>", unsafe_allow_html=True)
st.write("Selecciona una categoría, elige el producto vendido y registra la cantidad.")

# --- Inicialización de datos ---
if "categorias" not in st.session_state:
    st.session_state.categorias = {
        "Cloro": ["Cloro"]
    }

# --- Ruta del archivo CSV ---
fecha_actual = datetime.now().strftime("%Y-%m-%d")
nombre_archivo = f"ventas_{fecha_actual}.csv"
ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)

# --- Función para guardar ventas ---
def guardar_venta(usuario, categoria, producto, cantidad):
    nueva_venta = pd.DataFrame([{
        "Fecha": fecha_actual,
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
    st.success(f"✅ Venta registrada: {cantidad} de '{producto}' ({categoria}) por {usuario}")

# --- Función para agregar nueva categoría ---
def agregar_categoria():
    with st.form("nueva_cat"):
        nueva_cat = st.text_input("Nombre de nueva categoría")
        nuevo_prod = st.text_input("Productos separados por coma (opcional)")
        agregar = st.form_submit_button("Agregar")
        if agregar and nueva_cat:
            productos = [p.strip() for p in nuevo_prod.split(",") if p.strip()]
            if nueva_cat in st.session_state.categorias:
                st.warning(f"⚠️ La categoría '{nueva_cat}' ya existe.")
                sobrescribir = st.checkbox("¿Deseas sobrescribir los productos existentes?")
                if sobrescribir:
                    st.session_state.categorias[nueva_cat] = productos
                    st.success(f"✅ Productos actualizados en la categoría '{nueva_cat}'.")
            else:
                st.session_state.categorias[nueva_cat] = productos
                st.success(f"✅ Categoría '{nueva_cat}' agregada con éxito.")

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

# --- Panel lateral ---
st.sidebar.header("⚙️ Opciones")
accion = st.sidebar.radio("Selecciona una acción:", ["Registrar venta", "Agregar categoría", "Eliminar categoría o producto"])

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
                if cols2[i % 4].button(prod, key=f"btn_{categoria}_{prod}"):
                    st.session_state.producto_seleccionado = prod
                    st.session_state.ingresando_cantidad = True

            if "ingresando_cantidad" in st.session_state and st.session_state.ingresando_cantidad:
                prod = st.session_state.producto_seleccionado
                cantidad = st.number_input(f"Ingresa cantidad vendida de {prod}:", min_value=1, step=1)
                if st.button("Registrar venta", key="registrar"):
                    guardar_venta(usuario, categoria, prod, cantidad)
                    st.session_state.mostrando_productos = False
                    st.session_state.ingresando_cantidad = False
                    st.experimental_rerun()

        # --- Visualización de ventas ---
        if os.path.exists(ruta_archivo):
            st.subheader("📈 Ventas registradas hoy")
            df_ventas = pd.read_csv(ruta_archivo)
            st.dataframe(df_ventas)

            st.subheader("📊 Vent
