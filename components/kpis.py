import streamlit as st

from etl.metrics import (
    cards_em_andamento,
    cards_finalizados_count_by_priority,
    soma_finalizados,
)


def kpis(df):
    col1, col2, col3, col4 = st.columns(4, border=True, gap='small')
    with col1:
        st.metric(
            label='Volume de Cards finalizados', value=soma_finalizados(df)
        )
    with col2:
        st.metric(
            label='Volume de Cards em Andamento', value=cards_em_andamento(df)
        )
    with col3:
        st.metric(
            label='Volume de Cards A Fazer',
            value=df['Categoria'].isin(['A Fazer']).sum(),
        )
    with col4:
        st.metric(
            label='Volume de Cards Finalizados por prioridade Alta e Crítico',
            value=cards_finalizados_count_by_priority(df),
        )
