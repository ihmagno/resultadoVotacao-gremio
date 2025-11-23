import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
import base64

escopo = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credenciais = ServiceAccountCredentials.from_json_keyfile_name('projetovotacao2.json', escopo)
client = gspread.authorize(credenciais)

# Função de carregamento dos dados SEM cache (para sempre pegar atualizados)
def carregar_dados():
    planilha = client.open('Resultado da Votação - Grêmio').sheet1
    dados = planilha.get_all_records()
    return pd.DataFrame(dados)

#Configuração da pagina - adicionando uma imagem de fundo 
def pegar_imagem(imagem):
    with open(imagem, 'rb') as img:
        data = img.read()
    return base64.b64encode(data).decode()

# Página
st.set_page_config(page_title="Votação Grêmio", layout="centered")
st.title("📊 Resultado da Votação - Grêmio Estudantil")

imagem_fundo = pegar_imagem('Fundo Gremio.png')

bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{imagem_fundo}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

</style>
"""
st.markdown(bg_img, unsafe_allow_html=True)

# Simula atualização automática a cada 60 segundos 
refresh_interval = 60  

# JavaScript para autoatualizar a página
st.markdown(f"""
    <meta http-equiv="refresh" content="{refresh_interval}">
    <p style="text-align:center; color: gray;">🔁 A página se atualiza automaticamente a cada {refresh_interval} segundos.</p>
""", unsafe_allow_html=True)

# Carregar os dados
df = carregar_dados()

# Gráfico de Pizza
if "Vote na Chapa" in df.columns:
    votos_contados = df["Vote na Chapa"].value_counts().sort_index()

   #st.subheader("🥧 Distribuição de Votos")
    fig, ax = plt.subplots(facecolor='none')
    ax.pie(
        votos_contados,
        labels=votos_contados.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Paired.colors, 
        textprops={'fontsize': 10, 'fontweight': 'bold'} 
    )
    ax.axis('equal')
    st.pyplot(fig)
else:
    st.warning("Coluna 'Vote na Chapa' não encontrada. Verifique o nome na planilha.")

