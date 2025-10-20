import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =========================================
# CONFIGURACIÓN INICIAL
# =========================================
st.set_page_config(page_title="Punto de Venta", layout="wide")

# Archivo de productos
PRODUCTOS_FILE = "productos.csv"

# Crear archivo productos.csv si no existe
if not os.path.exists(PRODUCTOS_FILE):
    df_init = pd.DataFrame({
        "Categoria": ["Fabuloso", "Detergente", "Suavitel", "Cloro"],
        "Producto": ["Lavanda", "Ariel", "Downy", "Cloro"]
    })
    df_init.to_csv(PRODUCTOS_FILE, index=False)

# Leer productos
productos_df = pd.read_csv(PRODUCTOS_FILE)

# Función auxiliar para guardar registro diario
def guardar_registro(categoria, producto, cantidad):
    hoy = datetime.now().strftime("%Y-%m-%d")
    archivo = f"pedidos_{hoy}.csv"
    now = datetime.now().strftime("%H:%M:%S")

    registro = pd.DataFrame([{
        "Fecha": hoy,
        "Hora": now,
        "Categoria": categoria,
        "Producto": producto,
        "Cantidad": cantidad
    }])

    # Si el archivo ya existe, agregar al final
    if os.path.exists(archivo):
        registro.to_csv(archivo, mode="a", header=False, index=False)
    else:
        registro.to_csv(archivo, index=False)

# =========================================
# INTERFAZ
# =========================================
st.title("🧴 Punto de Venta - Registro de Ventas Diarias")

# --- Sección para agregar productos ---
with st.expander("➕ Agregar nueva categoría o producto"):
    st.write("Agrega nuevos productos o categorías al catálogo existente.")
    nueva_categoria = st.text_input("Nombre de la nueva categoría")
    nuevo_producto = st.text_input("Nombre del nuevo producto")

    if st.button("Agregar al catálogo"):
        if nueva_categoria and nuevo_producto:
            nuevos = pd.DataFrame({"Categoria": [nueva_categoria], "Producto": [nuevo_producto]})
            nuevos.to_csv(PRODUCTOS_FILE, mode="a", header=False, index=False)
            st.success(f"✅ '{nuevo_producto}' agregado a la categoría '{nueva_categoria}'. Recarga la app para verlo.")
        else:
            st.warning("⚠️ Debes escribir una categoría y un producto.")

st.divider()

# --- Menú principal de categorías ---
st.header("Selecciona una categoría:")
categorias = sorted(productos_df["Categoria"].unique())

cols = st.columns(4)
for i, cat in enumerate(categorias):
    if cols[i % 4].button(cat):
        st.session_state["categoria"] = cat

# Si se seleccionó una categoría, mostrar productos
if "categoria" in st.session_state:
    st.subheader(f"🧩 Productos de la categoría: {st.session_state['categoria']}")
    productos_cat = productos_df[productos_df["Categoria"] == st.session_state["categoria"]]["Producto"].tolist()

    cols2 = st.columns(4)
    for i, prod in enumerate(productos_cat):
        if cols2[i % 4].button(prod):
            st.session_state["producto"] = prod

# Si se seleccionó producto, pedir cantidad
if "producto" in st.session_state:
    producto = st.session_state["producto"]
    categoria = st.session_state["categoria"]

    st.write(f"### 🧾 Registrar venta de: **{producto}** (Categoría: {categoria})")
    cantidad = st.number_input("Cantidad vendida:", min_value=1, step=1)

    if st.button("Registrar venta"):
        guardar_registro(categoria, producto, cantidad)
        st.success("✅ Venta registrada correctamente.")
        # Limpiar selección para volver al menú principal
        del st.session_state["producto"]
        del st.session_state["categoria"]

# =========================================
# DESCARGAR CSV DEL DÍA
# =========================================
st.divider()
hoy = datetime.now().strftime("%Y-%m-%d")
archivo_hoy = f"pedidos_{hoy}.csv"

if os.path.exists(archivo_hoy):
    with open(archivo_hoy, "rb") as f:
        st.download_button(
            label=f"📥 Descargar ventas del día ({hoy})",
            data=f,
            file_name=archivo_hoy,
            mime="text/csv"
        )
else:
    st.info("📦 Aún no hay ventas registradas hoy.")
