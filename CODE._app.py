import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuração da página
st.set_page_config(page_title="📊 Dashboard Moderno", layout="wide")

# --- INÍCIO DO ESTILO CSS CUSTOMIZADO ---
# ATENÇÃO: Se o erro "removeChild" persistir no deploy,
# comente temporariamente esta seção inteira de st.markdown para testar.
# Conflitos no CSS são uma causa comum desse erro no Streamlit Cloud.
st.markdown("""
    <style>
    body, [class*="stApp"] {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sidebar com fundo cinza escuro e texto branco */
    section[data-testid="stSidebar"] {
        background-color: #2c2c2c;
        color: #ffffff;
    }
    /* Cor dos textos nas métricas */
    div[data-testid="metric-container"] {
        color: white !important;
    }
    /* Estilizar botão de download */
    button[kind="primary"] {
        color: white !important;
        background-color: #444 !important;
        border: 1px solid white !important;
    }
    /* Componentes visuais */
    .stDataFrame, .stMetric, .stPlotlyChart {
        background-color: #1e1e1e;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    /* Fundo cinza escuro para tabelas e texto branco */
    table {
        background-color: #2f2f2f !important;
        color: white !important;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #444 !important;
        padding: 8px;
        text-align: left;
        color: white !important;
    }
    /* Cores do cabeçalho da tabela */
    thead tr {
        background-color: #3b3b3b;
        color: white !important;
    }
    /* Ajuste para a coluna P.da Semana com cores */
    span {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
# --- FIM DO ESTILO CSS CUSTOMIZADO ---

plotly_template = "plotly_dark"

def to_excel(df):
    output = BytesIO()
    # Usar engine='xlsxwriter' é importante para o Streamlit Cloud, pois 'openpyxl' pode ter dependências extras.
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    return output.getvalue()

# Dados simulados
df = pd.DataFrame({
    'Data': pd.date_range(start='2025-01-01', periods=30, freq='D'),
    'Usuário': [f'user{i%5+1}' for i in range(30)],
    'Logins': [i*3 % 10 + 1 for i in range(30)],
    'Faltas': [i % 2 for i in range(30)],
    'Presenças': [1 if i % 2 == 0 else 0 for i in range(30)],
    'Nota': [round(7 + (i % 3) + (i % 2) * 0.5, 1) for i in range(30)]
})

# ---------------- Sidebar ----------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Logo_2023.png", width=150)
st.sidebar.markdown("---")
st.sidebar.image("https://randomuser.me/api/portraits/men/32.jpg", width=80)
st.sidebar.markdown("**Bem-vindo, Gabriel!**", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Filtros
st.sidebar.header("🔎 Filtros")
# Usar um set para unique values pode ser um pouco mais eficiente para listas grandes, mas .unique() já funciona bem
usuarios = st.sidebar.multiselect("👤 Usuários", sorted(df['Usuário'].unique()), default=sorted(df['Usuário'].unique()))
date_range = st.sidebar.date_input("📅 Período", [df['Data'].min(), df['Data'].max()])

inicio, fim = date_range
filtro_df = df[
    (df['Usuário'].isin(usuarios)) &
    (df['Data'] >= pd.to_datetime(inicio)) &
    (df['Data'] <= pd.to_datetime(fim))
]

# ---------------- Título e Métricas ----------------
st.title("📈 Dashboard de Logins e Desempenho")

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Usuários Únicos", filtro_df['Usuário'].nunique())
col2.metric("🔢 Total de Logins", filtro_df['Logins'].sum())
col3.metric("❌ Faltas Totais", filtro_df['Faltas'].sum())
col4.metric("📚 Média das Notas", round(filtro_df['Nota'].mean(), 2))

st.markdown("""<br></br>""", unsafe_allow_html=True)

# ---------------- Gráficos ----------------
col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Logins por Dia")
    fig1 = px.line(filtro_df, x='Data', y='Logins', markers=True, template=plotly_template)
    fig1.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🎓 Notas Médias por Usuário")
    nota_media = filtro_df.groupby('Usuário')['Nota'].mean().reset_index()
    fig2 = px.bar(nota_media, x='Usuário', y='Nota', template=plotly_template)
    fig2.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("✅ Distribuição de Presenças")
    pres_df = filtro_df.groupby('Usuário')['Presenças'].sum().reset_index()
    fig3 = px.pie(pres_df, values='Presenças', names='Usuário', template=plotly_template)
    fig3.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📊 Radar de Logins por Dia da Semana")
    radar_df = filtro_df.copy()
    radar_df['Dia'] = radar_df['Data'].dt.day_name()
    # Ordem dos dias para o gráfico radar (se desejar uma ordem específica)
    # day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # radar_df['Dia'] = pd.Categorical(radar_df['Dia'], categories=day_order, ordered=True)

    radar_data = radar_df.groupby(['Dia', 'Usuário'])['Logins'].sum().unstack().fillna(0)
    fig4 = px.line_polar(
        radar_data.reset_index(),
        r=radar_data.sum(axis=1),
        theta=radar_data.index,
        line_close=True,
        template=plotly_template
    )
    fig4.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
    st.plotly_chart(fig4, use_container_width=True)

# ---------------- Tabela com coluna P.da Semana ----------------
st.subheader("📋 Tabela de Dados Detalhados")

def formatar_presenca(row):
    return f"<span style='color: green;'>✔ Presente</span>" if row['Presenças'] == 1 else f"<span style='color: red;'>✘ Falta</span>"

filtro_df_formatado = filtro_df.copy()
filtro_df_formatado['P.da Semana'] = filtro_df_formatado.apply(formatar_presenca, axis=1)

# Usar st.markdown para exibir HTML de dataframe
st.markdown(
    filtro_df_formatado.to_html(escape=False, index=False),
    unsafe_allow_html=True
)

# Botão de download
excel_data = to_excel(filtro_df)
st.download_button(
    label="⬇️ Baixar Excel",
    data=excel_data,
    file_name='dados_logins_completos.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

# ---------------- Gráfico redondo resumo geral ----------------
st.subheader("📊 Resumo Geral da Turma")
resumo_df = pd.DataFrame({
    'Categoria': ['Presenças', 'Faltas', 'Nota Média'],
    'Valor': [
        filtro_df['Presenças'].sum(),
        filtro_df['Faltas'].sum(),
        filtro_df['Nota'].mean()
    ]
})
fig5 = px.pie(
    resumo_df,
    values='Valor',
    names='Categoria',
    title="Participação e Desempenho",
    template=plotly_template,
    hole=0.3
)
fig5.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')
st.plotly_chart(fig5, use_container_width=True)
