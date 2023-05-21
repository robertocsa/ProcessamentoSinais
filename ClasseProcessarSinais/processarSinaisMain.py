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

#Gráfico do sinal
processador.apresentaSinalSimples(sinal)

# Calcular tempo, frequência e intensidade
resultados = processador.calcularTempoFrequenciaIntensidade(sinal)
resultados=np.array(resultados)

print(resultados.shape)

# Apresentar o sinal em um gráfico 3D
processador.apresentarSinalEmGrafico3D(sinal)

# Apresentar histograma2D do sinal
processador.apresentarSinalEmHistograma2D(sinal)