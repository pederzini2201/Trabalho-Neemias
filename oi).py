import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
