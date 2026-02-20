import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analizador de Excel", layout="wide")

st.title("📊 Cointra S.A.S -Analizador")

uploaded_file = st.file_uploader("Carga tu archivo Excel", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    cols = df.columns.tolist()

    with st.sidebar:
        st.header("Configuración")
        # Filtro dinámico
        filter_col = st.selectbox("Selecciona columna para filtrar", ["Sin filtro"] + cols)
        if filter_col != "Sin filtro":
            unique_vals = df[filter_col].unique().tolist()
            selected_val = st.selectbox(f"Valor de {filter_col}", unique_vals)
            df = df[df[filter_col] == selected_val]

        # Parámetros de agrupación
        group_col = st.selectbox("Columna para agrupar (Categoría)", cols)
        value_col = st.selectbox("Columna de valores (Numérica)", cols)
        agg_func = st.selectbox("Función de agregación", ["sum", "count", "mean"])

    # Procesamiento de datos
    res = df.groupby(group_col)[value_col].agg(agg_func).sort_values(ascending=False).reset_index()
    
    col1, col2 = st.columns(2)

    # Gráfico de Barras (Top 10)
    with col1:
        st.subheader(f"Top 10 {group_col} (Barras)")
        top_10 = res.head(10)
        fig, ax = plt.subplots()
        bars = ax.bar(top_10[group_col], top_10[value_col], color='skyblue')
        
        # Añadir porcentajes
        total = top_10[value_col].sum()
        for bar in bars:
            height = bar.get_height()
            percentage = f'{(height/total)*100:.1f}%'
            ax.text(bar.get_x() + bar.get_width()/2., height, percentage,
                    ha='center', va='bottom', fontsize=9)
        
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Gráfico de Pie (Bottom 10)
    with col2:
        st.subheader(f"Últimos 10 {group_col} (Pie)")
        bottom_10 = res.tail(10)
        fig2, ax2 = plt.subplots()
        ax2.pie(bottom_10[value_col], labels=bottom_10[group_col], autopct='%1.1f%%', startangle=90)
        ax2.axis('equal') 
        st.pyplot(fig2)

    # Tabla con formato
    st.subheader("Tabla de Datos Agrupados")
    st.dataframe(res.style.background_gradient(cmap='Blues', subset=[value_col]))
else:
    st.info("💡 Por favor, carga un archivo de Excel para comenzar.")
