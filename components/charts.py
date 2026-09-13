import streamlit as st
import pandas as pd
from etl.metrics import count_priorit

def charts1(df):
    chart_col1, chart_col2 = st.columns(2, border=True, gap='small')

    with chart_col1:
        st.markdown("### 📊 Chamados por Categoria")
        st.space()
        st.bar_chart(df['Categoria'].value_counts(), use_container_width=True, height=300, width=400)

    with chart_col2:
        st.markdown("### 📊 Chamados por Prioridade")
        st.space()
        st.bar_chart(count_priorit(df), x='Prioridade', y='Uso', stack=False, use_container_width=True, horizontal=True, height=300, width=400)

def charts2(df):
    chart2_col1, chart2_col2 = st.columns(2, border=True, gap='small')
    
    grouped_df = df.groupby([df['Data Inicio']]).count().reset_index()
    with chart2_col1:
        st.line_chart(grouped_df, x='Data Inicio', y='idShort', use_container_width=True, height=300, width=400)
