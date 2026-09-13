import streamlit as st
import pandas as pd

def sidebar(df):
    df['Data Prevista Entrega'] = pd.to_datetime(df['Data Prevista Entrega'], errors='coerce', dayfirst=True)
    df['Data Inicio'] = pd.to_datetime(df['Data Inicio'], errors='coerce', dayfirst=True)
    df['Ultima atividade'] = pd.to_datetime(df['Última atividade'], errors='coerce', dayfirst=True)
    
    with st.sidebar:
        st.title("💻 Painel de Operações TI")

        checkbox = st.checkbox("Filtrar por período")

        select_date = st.date_input(
            "Selecione o período de análise", 
            value=None,
            format="DD/MM/YYYY"
        )

        if select_date and checkbox:
            inicio_periodo = pd.to_datetime(select_date)
            fim_periodo = inicio_periodo + pd.Timedelta(days=7)

            df['Data Inicio'] = df['Data Inicio'].dt.tz_localize(None).dt.normalize()

            filtro_periodo = (df['Data Inicio'] >= inicio_periodo) & (df['Data Inicio'] <= fim_periodo)
            df = df.loc[filtro_periodo]

        return df
            
