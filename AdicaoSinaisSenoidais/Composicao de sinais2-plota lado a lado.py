# -*- coding: utf-8 -*-
"""
Created on Sat May 20 08:34:46 2023

@author: rober
"""

import numpy as np
import matplotlib.pyplot as plt

# Vetor de pares [frequencia, amplitude]
vetor = [[2, 7], [3, 5], [5, 8], [25, 1.5], [60, 1]]

# Parâmetros de tempo
tempo = np.linspace(0, 1, 1000)  # Intervalo de tempo de 0 a 1

# Plotar as funções de amplitude em função do tempo para cada frequência desejada

fig, axs = plt.subplots(len(vetor)+1, 1, figsize=(8, 32))

# Sinal resultante
sinal_resultante = np.zeros_like(tempo)

i=0
for freq, amp in vetor:    
    amplitude = amp * np.sin(2 * np.pi * freq * tempo)
    axs[i].plot(tempo, amplitude, color='b')
    axs[i].set_title(f'Frequência {freq}')
    axs[i].set_xlabel('Tempo')
    axs[i].set_ylabel('Amplitude') 
    sinal_resultante += amplitude
    if(i==4):
        axs[i+1].plot(tempo, sinal_resultante, color='b')
        axs[i+1].set_title('Frequência resultante')
        axs[i+1].set_xlabel('Tempo')
        axs[i+1].set_ylabel('Amplitude')
    i+=1

#plt.tight_layout()
plt.show()
