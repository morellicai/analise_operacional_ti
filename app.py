# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

BOARD_ID = "6a67a5b04b5807ee0484db29"

def data_cards():
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/cards"
    headers = {"Accept": "application/json"}
    query = {
        'key': os.getenv("API_KEY"),
        'token': os.getenv("SECRET_KEY")
    }

    try:
        response = requests.get(url, headers=headers, params=query)

        return response.json()

    except requests.exceptions.HTTPError as erro_http:
        st.error(f'Erro rota cards -> Falha na comunicação com o Trello: {erro_http}')

    except requests.exceptions.ConnectionError as erro_conexao:
        st.error(f'Sem conexão com a internet ou firewall bloqueado: {erro_conexao}')

    except Exception as erro_geral:
        st.error(f'Erro inesperado durante a estração: {erro_geral}')

def data_label():
    url = (f'https://api.trello.com/1/boards/{BOARD_ID}/labels')
    headers = {"Accept": "application/json"}
    query = {
        'key': os.getenv("API_KEY"),
        'token': os.getenv("SECRET_KEY")
    }

    try:
        response = requests.get(url, headers=headers, params=query)

        return response.json()

    except requests.exceptions.HTTPError as erro_http:
        st.error(f'Erro rota labels -> Falha na comunicação com o Trello: {erro_http}')

    except requests.exceptions.ConnectionError as erro_conexao:
        st.error(f'Sem conexão com a internet ou firewall bloqueado: {erro_conexao}')

    except Exception as erro_geral:
        st.error(f'Erro inesperado durante a estração: {erro_geral}')

def data_lists():
    url = (f'https://api.trello.com/1/boards/{BOARD_ID}/lists')
    headers = {"Accept": "application/json"}
    query = {
        'key': os.getenv("API_KEY"),
        'token': os.getenv("SECRET_KEY")
    }

    try:
        response = requests.get(url, headers=headers, params=query)

        return response.json()

    except requests.exceptions.HTTPError as erro_http:
        st.error(f'Erro rota lists -> Falha na comunicação com o Trello: {erro_http}')

    except requests.exceptions.ConnectionError as erro_conexao:
        st.error(f'Sem conexão com a internet ou firewall bloqueado: {erro_conexao}')

    except Exception as erro_geral:
        st.error(f'Erro inesperado durante a estração: {erro_geral}')

def cleam_data_cards(df):
    df = df.dropna(axis=1, how='all')
    df = df.drop(columns=[
        'idBoard', 
        'nodeId', 
        'id', 
        'closed', 
        'isTemplate',
        'subscribed',
        'shortLink',
        'shortUrl',
        'cover',
        'url',
        'pinned',
        'idMembersVoted',
        'labels'
    ])

    return df

def cleam_data_labels(df):
    df = df.drop(columns=['idBoard'])
    return df

def cleam_data_lists(df):
    df = df.drop(columns=['closed', 'idBoard', 'pos'])
    return df

def join_tables(df_left, df_center, df_right):
    """
    Trazer por join os titulos para os ids que vem de outra tabela
    """
    df_left_exploded = df_left.explode('idLabels')
    join = df_left_exploded.merge(df_center, left_on='idLabels', right_on='id', how='inner')
    join = join.merge(df_right, left_on='idList', right_on='id', how='inner')

    return join

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


dados_cards_json = data_cards()
dados_labels_json = data_label()
dados_lists_json = data_lists()
data_cards = pd.DataFrame(dados_cards_json)
data_label = pd.DataFrame(dados_labels_json)
data_lists = pd.DataFrame(dados_lists_json)

data_cards = cleam_data_cards(data_cards)
data_label = cleam_data_labels(data_label)
data_lists = cleam_data_lists(data_lists)
data_label = data_label.rename(columns={
    'name': 'Prioridade',
    'uses': 'Uso'
})

data_cards = data_cards.rename(columns={
    'due': 'Data Prevista Entrega', 
    'start': 'Data Inicio', 
    'name': 'Nome do Card', 
    'dateLastActivity': 'Última atividade',
    'dueComplete': 'Card Finalizado'
})


df_join = join_tables(data_cards, data_label, data_lists)

df_join['Última atividade'] = normalize_date_format(df_join['Última atividade'])
df_join['Data Inicio'] = normalize_date_format(df_join['Data Inicio'])
df_join['Data Prevista Entrega'] = normalize_date_format(df_join['Data Prevista Entrega'])

df_join = df_join.rename(columns={'name': 'Categoria'})

# 3. Exibição no Streamlit
st.set_page_config(page_title="Painel de Operações TI", page_icon="💻", layout="wide")
st.title("💻 Painel de Operações TI")

# Filtramos apenas o nome da tarefa e o ID da lista para inspecionar
df = df_join[['idShort','Nome do Card', 'Prioridade', 'Data Inicio', 'Data Prevista Entrega', 'Card Finalizado', 'Última atividade', 'Categoria']]

col1, col2, col3, col4 = st.columns(4, border=True, gap='small')

cards_finalizados_count = df['Card Finalizado'].value_counts().get(True, 0)
count_cards_em_andamento = df_join['Categoria'].value_counts().get('Em andamento', 0)
cards_finalizados_count_by_priority = df[df['Card Finalizado'] & df['Prioridade'].isin(['Alta', 'Crítico / Urgente'])].shape[0]

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

st.subheader("Chamados Brutos:")
st.dataframe(df, hide_index=True)