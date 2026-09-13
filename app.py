import pandas as pd
import streamlit as st
from datetime import date, timedelta
from etl.api import data_cards, data_label, data_lists
from etl.metrics import soma_finalizados, cards_em_andamento, cards_finalizados_count_by_priority, count_priorit
from etl.cleam_data import cleam_data_cards, cleam_data_labels, cleam_data_lists
from etl.normalize import normalize_date_format
from etl.join import join_tables
from components.modal import modal_detalhs
from components.kpis import kpis
from components.charts import charts1, charts2
from components.sidebar import sidebar

st.set_page_config(page_title="Painel de Operações TI", page_icon="💻", layout="wide")

data_cards = cleam_data_cards(pd.DataFrame(data_cards()))
data_label = cleam_data_labels(pd.DataFrame(data_label()))
data_lists = cleam_data_lists(pd.DataFrame(data_lists()))

df_join = join_tables(data_cards, data_label, data_lists)

df_join[[
    'Data Inicio', 
    'Data Prevista Entrega', 
    'Última atividade'
]] = df_join[[
    'Data Inicio', 
    'Data Prevista Entrega', 
    'Última atividade'
]].apply(normalize_date_format)

df = df_join[[
    'idShort',
    'Nome do Card', 
    'Prioridade', 
    'Data Inicio', 
    'Data Prevista Entrega', 
    'Card Finalizado', 
    'Última atividade', 
    'Categoria',
    'desc'
]]

df = sidebar(df)

kpis(df)

st.space()

charts1(df)
charts2(df)

st.markdown('---')

st.subheader("Tabela Chamados:")

df[['Data Inicio', 'Data Prevista Entrega']] = df[['Data Inicio', 'Data Prevista Entrega']].apply(normalize_date_format)

select = st.dataframe(
    df[['Nome do Card', 'Categoria', 'Prioridade', 'Data Inicio', 'Data Prevista Entrega', 'Card Finalizado', 'Última atividade']],
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row"
)

select_line = select["selection"]["rows"]

if select_line:
    index_line = select_line[0]
    data_line = df.iloc[index_line]

    modal_detalhs(data_line)
