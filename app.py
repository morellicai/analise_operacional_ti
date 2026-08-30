# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import pandas as pd
import streamlit as st
from api import data_cards, data_label, data_lists
from cleam_data import cleam_data_cards, cleam_data_labels, cleam_data_lists
from join import join_tables
from normalize import normalize_date_format

# 1. Extração dos dados da API do Trello
data_cards = cleam_data_cards(pd.DataFrame(data_cards()))
data_label = cleam_data_labels(pd.DataFrame(data_label()))
data_lists = cleam_data_lists(pd.DataFrame(data_lists()))

# 2. Normalização e junção dos dados
df_join = join_tables(data_cards, data_label, data_lists)
df_join[['Última atividade', 'Data Inicio', 'Data Prevista Entrega']] = df_join[['Última atividade', 'Data Inicio', 'Data Prevista Entrega']].apply(normalize_date_format)
df = df_join[['idShort','Nome do Card', 'Prioridade', 'Data Inicio', 'Data Prevista Entrega', 'Card Finalizado', 'Última atividade', 'Categoria']]

# Indicadores KPI's
cards_finalizados_count = df['Card Finalizado'].value_counts().get(True, 0)
count_cards_em_andamento = df_join['Categoria'].value_counts().get('Em andamento', 0)
cards_finalizados_count_by_priority = df[df['Card Finalizado'] & df['Prioridade'].isin(['Alta', 'Crítico / Urgente'])].shape[0]

# 3. Configuração da pagina de Exibição no Streamlit
st.set_page_config(page_title="Painel de Operações TI", page_icon="💻", layout="wide")

st.title("💻 Painel de Operações TI")

col1, col2, col3, col4 = st.columns(4, border=True, gap='small')

with col1:
    st.metric(
        value=cards_finalizados_count,
        label='Volume de Cards Finalizados' 
    )
with col2:
    st.metric(label='Cards finalizados por prioridade Alta e Crítico / Urgente', value=cards_finalizados_count_by_priority)
with col3:
    st.metric(label='Volume de Cards em Andamento', value=count_cards_em_andamento)
with col4:
    st.metric(label='Total de Cards', value=len(df))

st.space()

chart_col1, chart_col2 = st.columns(2, border=True, gap='small')

with chart_col1:
    st.markdown("### 📊 Chamados por Categoria")
    st.space()
    st.bar_chart(df_join['Categoria'].value_counts(), use_container_width=True, height=300, width=400)

with chart_col2:
    st.markdown("### 📊 Chamados por Prioridade")
    st.space()
    st.bar_chart(data_label, x='Prioridade', y='Uso', stack=False, use_container_width=True, horizontal=True, height=300, width=400)

chart2_col1, chart2_col2 = st.columns(2, border=True, gap='small')

with chart2_col1:
    st.line_chart(df_join, x='Data Inicio', y='idShort', use_container_width=True, height=300, width=400)

st.markdown('---')

st.subheader("Tabela Chamados Brutos:")
st.dataframe(df, hide_index=True)