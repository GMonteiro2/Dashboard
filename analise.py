import pandas as pd


transacoes = pd.read_csv('dados/transacoes.csv')
transacoes['data'] = pd.to_datetime(transacoes['data'])


despesas = transacoes[transacoes['tipo'] == 'despesa']
receitas = transacoes[transacoes['tipo'] == 'receita']


total_despesas = despesas['valor'].sum()
total_receitas = receitas['valor'].sum()

por_categoria = despesas.groupby('categoria')['valor'].sum()
por_mes = despesas.groupby(despesas['data'].dt.to_period('M'))['valor'].sum()


print(por_mes)
print(por_categoria)
print(f'Total de despesas: R$ {total_despesas}')
print(f'Total de receitas: R$ {total_receitas}') 
print(f'Saldo final: R$ {total_receitas - total_despesas}')
print(por_categoria.sort_values(ascending=False))

import plotly.express as px

fig = px.pie(
    values=por_categoria.values,
    names=por_categoria.index,
    title='Gastos por Categoria'
)

fig2 = px.bar(
    x=['Janeiro', 'Fevereiro'],
    y=por_mes.values,
    title='Gastos por Mês',
    labels={'x': 'Mês', 'y': 'Total (R$)'}
)

fig2.show()