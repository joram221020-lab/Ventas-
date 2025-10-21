import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
st.set_page_config(page_title="Punto de Venta", page_icon="🧾", layout="wide")

# ==============================
# FUNCIONES AUXILIARES
# ==============================
def obtener_nombre_archivo():
    """Genera el nombre del archivo CSV según la fecha actual."""
    fecha = datetime.now().strftime("%Y-%m-%d")
    return f"ventas_{fecha}.csv"

PRODUCTOS_FILE = "productos.csv"

# ==============================
# ARCHIVO DE PRODUCTOS
# ==============================
if not os.path.exists(PRODUCTOS_FILE):
    df_prod = pd.DataFrame({
        "Categoría": ["Cloro"],
        "Producto": ["Cloro"]
    })
    df_prod.to_csv(PRODUCTOS_FILE, index=False)

productos = pd.read_csv(PRODUCTOS_FILE)

# ==============================
# ESTILO PERSONALIZADO
# ==============================
st.markdown("""
    <style>
        body {
            background-color: #f0fff4;
        }
        .stButton>button {
            background-color: #38a169;
            color: white;
            border-radius: 10px;
            height: 3em;
            width: 100%;
            border: none;
            font-size: 16px;
            font-weight: bold;
            transition: 0.2s;
        }
        .stButton>button:hover {
            background-color: #2f855a;
            transform: scale(1.02);
        }
        .categoria {
            padding: 15px;
            border-radius: 12px;
            background-color: #c6f6d5;
            text-align: center;
            font-weight: bold;
            color: #22543d;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# TÍTULO PRINCIPAL
# ==============================
st.title("💚 Registro de Ventas del Punto de Venta")
st.markdown("Selecciona una **categoría**, luego un **producto**, indica la cantidad y registra la venta.")

# ==============================
# SECCIÓN DE CATEGORÍAS
# ==============================
categorias = sorted(productos["Categoría"].unique())
st.subheader("🧺 Categorías disponibles")

cols = st.columns(4)
cat_elegida = st.session_state.get("categoria", None)

for i, cat in enumerate(categorias):
    if cols[i % 4].button(cat):
        st.session_state.categoria = cat
        cat_elegida = cat

# ==============================
# SECCIÓN DE PRODUCTOS
# ==============================
if cat_elegida:
    st.markdown(f"### 🛒 Productos de la categoría: **{cat_elegida}**")

    prods = productos[productos["Categoría"] == cat_elegida]["Producto"].tolist()
    cols2 = st.columns(4)
    prod_sel = st.session_state.get("producto", None)

    for i, prod in enumerate(prods):
        if cols2[i % 4].button(prod):
            st.session_state.producto = prod
            prod_sel = prod

    if prod_sel:
        st.success(f"Seleccionado: **{prod_sel}** de la categoría **{cat_elegida}**")
        cantidad = st.number_input("Cantidad vendida:", min_value=1, step=1, key="cantidad_input")

        if st.button("✅ Registrar venta"):
            archivo = obtener_nombre_archivo()
            nueva_venta = pd.DataFrame({
                "Fecha": [datetime.now().strftime("%Y-%m-%d")],
                "Hora": [datetime.now().strftime("%H:%M:%S")],
                "Categoría": [cat_elegida],
                "Producto": [prod_sel],
                "Cantidad": [cantidad]
            })

            if os.path.exists(archivo):
                ventas = pd.read_csv(archivo)
                ventas = pd.concat([ventas, nueva_venta], ignore_index=True)
            else:
                ventas = nueva_venta

            ventas.to_csv(archivo, index=False)
            st.success(f"✅ Venta registrada: {cantidad} unidades de {prod_sel}.")
            st.balloons()

# ==============================
# SECCIÓN PARA AGREGAR PRODUCTOS
# ==============================
st.markdown("---")
st.header("➕ Agregar nueva categoría o producto")

with st.form("agregar_form"):
    nueva_categoria = st.text_input("Nueva categoría (o existente):")
    nuevo_producto = st.text_input("Nuevo producto:")
    agregar = st.form_submit_button("Agregar")

    if agregar:
        if nueva_categoria and nuevo_producto:
            nuevo = pd.DataFrame({"Categoría": [nueva_categoria], "Producto": [nuevo_producto]})
            productos = pd.concat([productos, nuevo], ignore_index=True)
            productos.to_csv(PRODUCTOS_FILE, index=False)
            st.success(f"✅ Producto '{nuevo_producto}' agregado en la categoría '{nueva_categoria}'.")
        else:
            st.error("❌ Debes escribir una categoría y un producto.")

# ==============================
# DESCARGA DEL CSV DEL DÍA
# ==============================
st.markdown("---")
archivo_actual = obtener_nombre_archivo()
st.subheader("📦 Descargar registro del día")
if os.path.exists(archivo_actual):
    with open(archivo_actual, "rb") as f:
        st.download_button(
            label="⬇️ Descargar ventas del día (CSV)",
            data=f,
            file_name=archivo_actual,
            mime="text/csv"
        )
else:
    st.info("Aún no se han registrado ventas hoy.")

