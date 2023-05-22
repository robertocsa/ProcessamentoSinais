# -*- coding: utf-8 -*-
"""
Created on Sun May 21 18:53:24 2023

@author: rober
"""

import numpy as np
import soundfile as sf
import librosa
#from scipy.fftpack import dct
from scipy.linalg import eigh
import pandas as pd


sr=22050 #Frequencia de amostragem

def calculate_covariance_matrix(*arrays):
    n = arrays[0].shape[0]
    k = len(arrays)
    covariance_matrix = np.zeros((k, k))
    
    for i in range(k):
        for j in range(i, k):
            covariance_matrix[i, j] = np.sum((arrays[i] - np.mean(arrays[i])) * (arrays[j] - np.mean(arrays[j]))) / (n - 1)
            covariance_matrix[j, i] = covariance_matrix[i, j]
    
    return covariance_matrix


# Função para normalizar um vetor entre -1 e 1

def normalizar(vetor):
    #print(vetor.shape)
    vetorShape0=vetor.shape[0]
    if (vetorShape0 == 0):
        vetor_normalizado=None
    else:
        max_val = np.max(vetor)
        min_val = np.min(vetor)
        
        if max_val == min_val:
            # Caso especial: valores mínimo e máximo iguais
            # Retornar o vetor original ou atribuir um valor fixo
            #vetor_normalizado = vetor  
            vetor_normalizado = None
        else:
            # Normalizar o vetor entre -1 e 1
            vetor_normalizado = 2 * (vetor - min_val) / (max_val - min_val) - 1
    
    return vetor_normalizado


def encurtarSinal(sinal, duracaoDesejada, duracaoAtual):

    # Calcular o número de amostras correspondentes a ? segundos
    # duração_desejada = ? # em segundos
    n_amostras_desejadas = int(duracaoDesejada * sr)
    print("Qtde de amostras desejadas:", n_amostras_desejadas)             
    
    # encurtamento de tempo do sinal
    escalaReducao = duracaoAtual / duracaoDesejada
    sinalEncurtado = librosa.effects.time_stretch(y=sinal, rate=escalaReducao)

    # Salvar o sinal encurtado para um novo arquivo wav
    sf.write('shortened_audio.wav', sinalEncurtado, sr, 'PCM_16')
        
    # Verificar a nova duração do sinal encurtado
    duracaoEncurtada = len(sinalEncurtado) / sr
    print("Duração do sinal encurtado:", duracaoEncurtada, "segundos")
    return sinalEncurtado

nomeArquivos=['..\\Audios Exemplos\\esse1.wav','..\\Audios Exemplos\\esse2.wav']
# Loop externo
tamSinal=0
for i in range(len(nomeArquivos)):
    nomeArquivo=nomeArquivos[i]
    # Abertura dos arquivos WAV
    wav_data, sr = sf.read(nomeArquivo)

    # Carregando os sinais
    if i == 0:
        sinal1 = wav_data
        tamSinal1 = len(sinal1)
        tamSinal=tamSinal1
    else:
        sinal2 = wav_data
        tamSinal2 = len(sinal2)
        tamSinal=tamSinal2

duracaoSinal1=1/sr*tamSinal1
duracaoSinal2=1/sr*tamSinal2
print("Duração dos sinais:", duracaoSinal1,duracaoSinal2)

# Encurtar o sinal de maior tamanho:
duracaoSinal=0.0
if (tamSinal1 > tamSinal2):    
    sinal1 = encurtarSinal(sinal1, duracaoSinal2, duracaoSinal1)
    duracaoSinal=duracaoSinal2
else:
    sinal2 = encurtarSinal(sinal2, duracaoSinal1, duracaoSinal2)
    duracaoSinal=duracaoSinal1
    

# Cálculo do valor de N
N = int(np.sqrt(tamSinal))

print("qtde N de janelas dos sinais:", N)


# Divisão em janelas de tempo e frequência
n = N  # Número de janelas de tempo e frequência (mesmo valor neste caso)
janela_tempo = np.linspace(0, duracaoSinal, n)
janela_frequencia = np.linspace(20, 20001, n)

# Matrizes para armazenar os resultados
media_sinal1 = np.zeros((n, n))
desvio_padrao_sinal1 = np.zeros((n, n))
variancia_sinal1 = np.zeros((n, n))
melfcc_sinal1 = np.zeros((n, n))
fo_sinal1 = np.zeros((n, n))

media_sinal2 = np.zeros((n, n))
desvio_padrao_sinal2 = np.zeros((n, n))
variancia_sinal2 = np.zeros((n, n))
melfcc_sinal2 = np.zeros((n, n))
fo_sinal2 = np.zeros((n, n))

print("Shapes:")
print(janela_frequencia.shape, janela_tempo.shape)

