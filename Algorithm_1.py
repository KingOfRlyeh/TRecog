# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 17:06:14 2022

@author: jwbol
"""
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

# Load the audio file
AUDIO_FILE = "C:/Users/jwbol/OneDrive/Desktop/Piano triads/piano_triads/G_dim_5_0.wav"
samples, sample_rate = librosa.load(AUDIO_FILE, sr=None)

note_map = np.array(['C','Cs','D','Eb','E','F','Fs','G','Gs','A','Ab','B'])

plt.figure(figsize=(14, 5))

def get_notelist(path: str): #extract chromatic tones from wav file
    #getting notes out of sample
    #parts for simple chord analysis
    #CQT fourier transform with a low-ish threshold to get rid of noise
    chrom_note = librosa.feature.chroma_cqt(samples, threshold= 0.2)
    #spec plot and color bar
    fig, ax = plt.subplots()
    img = librosa.display.specshow(chrom_note, y_axis='chroma', x_axis= 'time', ax=ax)
    #set title as file name
    ax.set(title= os.path.basename(path))
    #colorbar
    fig.colorbar(img, ax=ax)
    #boolean mask
    chordv = np.sum(chrom_note, axis= 1)
    chordv = np.where(chordv > 20)
    #extract note names according to note_map
    notelist = note_map[chordv]
    return notelist

  
def get_root(chord: tuple): #extract root from chromatic tones
    specg = librosa.feature.chroma_cqt(samples)










