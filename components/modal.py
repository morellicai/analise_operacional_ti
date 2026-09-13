import streamlit as st

@st.dialog("Detalhes do Chamado")
def modal_detalhs(select_line):
    st.markdown(f"## {select_line['Nome do Card']}")
    st.markdown(f"- **Prioridade**: {select_line['Prioridade']}\n- **Data Inicio**: {select_line['Data Inicio']}")
    st.markdown(f"\n\n---\n\n{select_line['desc']}")


