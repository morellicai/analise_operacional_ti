import pandas as pd
import streamlit as st


def normalize_date_format(date_str):
    """
    Normaliza o formato da data para o padrão dd/mm/yyyy
    """
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.dt.strftime('%d/%m/%Y')
    except Exception as e:
        st.error(f'Erro ao normalizar a data: {e}')
        return date_str
