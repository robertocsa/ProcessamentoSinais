# -*- coding: utf-8 -*-
"""
Created on Sat May 20 18:51:37 2023

@author: rober
"""

import ProcessarSinal
import numpy as np

# Criar um objeto ProcessarSinal
processador = ProcessarSinal.ProcessarSinal()

# Ler o arquivo WAV e obter o sinal
arquivo_wav = "..\\Audios Exemplos\\esse1.wav"
sinal = processador.lerArquivoWav(arquivo_wav)
tamSinal=len(sinal)

#Gráfico do sinal
processador.apresentaSinalSimples(sinal)

# Calcular tempo, frequência e intensidade
resultados = processador.calcularTempoFrequenciaIntensidade(sinal)
resultados=np.array(resultados)
print(resultados.shape)
indice_inicio, tempo_centro, frequencia_predominante, amplitude_media = resultados.T



# Apresentar o sinal em um gráfico 3D
processador.apresentarSinalEmGrafico3D(sinal)


# Apresentar histograma2D do sinal
processador.apresentarSinalEmHistograma2D(sinal)

# Obtem os vetores de contagens e de bordas de um histograma
#serieDados = np.array([1.2, 2.5, 1.8, 3.2, 2.1, 1.5, 2.7, 2.9, 3.5, 3.8])
#serieDados = np.array([1, 2, 1, 3, 2, 4, 3, 0, 1, 3, 4, 0, 0, 4, 4])
#qtde_bins = 2

print(tempo_centro.shape, frequencia_predominante.shape, amplitude_media.shape)

processador.graficoBarras3D(x=tempo_centro, y=frequencia_predominante, z=amplitude_media)

#processador.graficoCalor(x=tempo_centro, y=frequencia_predominante, z=amplitude_media)

# Exemplo de uso da função exportarParaExcel
#vetor1 = np.array([1, 2, 3, 4])
#vetor2 = np.array([5, 6, 7, 8])
#vetor3 = np.array([9, 10, 11, 12])
#vetor4 = np.array([13, 14, 15, 16])
#nomeArq='serieDadosFicticia.xlsx'
#processador.exportarParaExcel(vetor1, vetor2, vetor3, vetor4, nomeArq)
nomeArq='serieDadosAudioEsse1.xlsx'
processador.exportarParaExcel(indice_inicio, tempo_centro, frequencia_predominante, amplitude_media, nomeArq)