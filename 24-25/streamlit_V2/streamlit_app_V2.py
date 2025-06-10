import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Função para carregar os dados diretamente do GitHub
@st.cache_data
def carregar_dados_github():
    base_url = "https://raw.githubusercontent.com/ohallao/MoneyBall_Big5_Europe/main/24-25/Output_Cluster/"
    arquivos = [
        "gol_data.csv",
        "Attacking_Midfielder_data.csv",
        "Winger_data.csv",
        "Defensive_Midfielder_data.csv",
        "Defender_data.csv",
        "FullBack_data.csv",
        "striker_data.csv"
    ]

    dfs = []
    for arquivo in arquivos:
        url = base_url + arquivo
        try:
            df = pd.read_csv(url)
            dfs.append(df)
        except Exception as e:
            st.error(f"Erro ao carregar {arquivo}: {e}")

    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        st.warning("Nenhum dado foi carregado.")
        return pd.DataFrame()

# Carregar os dados
df = carregar_dados_github()

# Título do app
st.title("Moneyball Big 5 Europe - Cluster App")

# Verifica se o DataFrame não está vazio
if not df.empty:
    # Exibir amostra dos dados
    st.subheader("Prévia dos Dados")
    st.dataframe(df.head())

    # Filtro por posição
    posicoes = df['Position'].unique().tolist()
    posicao_selecionada = st.selectbox("Selecione a posição:", sorted(posicoes))

    df_filtrado = df[df['Position'] == posicao_selecionada]

    # Filtro por cluster
    clusters = df_filtrado['Cluster'].unique().tolist()
    cluster_selecionado = st.multiselect("Selecione os clusters:", sorted(clusters), default=clusters)

    df_filtrado = df_filtrado[df_filtrado['Cluster'].isin(cluster_selecionado)]

    # Filtro por time (Squad)
    times = df_filtrado['Squad'].unique().tolist()
    time_selecionado = st.multiselect("Filtrar por time:", sorted(times), default=times)
    df_filtrado = df_filtrado[df_filtrado['Squad'].isin(time_selecionado)]

    # Filtro por nacionalidade (Nation)
    nacionalidades = df_filtrado['Nation'].unique().tolist()
    nacionalidade_selecionada = st.multiselect("Filtrar por nacionalidade:", sorted(nacionalidades), default=nacionalidades)
    df_filtrado = df_filtrado[df_filtrado['Nation'].isin(nacionalidade_selecionada)]

    # Gráfico de dispersão interativo
    st.subheader("Gráfico de Dispersão")
    colunas_numericas = df_filtrado.select_dtypes(include=np.number).columns.tolist()
    x_col = st.selectbox("Eixo X:", colunas_numericas)
    y_col = st.selectbox("Eixo Y:", colunas_numericas, index=1 if len(colunas_numericas) > 1 else 0)

    fig = px.scatter(df_filtrado, x=x_col, y=y_col, color='Cluster', hover_data=['Player', 'Squad', 'Nation'])
    st.plotly_chart(fig)
else:
    st.warning("Não foi possível carregar os dados.")
