import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as snss

def gerar_dados():
    np.random.seed(42)
    usuarios = ['Ana', 'Lucas', 'Marcos', 'Julia', 'Maria', 'Carlos', 'Pedro', 'Lazaros', 'Gabriel', 'Carla']
    idades = np.random.randint(18, 45, 10)
    generos = np.random.choice(['Masculino', 'Feminino'], 10)
    frequencia_checkin = np.random.randint(1, 5, 10)

   dados = pd.DataFrame({
        'Usuário': usuarios,
        'Idade': idades,
        'Gênero': generos,
        'Frequência de Check-in (semana)': frequencia_checkin
        })

    return dados
def mostrar_dashboard():
    st.title("Dashboard de Check-ins na Academia")
    st.write("Visualize os check-ins e os metadados dos usuários da academia.")
    
    dados = gerar_dados()
    st.subheader("Dados de Usuários")
    st.dataframe(dados)
    
    st.subheader("Frequência de Check-ins por Semana")
    fig, ax = plt.subplots()
    sns.countplot(x='Frequência de Check-in (semana)', data=dados, ax=ax)
    ax.set_title('Distribuição da Frequência de Check-ins por Usuário')
    st.pyplot(fig)

    st.subheader("Distribuição por Gênero")
    fig2, ax2 = plt.subplots()
    sns.countplot(x='Gênero', hue='Frequência de Check-in (semana)', data=dados, ax=ax2)
    ax2.set_title('Distribuição por Gênero e Frequência de Check-ins')
    st.pyplot(fig2)

    

