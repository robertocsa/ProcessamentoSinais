# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:21:32 2023

@author: rober 
""" 

import numpy as np
import matplotlib.pyplot as plt
import librosa
import pandas as pd

sr=22050  # frequencia de amostragem
###########################
## CLASSE PROCESSAR SINAL
###########################
class ProcessarSinal:
    
    # Abre um arquivo WAV no formato PCM16, 22050hz de amostragem
    def lerArquivoWav(self, nomeCompletoArquivo):
        
        # carregando os arquivos de áudio
        audio, _ = librosa.load(nomeCompletoArquivo, sr=sr)
        tamAudio=len(audio)
        duracao=1/sr*tamAudio
        print(f"Duração do áudio: {duracao :.3f}s, tamanho:{tamAudio} amostras")
        
        return audio
    
    def obterHistogramaSerieDados(self,serieDados, qtde_bins):
        # Calcula o histograma usando np.histogram
        contagens, fronteirasDosBins = np.histogram(serieDados, bins=qtde_bins)
        
        # Retorna os valores dos bins e as contagens correspondentes
        return contagens, fronteirasDosBins   
    
    # Cria o gráfico 2D do sinal
    def apresentaSinalSimples(self, sinal):
        
        N=len(sinal)
        
        # Período de amostragem
        T=1/sr
        print(f"Período de amostragem:{T :0.6f}s")

        # Definir vetor tempo
        t = np.linspace(0, T*N, N)
        

        # Configurar rótulos dos eixos
        plt.xlabel('Tempo')
        plt.ylabel('Frequência')


        plt.plot(t,sinal)
        plt.show()
    
    # Recebe um array de valores float e retorna:
        # indice_inicio (Indice n do início da janela)
        # tempo_centro (centro do tempo na faixa de tempo da janela)
        # frequencia_predominante (frequencia predominante na janela)
        # amplitude_media (amplitude média na janela)
    def calcularTempoFrequenciaIntensidade(self, sinal):
        taxa_amostragem=sr
        # Define a duração da janela, em segundos
        janela_tempo = np.sqrt(1 / taxa_amostragem)
        # Quantidade de amostras em cada janela
        tamanho_janela = int(janela_tempo * taxa_amostragem)
        indice_inicio = 0
        indice_fim = tamanho_janela
    
        resultados = []
    
        while indice_fim <= len(sinal):
            vetorItem=[]
            
            sinal_trecho = sinal[indice_inicio:indice_fim]
    
            # Aplicar a Transformada de Fourier
            transformada = np.fft.fft(sinal_trecho)
            frequencias = np.fft.fftfreq(len(sinal_trecho), 1 / taxa_amostragem)
    
            # Encontrar a frequência com maior magnitude
            indice_maior_magnitude = np.argmax(np.abs(transformada))
            frequencia_predominante = frequencias[indice_maior_magnitude]
            amplitude_media = np.mean(np.abs(sinal_trecho))                
    
            # Calcular o tempo do centro da amostragem
            tempo_centro = (indice_inicio + indice_fim) / (2 * taxa_amostragem)        
            
            vetorItem.append(indice_inicio)
            vetorItem.append(tempo_centro)
            vetorItem.append(frequencia_predominante)
            vetorItem.append(amplitude_media)
    
            # Adicionar os resultados ao vetor
            resultados.append(vetorItem)
    
            # Avançar para a próxima janela
            indice_inicio += tamanho_janela
            indice_fim += tamanho_janela
    
        return resultados
    
    def normalizarEntre_0_e_1(self,serie):
        minSerie=np.abs(np.min(serie))
        maxSerie=np.abs(np.max(serie))
        amplitudeSerie=maxSerie-minSerie
        
        serieRetorno=(np.abs(serie)-minSerie)/amplitudeSerie
        return serieRetorno
    
    def normalizarEntre_menos1_e_1(self,serie):
        maxSerie=np.max(np.abs(serie))                
        serieRetorno=serie/maxSerie
        return serieRetorno
    
    def apresentarSinalEmGrafico3D(self, sinal):
    
        #sinal = np.random.randn(taxa_amostragem)
        
        tempo_frequencia_intensidade=self.calcularTempoFrequenciaIntensidade(sinal)
        
        indice_inicio, tempo_centro, frequencia_predominante, amplitude_media = np.array(tempo_frequencia_intensidade).T
        
        # Criar a string "n-tempo"
        n_tempo = [f"{x1}-{x2}" for x1, x2 in zip(indice_inicio, tempo_centro)]

        print(n_tempo)
        
        # Configurar a figura 3D
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, projection='3d')
        
        #print(tempo_centro.shape, frequencia_predominante.shape, amplitude_media.shape,  type(amplitude_media[0]))
        
        #Normalizar as frequências entre -1 e 1
        frequencia_predominante=self.normalizarEntre_menos1_e_1(frequencia_predominante)
                
        # Plotar os resultados
        ax.scatter(tempo_centro, frequencia_predominante, amplitude_media)
        
        # Definir os rótulos para cada item do eixo x
        #plt.xticks(tempo_centro, n_tempo)
        
        # Configurar rótulos dos eixos
        ax.set_xlabel('Tempo(s)')
        ax.set_ylabel('Frequência(hz)')
        ax.set_zlabel('Amplitude(dB)')
        
        # Exibir o gráfico
        plt.show()

    def apresentarSinalEmHistograma2D(self, sinal):
        tempo_frequencia_intensidade = self.calcularTempoFrequenciaIntensidade(sinal)
        indice_inicio, tempo_centro, frequencia_predominante, amplitude_media = np.array(tempo_frequencia_intensidade).T
    
        # Normalizar as frequências entre -1 e 1
        frequencia_predominante = self.normalizarEntre_menos1_e_1(frequencia_predominante)
    
        # Criar a string "n-tempo"
        #n_tempo = [f"{x1}-{x2}" for x1, x2 in zip(indice_inicio, tempo_centro)]
    
        # Configurar a figura
        plt.figure(figsize=(10, 10))
    
        # Criar o histograma bidimensional
        plt.hist2d(tempo_centro, frequencia_predominante, bins=50, cmap='jet')

    
        # Definir os rótulos dos eixos
        plt.xlabel('Tempo (s)')
        plt.ylabel('Frequência (Hz)')
    
        # Exibir o gráfico
        plt.colorbar()
        plt.show()
        
    
    # Exporta vetores numpy para arquivo Excel
    # Usado para exportar os vetores indice_inicio, tempo_centro, frequencia_predominante, amplitude_media 
    # para um arquivo do Excel
    def exportarParaExcel(self, indice_inicio, tempo_centro, frequencia_predominante, amplitude_media, nome_arquivo):
        # Criar um DataFrame a partir dos vetores
        serieDados = {'indice_inicio': indice_inicio, 'tempo_centro': tempo_centro,
                      'frequencia_predominante': frequencia_predominante, 'amplitude_media': amplitude_media}
        df = pd.DataFrame(serieDados)
        
        # Exportar o DataFrame para um arquivo Excel
        df.to_excel(nome_arquivo, index=False)

    
    # Com erro:    
    def graficoCalor(self,x,y,z):
        # Gráfico de calor com rótulos internos
        fig, ax = plt.subplots()
        im = ax.imshow(z, cmap='hot')

        # Adicionar rótulos internos
        for i in range(len(y)):
            for j in range(len(x)):
                ax.text(j, i, z[i, j], ha='center', va='center', color='black')

        ax.set_xticks(np.arange(len(x)))
        ax.set_yticks(np.arange(len(y)))
        ax.set_xticklabels(x)
        ax.set_yticklabels(y)
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Intensidade', rotation=90, va='center')
        plt.show()
        
    # Não estou certo de que está correto:
    def graficoBarras3D(self, x, y, z):
        # Verificar e ajustar as dimensões dos vetores
        x = np.asarray(x)
        y = np.asarray(y)
        z,_ = np.meshgrid(z,z)
    
        # Verificar e ajustar as dimensões da matriz z
        if z.shape != (len(y), len(x)):
            print(z.shape, "<< z.shape")
            raise ValueError("A matriz z deve ter dimensões (len(y), len(x))")
    
        # Criar as grades
        xpos, ypos = np.meshgrid(x, y)
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros_like(xpos)
    
        # Calcular as dimensões das barras
        dx = (x[1] - x[0]) * np.ones_like(xpos)
        dy = (y[1] - y[0]) * np.ones_like(ypos)
        dz = z.flatten()
    
        # Gráfico de barras em 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz)
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.set_zlabel('Intensidade')
        plt.show()



