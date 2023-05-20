# -*- coding: utf-8 -*-
"""
Spyder Editor

Demonstração de sinais no domínio do tempo e no da frequência

Vídeos base (dentre outros):  
    
    https://www.youtube.com/watch?v=1-i4byj3MqI
    
    https://www.youtube.com/watch?v=ev0juGwUz78
    
    https://www.youtube.com/watch?v=tMWPa-cikZ8
    
    https://www.youtube.com/watch?v=v_dhWDZs0KQ
    
    https://www.youtube.com/watch?v=mgXSevZmjPc
    
    https://www.youtube.com/playlist?list=PLuw79CJhBbBl5gESZG_6Un9ZmzK13MgGD

"""
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from scipy.io import wavfile # para gravar o arquivo wav de saída

# Gerar a onda senoidal
def gerarSinalSenoidal(tempos, frequencia, amplitude):
    return amplitude * np.sin(2.0 * np.pi * frequencia * tempos)

#
# Normalizar o sinal entre -1 e 1
def normalizar_sinal(signal):
    max_val = np.max(signal)
    min_val = np.min(signal)
    amplitude = max_val - min_val    
    normalized_signal = ((signal - min_val) / amplitude) * 2 - 1
    return normalized_signal

# normalizar entre 0 e o valor máximo após normalizado (no caso, 20)
def normalizarSinal_meiaOnda(signal, maxAposNorm):
    max_val = np.max(signal)
    min_val = np.min(signal)
    amplitude = max_val - min_val
    
    normalized_signal = ((signal - min_val) / amplitude) * maxAposNorm
    return normalized_signal


frequenciaAmostragem=22050  # Amostragem: 22050 amostras por segundo (22050 hertz)
periodoAmostragem=1/frequenciaAmostragem  # algum submúltiplo de tempo em segundos
tempos=np.arange(0.0, 1.0, periodoAmostragem, dtype=float) # constroi o vetor de tempos

# Vetor de parametros ([frequencia, amplitude]), para um loop que irá somar 5 sinais escolhidos aleatoriamente
# Se quiser usar o primeiro, comente o segundo abaixo
vetorFreqsAmplts=[[2,7],[3,5],[5,8],[25,1.5]]          # Simula um sinal de áudio
vetorFreqsAmplts=[[2,7],[3,5],[5,8],[25,1.5],[60,1]]   # Simula o sinal acima, acrescido de sinal de ruído de 60hz


print('Os sinais foram amostrados em 22050hz')
print('Como estamos trabalhando com apenas 1 segundo, então, cada sinal contém 22050 amostras')
print('Esse, portanto, é o tamanho do vetor de tempo (eixo da variável independente tempo)')

sinalResultante=np.zeros_like(tempos)  # gera um vetor de valores nulos igual ao shape do vetor de amostras (domínio do tempo)
for i in range(len(vetorFreqsAmplts)):
    frequencia, amplitude = vetorFreqsAmplts[i]
    sinal=gerarSinalSenoidal(tempos, frequencia, amplitude)
    
    plt.figure()
    plt.plot(tempos, sinal)
    #plt.show()
    sinalResultante += sinal
    plt.plot(tempos, sinalResultante)
    plt.title(f"Sinal anterior + sinal (azul) de amplitude {amplitude}, frequência: {frequencia} (sinal resultante na cor laranja)")
    plt.show()


maxIntensidade=np.max(sinalResultante)
print('maxIntensidade',maxIntensidade)

# Normalizar o sinal resultante entre -1 e 1
sinalResultante = normalizar_sinal(sinalResultante)

plt.plot(tempos, sinalResultante)
plt.title("Sinal resultante:")
plt.show()

########################
## Transformada de Fourier para encontrar o vetor de frequencias
N=len(sinalResultante)
print("Tamanho N do sinal:", N, "amostras")

# Eixo da variável independente do domínio das frequências (eixo horizontal)
frequencias=np.fft.fftfreq(N, periodoAmostragem)

