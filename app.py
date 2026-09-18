import pandas as pd
import streamlit as st

from components.charts import charts1, charts2
from components.kpis import kpis
from components.modal import modal_detalhs
from components.sidebar import sidebar
from etl.api import data_actions, data_cards, data_label, data_lists
from etl.cleam_data import (
    cleam_data_actions,
    cleam_data_cards,
    cleam_data_labels,
    cleam_data_lists,
)
from etl.join import join_last_line, join_tables

st.set_page_config(
    page_title='Painel de Operações TI', page_icon='💻', layout='wide'
)

data_cards = cleam_data_cards(pd.DataFrame(data_cards()))
data_label = cleam_data_labels(pd.DataFrame(data_label()))
data_lists = cleam_data_lists(pd.DataFrame(data_lists()))
data_actions = cleam_data_actions(
    pd.json_normalize(data_actions(), max_level=2)
)


df_join = join_tables(data_cards, data_label, data_lists)
df_join = join_last_line(data_actions, df_join)

date_cols = ['Data Inicio', 'Data Prevista Entrega', 'Última atividade']
for col in date_cols:
    df_join[col] = pd.to_datetime(df_join[col], errors='coerce')

df = df_join[
    [
        'idShort',
        'Nome do Card',
        'Prioridade',
        'Data Inicio',
        'Data Prevista Entrega',
        'Card Finalizado',
        'Última atividade',
        'Categoria',
        'desc',
    ]
]

df = sidebar(df)

kpis(df)

st.space()

charts1(df)
charts2(df)

st.markdown('---')

st.subheader('Tabela Chamados:')

df_display = df.copy()
for col in ['Data Inicio', 'Data Prevista Entrega', 'Última atividade']:
    df_display[col] = df_display[col].dt.strftime(  # type: ignore
        '%d/%m/%Y'
    )

select = st.dataframe(
    df_display[
        [
            'Nome do Card',
            'Categoria',
            'Prioridade',
            'Data Inicio',
            'Data Prevista Entrega',
            'Card Finalizado',
            'Última atividade',
        ]
    ],
    hide_index=True,
    on_select='rerun',
    selection_mode='single-row',
)

select_line = select['selection']['rows']

if select_line:
    index_line = select_line[0]
    data_line = df_display.iloc[index_line]

    modal_detalhs(data_line)

st.markdown('---')

st.dataframe(data_actions)
