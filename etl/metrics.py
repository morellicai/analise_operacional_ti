import pandas as pd

def soma_finalizados(df):
    return df['Card Finalizado'].value_counts().get(True, 0)

def cards_em_andamento(df):
    return df['Categoria'].value_counts().get('Em andamento', 0)

def cards_finalizados_count_by_priority(df):
    return df[df['Card Finalizado'] & df['Prioridade'].isin(['Alta', 'Crítico / Urgente'])].shape[0]

def count_priorit(df):
    return df['Prioridade'].value_counts().reset_index().rename(columns={'count': 'Uso'})
