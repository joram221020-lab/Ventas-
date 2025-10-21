
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Punto de Venta", layout="wide")

# ---------- Función para cargar datos ----------
@st.cache_data
def cargar_datos():
    try:
        return pd.read_csv("productos.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Categoría", "Producto"])

productos_df = cargar_datos()

# ---------- Interfaz ----------
st.title("🛍️ Registro de Ventas del Punto de Venta")

st.markdown("Selecciona una **categoría**, luego un **producto** y registra la cantidad vendida.")

categorias = productos_df["Categoría"].unique()

# Mostrar categorías como botones
st.subheader("📂 Categorías disponibles:")
cols = st.columns(4)
categoria_seleccionada = None
for i, cat in enumerate(categorias):
    if cols[i % 4].button(cat):
        categoria_seleccionada = cat

if categoria_seleccionada:
    st.subheader(f"🛒 Productos de la categoría: {categoria_seleccionada}")
    productos_cat = productos_df[productos_df["Categoría"] == categoria_seleccionada]["Producto"].tolist()

    cols_prod = st.columns(4)
    producto_seleccionado = None
    for i, prod in enumerate(productos_cat):
        if cols_prod[i % 4].button(prod):
            producto_seleccionado = prod

    if producto_seleccionado:
        cantidad = st.number_input("Cantidad vendida:", min_value=1, step=1, key="cantidad_venta")
        if st.button("✅ Registrar venta"):
            fecha = datetime.now().strftime("%Y-%m-%d")
            archivo = f"ventas_{fecha}.csv"
            venta = pd.DataFrame([[fecha, categoria_seleccionada, producto_seleccionado, cantidad]],
                                 columns=["Fecha", "Categoría", "Producto", "Cantidad"])
            try:
                df_existente = pd.read_csv(archivo)
                df_actualizado = pd.concat([df_existente, venta], ignore_index=True)
            except FileNotFoundError:
                df_actualizado = venta
            df_actualizado.to_csv(archivo, index=False)
            st.success(f"✅ Venta registrada: {producto_seleccionado} ({cantidad} unidades)")

# ---------- Agregar nueva categoría o producto ----------
st.markdown("---")
st.subheader("➕ Agregar nueva categoría o producto")

col1, col2 = st.columns(2)
with col1:
    nueva_categoria = st.text_input("Nueva categoría (o existente):")
with col2:
    nuevo_producto = st.text_input("Nuevo producto:")

if st.button("Agregar"):
    if nueva_categoria and nuevo_producto:
        nuevo_registro = pd.DataFrame([[nueva_categoria, nuevo_producto]], columns=["Categoría", "Producto"])
        productos_actualizado = pd.concat([productos_df, nuevo_registro], ignore_index=True)
        productos_actualizado.to_csv("productos.csv", index=False)
        st.success(f"✅ Se agregó el producto '{nuevo_producto}' a la categoría '{nueva_categoria}'.")
    else:
        st.warning("Por favor, completa ambos campos antes de agregar.")
