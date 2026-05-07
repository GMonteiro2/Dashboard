import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Financeiro', layout='wide')

col_header1, col_header2 = st.columns([8, 1])

with col_header1:
    st.title('💰 Dashboard Financeiro')
    st.caption('Controle inteligente das suas finanças pessoais')

with col_header2:
    st.markdown('''
        <a href="/?theme=light" target="_self" style="text-decoration:none;">
        </a>
    ''', unsafe_allow_html=True)
    if st.button('🌙 / ☀️'):
        st.toast('Para mudar o tema: Menu (≡) → Settings → Theme')

with st.spinner('Carregando seus dados financeiros...'):
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

# Formulário na sidebar
st.sidebar.markdown('---')
st.sidebar.subheader('➕ Adicionar Gasto')

with st.sidebar.form('form_gasto'):
    data_input = st.date_input('Data')
    descricao_input = st.text_input('Descrição')
    valor_input = st.number_input('Valor (R$)', min_value=0.0, step=0.01, format='%.2f')
    tipo_input = st.selectbox('Tipo', ['despesa', 'receita'])
    grupo_input = st.selectbox('Grupo', sorted(transacoes['grupo'].unique()))
    categoria_input = st.selectbox('Categoria', sorted(transacoes['categoria'].unique()))
    observacao_input = st.text_input('Observação (opcional)')
    
    salvar = st.form_submit_button('Salvar')

if salvar:
    nova_linha = {
        'data': data_input,
        'descricao': descricao_input,
        'valor': valor_input,
        'tipo': tipo_input,
        'categoria': categoria_input,
        'grupo': grupo_input,
        'observacao': observacao_input
    }
    novo_df = pd.DataFrame([nova_linha])
    novo_df.to_csv('dados/transacoes.csv', mode='a', header=False, index=False)
    st.sidebar.success('Gasto salvo com sucesso!')

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
        x=por_mes.index.astype(str),
        y=por_mes.values,
        labels={'x': 'Mês', 'y': 'Total (R$)'},
        color=por_mes.values,
        color_continuous_scale='RdBu'
    )
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)


st.markdown('---')
st.subheader('🧠 Resumo do Mês')


mes_recente = despesas[despesas['data'] == despesas['data'].max()]['data'].dt.to_period('M').iloc[0]
despesas_mes = despesas[despesas['data'].dt.to_period('M') == mes_recente]
receitas_mes = receitas[receitas['data'].dt.to_period('M') == mes_recente]

total_desp_mes = despesas_mes['valor'].sum()
total_rec_mes = receitas_mes['valor'].sum()
saldo_mes = total_rec_mes - total_desp_mes

maior_categoria = despesas_mes.groupby('categoria')['valor'].sum().idxmax()
maior_valor = despesas_mes.groupby('categoria')['valor'].sum().max()

gastos_opcionais = despesas_mes[despesas_mes['categoria'].isin(['Lazer', 'Futilidades'])]['valor'].sum()
perc_opcional = (gastos_opcionais / total_rec_mes * 100) if total_rec_mes > 0 else 0

meses = despesas.groupby(despesas['data'].dt.to_period('M'))['valor'].sum()
if len(meses) >= 2:
    mes_anterior = meses.iloc[-2]
    variacao = ((total_desp_mes - mes_anterior) / mes_anterior * 100) if mes_anterior > 0 else 0
else:
    variacao = 0


# Histórico comparativo
st.markdown('---')
st.subheader('📅 Histórico Mensal')

historico = despesas.groupby(despesas['data'].dt.to_period('M'))['valor'].sum().reset_index()
historico.columns = ['mes', 'total']
historico['mes'] = historico['mes'].astype(str)
media = historico['total'].mean()
historico['status'] = historico['total'].apply(
    lambda x: '🟢 Abaixo da média' if x < media else '🔴 Acima da média'
)
historico['média'] = media.round(2)
historico['total'] = historico['total'].round(2)
historico.columns = ['Mês', 'Total (R$)', 'Status', 'Média (R$)']

st.dataframe(historico, use_container_width=True, hide_index=True)

resumo = []

resumo.append(f"📊 **Seu maior gasto foi {maior_categoria}** com R$ {maior_valor:.2f}.")

if perc_opcional > 20:
    resumo.append(f"⚠️ **Lazer e Futilidades** consumiram {perc_opcional:.1f}% da sua renda. Tente reduzir para abaixo de 20% no próximo mês.")

if saldo_mes < 0:
    resumo.append(f"🚨 **Atenção!** Seu saldo ficou negativo em R$ {abs(saldo_mes):.2f}. Revise seus gastos urgentemente.")

if variacao > 0 and len(meses) >= 2:
    resumo.append(f"📈 Você gastou **{variacao:.1f}% a mais** que o mês anterior. Tente melhorar no próximo mês.")
elif variacao < 0 and len(meses) >= 2:
    resumo.append(f"📉 Ótimo! Você gastou **{abs(variacao):.1f}% a menos** que o mês anterior.")

perc_saldo = (saldo_mes / total_rec_mes * 100) if total_rec_mes > 0 else 0
if perc_saldo > 30:
    resumo.append(f"✅ **Parabéns!** Você guardou {perc_saldo:.1f}% da sua renda. Continue assim!")

for linha in resumo:
    st.markdown(linha)