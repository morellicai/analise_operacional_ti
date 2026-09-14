import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BOARD_ID = '6a67a5b04b5807ee0484db29'


def data_cards():
    url = f'https://api.trello.com/1/boards/{BOARD_ID}/cards'
    headers = {'Accept': 'application/json'}
    query = {'key': os.getenv('API_KEY'), 'token': os.getenv('SECRET_KEY')}

    try:
        response = requests.get(url, headers=headers, params=query)

        return response.json()

    except requests.exceptions.HTTPError as erro_http:
        st.error(
            f'Erro rota cards -> Falha na comunicação com o Trello: {erro_http}'
        )

    except requests.exceptions.ConnectionError as erro_conexao:
        st.error(
            f'Sem conexão com a internet ou firewall bloqueado: {erro_conexao}'
        )

    except Exception as erro_geral:
        st.error(f'Erro inesperado durante a estração: {erro_geral}')


def data_label():
    url = f'https://api.trello.com/1/boards/{BOARD_ID}/labels'
    headers = {'Accept': 'application/json'}
    query = {'key': os.getenv('API_KEY'), 'token': os.getenv('SECRET_KEY')}

    try:
        response = requests.get(url, headers=headers, params=query)

        return response.json()

    except requests.exceptions.HTTPError as erro_http:
        st.error(
            f'Erro rota labels -> Falha na comunicação com o Trello: {erro_http}'
        )

    except requests.exceptions.ConnectionError as erro_conexao:
        st.error(
            f'Sem conexão com a internet ou firewall bloqueado: {erro_conexao}'
        )

    except Exception as erro_geral:
        st.error(f'Erro inesperado durante a estração: {erro_geral}')


def data_lists():
    url = f'https://api.trello.com/1/boards/{BOARD_ID}/lists'
    headers = {'Accept': 'application/json'}
    query = {'key': os.getenv('API_KEY'), 'token': os.getenv('SECRET_KEY')}

    try:
        response = requests.get(url, headers=headers, params=query)

        return response.json()

    except requests.exceptions.HTTPError as erro_http:
        st.error(
            f'Erro rota lists -> Falha na comunicação com o Trello: {erro_http}'
        )

    except requests.exceptions.ConnectionError as erro_conexao:
        st.error(
            f'Sem conexão com a internet ou firewall bloqueado: {erro_conexao}'
        )

    except Exception as erro_geral:
        st.error(f'Erro inesperado durante a estração: {erro_geral}')
