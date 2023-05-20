# -*- coding: utf-8 -*-
"""
Created on Sat May 20 10:53:44 2023

@author: rober
"""

import numpy as np
import matplotlib.pyplot as plt

# Definir parâmetros do sinal
f1 = 5  # Frequência do primeiro sinal
f2 = 16   # Frequência do segundo sinal
amplitude1 = 1.5  # Amplitude do primeiro sinal
amplitude2 = 0.5  # Amplitude do segundo sinal

# Definir tempo
t = np.linspace(0, 1, 1000)

# Gerar os sinais
sinal1 = amplitude1 * np.sin(2 * np.pi * f1 * t)
sinal2 = amplitude2 * np.sin(2 * np.pi * f2 * t)

# Sinal resultante da mistura
sinal_resultante = sinal1 + sinal2

# Calcular o espectrograma
plt.specgram(sinal_resultante, NFFT=16, Fs=2, noverlap=2)

# Configurar rótulos dos eixos
plt.xlabel('Tempo')
plt.ylabel('Frequência')

# Exibir o espectrograma
plt.show()

plt.plot(t,sinal_resultante)
plt.show()
