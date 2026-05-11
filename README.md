# 💰 Dashboard Financeiro

Dashboard interativo para controle de finanças pessoais, desenvolvido com Python, Pandas, Plotly e Streamlit.
---

## 📸 Preview

<img width="1919" height="872" alt="Captura de tela 2026-05-11 104816" src="https://github.com/user-attachments/assets/6539cbab-2778-4c3a-ad87-4a468a3102c4" />

<img width="1917" height="750" alt="Captura de tela 2026-05-11 104856" src="https://github.com/user-attachments/assets/b6c0986a-354b-4ecf-87eb-3f5942ac4b87" />



> *Dashboard com tema escuro, gráficos interativos e análise automática do mês*

---

## 🚀 Funcionalidades

- Visualização de receitas, despesas e saldo total
- Gráfico de gastos por categoria (donut interativo)
- Gráfico de gastos por mês com gradiente de cor
- Filtro interativo por categoria na sidebar
- Formulário para adicionar novos gastos em tempo real
- Resumo inteligente com análise automática do mês
- Histórico mensal comparativo com média dos gastos
- Indicadores visuais de meses acima/abaixo da média

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.13 | Linguagem principal |
| Pandas | Leitura e análise dos dados |
| Plotly | Gráficos interativos |
| Streamlit | Interface web do dashboard |

---

## 📂 Estrutura do Projeto

Dashboard/
├── dados/
│   ├── transacoes.csv      ← transações financeiras
│   └── categorias.csv      ← categorias disponíveis
├── dashboard.py            ← aplicação principal
├── analise.py              ← scripts de análise
├── requirements.txt        ← dependências do projeto
└── README.md

---

## ▶️ Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/GMonteiro2/Dashboard.git
cd Dashboard

# Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Rode o dashboard
streamlit run dashboard.py
```

---

## 📊 Sobre os dados

O projeto utiliza dados fictícios para demonstração — 6 meses de transações com variações realistas de gastos e receitas. Para uso pessoal basta substituir o arquivo `dados/transacoes.csv` mantendo a mesma estrutura de colunas.

---

## 👨‍💻 Autor

Feito com 💚 por **Gabriel Monteiro**  
[![GitHub](https://img.shields.io/badge/GitHub-GMonteiro2-black?logo=github)](https://github.com/GMonteiro2)
