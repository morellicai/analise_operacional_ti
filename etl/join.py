

def join_tables(df_left, df_center, df_right):
    """
    Trazer por join os titulos para os ids que vem de outra tabela
    """

    df_left_exploded = df_left.explode('idLabels')
    join = df_left_exploded.merge(
        df_center, left_on='idLabels', right_on='id', how='inner'
    )
    join = join.merge(df_right, left_on='idList', right_on='id', how='inner')

    return join
