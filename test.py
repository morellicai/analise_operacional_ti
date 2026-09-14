import pandas as pd
import streamlit as st


# 1. Definimos a função do Modal usando a decoração @st.dialog
@st.dialog('Detalhes do Item')
def abrir_modal_detalhes(linha_selecionada):
    # Exibe os dados da linha recebida
    st.write(f'### {linha_selecionada["Nome"]}')

    st.write(f'**ID:** {linha_selecionada["ID"]}')
    st.write(f'**Categoria:** {linha_selecionada["Categoria"]}')
    st.write(f'**Valor:** R$ {linha_selecionada["Valor"]:.2f}')
    st.write(f'**Status:** {linha_selecionada["Status"]}')

    st.markdown('---')
    st.write('**Descrição completa:**')
    st.info(linha_selecionada['Descrição'])

    # Botão opcional para fechar manualmente (ou clicar fora do modal)
    if st.button('Fechar'):
        st.rerun()


# 2. Criamos dados fictícios para a tabela
dados = {
    'ID': [101, 102, 103],
    'Nome': ['Item A', 'Item B', 'Item C'],
    'Categoria': ['Eletrônicos', 'Escritório', 'Informática'],
    'Valor': [150.00, 45.50, 1200.00],
    'Status': ['Ativo', 'Inativo', 'Ativo'],
    'Descrição': [
        'Detalhes aprofundados sobre o Item A e suas especificações.',
        'Descrição detalhada do Item B para controle de estoque.',
        'Equipamento de alta performance para a equipe de TI.',
    ],
}

df = pd.DataFrame(dados)

st.title('Gerenciador de Dados')
st.write('Selecione uma linha na tabela para ver os detalhes completos:')

# 3. Renderizamos a tabela ativando a seleção de linha única
evento_selecao = st.dataframe(
    df,
    hide_index=True,
    on_select='rerun',
    selection_mode='single-row',
)

# 4. Verificamos se alguma linha foi selecionada
linhas_selecionadas = evento_selecao['selection']['rows']

if linhas_selecionadas:
    index_linha = linhas_selecionadas[0]
    dados_da_linha = df.iloc[index_linha]

    # Chama a função configurada como modal
    abrir_modal_detalhes(dados_da_linha)
