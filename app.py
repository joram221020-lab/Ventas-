import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Punto de Venta", layout="wide")

def obtener_nombre_archivo():
    fecha = datetime.now().strftime("%Y-%m-%d")
    return f"ventas_{fecha}.csv"

PRODUCTOS_FILE = "productos.csv"

if not os.path.exists(PRODUCTOS_FILE):
    df_prod = pd.DataFrame({"Categoría": ["Cloro"], "Producto": ["Cloro"]})
    df_prod.to_csv(PRODUCTOS_FILE, index=False)

productos = pd.read_csv(PRODUCTOS_FILE)

st.title("🧾 Registro de Ventas del Punto de Venta")
st.markdown("Selecciona una **categoría**, luego un **producto**, y registra la cantidad vendida.")

categorias = sorted(productos["Categoría"].unique())
st.subheader("Categorías disponibles:")
cols = st.columns(4)

cat_elegida = None
for i, cat in enumerate(categorias):
    if cols[i % 4].button(cat):
        cat_elegida = cat

if cat_elegida:
    st.markdown(f"### 🛒 Productos de la categoría: **{cat_elegida}**")
    prods = productos[productos["Categoría"] == cat_elegida]["Producto"].tolist()

    prod_sel = st.selectbox("Selecciona un producto:", prods)
    cantidad = st.number_input("Cantidad vendida:", min_value=1, step=1)

    if st.button("Registrar venta"):
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
        st.success(f"✅ Venta registrada: {cantidad} unidades de {prod_sel}")
        st.balloons()

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

st.markdown("---")
archivo_actual = obtener_nombre_archivo()
if os.path.exists(archivo_actual):
    with open(archivo_actual, "rb") as f:
        st.download_button(
            label="⬇️ Descargar ventas del día",
            data=f,
            file_name=archivo_actual,
            mime="text/csv"
        )
