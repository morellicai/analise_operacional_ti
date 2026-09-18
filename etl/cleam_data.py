def cleam_data_cards(df):
    df = df.dropna(axis=1, how='all')
    df = df.drop(
        columns=[
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
            'labels',
        ]
    )

    df = df.rename(
        columns={
            'due': 'Data Prevista Entrega',
            'start': 'Data Inicio',
            'name': 'Nome do Card',
            'dateLastActivity': 'Última atividade',
            'dueComplete': 'Card Finalizado',
        }
    )

    return df


def cleam_data_labels(df):
    df = df.drop(columns=['idBoard'])

    df = df.rename(columns={'name': 'Prioridade', 'uses': 'Uso'})

    return df


def cleam_data_lists(df):
    df = df.drop(columns=['closed', 'idBoard', 'pos'])

    df = df.rename(columns={'name': 'Categoria'})

    return df


def cleam_data_actions(df):
    df = df.dropna(axis=1, how='all')

    df = df.drop(
        columns=[
            'idMemberCreator',
            'type',
            'data.card.shortLink',
            'data.board.shortLink',
            'data.board.id',
            'data.board.name',
            'data.list.color',
            'memberCreator.id',
            'memberCreator.activityBlocked',
            'memberCreator.avatarHash',
            'memberCreator.avatarUrl',
            'memberCreator.initials',
            'memberCreator.username',
            'memberCreator.idMemberReferrer',
            'memberCreator.nonPublicAvailable',
        ]
    )
    return df