# Eixo vertical (intensidades do sinal)
intensidadesSinalDomFreq=np.fft.fft(sinalResultante)
intensidadesSinalDomFreq=np.abs(intensidadesSinalDomFreq)

# Normalizar o eixo das intensidades entre 0 e 1, para ficar igual às intensidades do dominio do tempo
#intensidadesSinalDomFreq=normalizarSinal_meiaOnda(intensidadesSinalDomFreq, maxIntensidade)
intensidadesSinalDomFreq=normalizarSinal_meiaOnda(intensidadesSinalDomFreq, 1.0)

plt.figure()
plt.plot(frequencias, intensidadesSinalDomFreq)
plt.title("Sinal resultante (visto no domínio da frequência):")
plt.xlim(-100, 100)  # Restringe o eixo horizontal até 100
plt.show()

# Dá um zoom no gráfico
print("Zoom no eixo horizontal, para ver somente os valores > 0")
plt.figure()
plt.plot(frequencias[frequencias>0], intensidadesSinalDomFreq[frequencias > 0])
plt.title("Sinal resultante (visto no domínio da frequência):")
plt.xlim(0, 100)  # Restringe o eixo horizontal até 100
plt.show()

## Eliminar a frequencia de 60hz

# Definir a frequência de corte em Hz
cutoff_frequency = 60

# Calcular o índice correspondente à frequência de corte
cutoff_index = int(cutoff_frequency / (frequenciaAmostragem / len(intensidadesSinalDomFreq)))

# Criar uma cópia do espectro de frequências
intensidadesSinalDomFreq_corte = intensidadesSinalDomFreq.copy()

# Zerar a intensidade da frequência de corte e sua simétrica
intensidadesSinalDomFreq_corte[cutoff_index] = 0
intensidadesSinalDomFreq_corte[-cutoff_index] = 0

# Realizar a transformação inversa de Fourier
sinalResultanteIfft = np.fft.ifft(intensidadesSinalDomFreq_corte)

# Converter o sinal resultante para o tipo de dado adequado
sinalResultanteIfft = np.real(sinalResultanteIfft)

print(sinalResultanteIfft)

plt.figure()
plt.plot(tempos, sinalResultanteIfft)
plt.title("Sinal resultante depois do corte da frequencia de 60hz:")
#plt.xlim(-100, 100)  # Restringe o eixo horizontal até 100
plt.show()

# Gravar o sinalResultante em um arquivo WAV
wavfile.write('sinalResultante_iFFT.wav', frequenciaAmostragem, sinalResultanteIfft)


# Plotar os eixos em um gráfico 3D

# PAREI AQUI 
# O código abaixo está com problemas.
# Acredito que tenha de fazer alguma manipulação algébrica (Álgebra Linear)


# Configurar figura e eixos 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotar o gráfico 3D
ax.plot(tempos, frequencias, intensidadesSinalDomFreq)

# Configurar rótulos dos eixos
ax.set_xlabel('Tempo (s)')
ax.set_ylabel('Frequência (Hz)')
ax.set_zlabel('Amplitude')

# Exibir o gráfico 3D
plt.show()

# Dados de entrada
x = tempos
y = frequencias
z = intensidadesSinalDomFreq

print(x.shape)
print(y.shape)
print(sinalResultante.shape)
print(intensidadesSinalDomFreq.shape)

# Configurar figura e eixos 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotar os vetores
ax.quiver(0, 0, 0, x, y, z, length=1)

# Configurar limites dos eixos
ax.set_xlim([0, np.max(x) + 1])
ax.set_ylim([0, np.max(y) + 1])
ax.set_zlim([0, np.max(z) + 1])

# Configurar rótulos dos eixos
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Ativar interação do mouse
ax.mouse_init()

# Exibir o gráfico 3D
plt.show()

# Gravar o sinalResultante em um arquivo WAV
wavfile.write('sinalResultante_com_ruido.wav', frequenciaAmostragem, sinalResultante)