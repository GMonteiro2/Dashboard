import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Financeiro', layout='wide')

st.title('💰 Dashboard Financeiro')

transacoes = pd.read_csv('dados/transacoes.csv')
transacoes['data'] = pd.to_datetime(transacoes['data'])

despesas = transacoes[transacoes['tipo'] == 'despesa']
receitas = transacoes[transacoes['tipo'] == 'receita']

st.sidebar.title('🔍 Filtros')

categorias_disponiveis = sorted(despesas['categoria'].unique())

categorias_selecionadas = st.sidebar.multiselect(
    'Filtrar por categoria:',
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

despesas = despesas[despesas['categoria'].isin(categorias_selecionadas)]

total_despesas = despesas['valor'].sum()
total_receitas = receitas['valor'].sum()
saldo = total_receitas - total_despesas

col1, col2, col3 = st.columns(3)
col1.metric('Total de Receitas', f'R$ {total_receitas:.2f}')
col2.metric('Total de Despesas', f'R$ {total_despesas:.2f}')
col3.metric('Saldo', f'R$ {saldo:.2f}')
col4, col5 = st.columns(2)


with col4:
    st.subheader('Gastos por Categoria')
    por_categoria = despesas.groupby('categoria')['valor'].sum()
    fig1 = px.pie(
        values=por_categoria.values,
        names=por_categoria.index,
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    st.subheader('Gastos por Mês')
    por_mes = despesas.groupby(despesas['data'].dt.to_period('M'))['valor'].sum()
    fig2 = px.bar(
        x=['Janeiro', 'Fevereiro'],
        y=por_mes.values,
        labels={'x': 'Mês', 'y': 'Total (R$)'},
        color=por_mes.values,
        color_continuous_scale='RdBu'
    )
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)