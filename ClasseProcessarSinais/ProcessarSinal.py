# -*- coding: utf-8 -*-
"""
Created on Sat May 20 17:21:32 2023

@author: rober 
""" 

import numpy as np
import matplotlib.pyplot as plt
import librosa

sr=22050

class ProcessarSinal:
    
    def lerArquivoWav(self, nomeCompletoArquivo):
        
        # carregando os arquivos de áudio
        audio, _ = librosa.load(nomeCompletoArquivo, sr=sr)
        tamAudio=len(audio)
        duracao=1/sr*tamAudio
        print(f"Duração do áudio: {duracao :.3f}s, tamanho:{tamAudio} amostras")
        
        return audio
    
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
