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

def join_tables(df_left, df_right):
    """
    Trazer por join os titulos para os ids que vem de outra tabela
    """
    df_left_exploded = df_left.explode('idLabels')
    join = df_left_exploded.merge(df_right, left_on='idLabels', right_on='id', how='inner')

    return join

dados_cards_json = data_cards()
dados_labels_json = data_label()

data_cards = pd.DataFrame(dados_cards_json)
data_label = pd.DataFrame(dados_labels_json)

data_cards = cleam_data_cards(data_cards)
data_label = cleam_data_labels(data_label)

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

df_join = join_tables(data_cards, data_label)

# 3. Exibição no Streamlit
st.title("💻 Painel de Operações TI")
st.write("Chamados Brutos:")
# Filtramos apenas o nome da tarefa e o ID da lista para inspecionar

st.dataframe(df_join[['idShort','Nome do Card', 'Prioridade', 'Última atividade', 'Data Inicio', 'Data Prevista Entrega']], hide_index=True)

st.bar_chart(data_label, x='Prioridade', y='Uso', stack=False)