# Loop para calcular os parâmetros em cada janela de tempo
for i, tempo_inicial in enumerate(janela_tempo):
    n_janela_tempo_inicial=int(tempo_inicial*sr)
    print(i)
    #if (i>2):
     #   break
    for j, frequencia in enumerate(janela_frequencia):
        # Obtendo a janela de tempo e frequência        
        janela_sinal1 = sinal1[n_janela_tempo_inicial:n_janela_tempo_inicial+n]
        janela_sinal2 = sinal2[n_janela_tempo_inicial:n_janela_tempo_inicial+n]

        # Normalizando o sinal1 entre -1 e 1
        janela_sinal1_norm = normalizar(janela_sinal1)
        # Normalizando o sinal2 entre -1 e 1
        janela_sinal2_norm = normalizar(janela_sinal2)
        
        if (janela_sinal1_norm is not None and janela_sinal2_norm is not None):
            # Cálculo dos parâmetros do sinal1
            
            media_sinal1[i, j] = janela_sinal1_norm.mean()
            desvio_padrao_sinal1[i, j] = np.std(janela_sinal1_norm)
            variancia_sinal1[i, j] = np.var(janela_sinal1_norm)
            melfcc_sinal1[i, j] = np.mean(librosa.feature.mfcc(y=janela_sinal1, sr=sr, n_fft=32, hop_length=16))
            fo_sinal1[i, j] = np.mean(librosa.yin(y=janela_sinal1, fmin=20, fmax=20000, sr=sr, frame_length=16, hop_length=4))       
        
        if (janela_sinal1_norm is not None and janela_sinal2_norm is not None):
            # Cálculo dos parâmetros do sinal2
            media_sinal2[i, j] = janela_sinal2_norm.mean()
            desvio_padrao_sinal2[i, j] = np.std(janela_sinal2_norm)
            variancia_sinal2[i, j] = np.var(janela_sinal2_norm)
            melfcc_sinal2[i, j] = np.mean(librosa.feature.mfcc(y=janela_sinal2, sr=sr, n_fft=32, hop_length=16))
            fo_sinal2[i, j] = np.mean(librosa.yin(y=janela_sinal2, fmin=20, fmax=20000, sr=sr, frame_length=16, hop_length=4))

# Cálculo da matriz de covariâncias
print(media_sinal1.shape, desvio_padrao_sinal1.shape, variancia_sinal1.shape, melfcc_sinal1.shape, fo_sinal1.shape)

covariance_matrix_sinal1 = calculate_covariance_matrix(media_sinal1, desvio_padrao_sinal1, variancia_sinal1, melfcc_sinal1, fo_sinal1)
covariance_matrix_sinal2 = calculate_covariance_matrix(media_sinal2, desvio_padrao_sinal2, variancia_sinal2, melfcc_sinal2, fo_sinal2)


# Cálculo do PCA
_, pca_sinal1 = eigh(covariance_matrix_sinal1)
_, pca_sinal2 = eigh(covariance_matrix_sinal2)

# Resultados
print("Matriz de Covariâncias Sinal 1:")
print(covariance_matrix_sinal1)
print()

print("PCA Sinal 1:")
print(pca_sinal1)
print()

print("Matriz de Covariâncias Sinal 2:")
print(covariance_matrix_sinal2)
print()

print("PCA Sinal 2:")
print(pca_sinal2)

# Criar DataFrame com os resultados
df_sinal1 = pd.DataFrame({
    'Média': media_sinal1.flatten(),
    'Desvio Padrão': desvio_padrao_sinal1.flatten(),
    'Variância': variancia_sinal1.flatten(),
    'MELFCC': melfcc_sinal1.flatten(),
    'Fo': fo_sinal1.flatten()
})

df_sinal2 = pd.DataFrame({
    'Média': media_sinal2.flatten(),
    'Desvio Padrão': desvio_padrao_sinal2.flatten(),
    'Variância': variancia_sinal2.flatten(),
    'MELFCC': melfcc_sinal2.flatten(),
    'Fo': fo_sinal2.flatten()
})

# Criação dos DataFrames restantes
df_covariance_sinal1 = pd.DataFrame(covariance_matrix_sinal1)
df_pca_sinal1 = pd.DataFrame(pca_sinal1)
df_covariance_sinal2 = pd.DataFrame(covariance_matrix_sinal2)
df_pca_sinal2 = pd.DataFrame(pca_sinal2)

# Exportação para Excel
#writer = pd.ExcelWriter('resultados.xlsx', engine='xlsxwriter')

# Salvar os DataFrames em um arquivo Excel
with pd.ExcelWriter('resultados.xlsx') as writer:
    df_sinal1.to_excel(writer, sheet_name='Sinal 1', index=False)
    df_sinal2.to_excel(writer, sheet_name='Sinal 2', index=False)
    df_covariance_sinal1.to_excel(writer, sheet_name='Covariance Sinal 1')
    df_pca_sinal1.to_excel(writer, sheet_name='PCA Sinal 1')
    df_covariance_sinal2.to_excel(writer, sheet_name='Covariance Sinal 2')
    df_pca_sinal2.to_excel(writer, sheet_name='PCA Sinal 2')
    
#writer.save()

print("Resultados exportados para o arquivo resultados.xlsx.")