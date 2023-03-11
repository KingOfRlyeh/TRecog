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


note_map = np.array(['C','Cs','D','Eb','E','F','Fs','G','Gs', 'A','As','B'])

gpath = 'C:/Users/jwbol/OneDrive/Desktop/Piano triads/piano_triads/A_maj_4_0.wav'


    #bigboy function that gets us what we want right here
def get_chordname(path: str, threshold= 5):
    nrmlzed_chords_meta = np.array([0, 9, 15, 16])
    numnotelist = get_notelist(path=path, c= False, threshold= threshold)
    if(np.size(numnotelist) > 4):
        return "Invalid, try raising threshold"
    if(np.size(numnotelist) == 0):
        return "Invalid, try lowering threshold"
    inv = inversions(numnotelist)
    hs_inv= numnote_to_hsteps(inv)
    chord_chart = np.genfromtxt('nrmlzed_chords.csv', delimiter= ',', dtype= str, skip_header= 1)
    chord_chart_intvls = chord_chart[nrmlzed_chords_meta[np.size(numnotelist) - 2]:nrmlzed_chords_meta[np.size(numnotelist) - 1], :np.size(hs_inv, 1)].astype(np.int16)
    print(chord_chart_intvls)
    index = -1
    tonic = -1
    tindex = 0
    for arr in  hs_inv:
        for x in range(np.size(chord_chart_intvls, axis= 0)):
            if(np.array_equal(arr, chord_chart_intvls[x])):
                index = x
                tonic = inv[tindex][0]
        tindex+= 1
    return note_map[tonic] + chord_chart[nrmlzed_chords_meta[np.size(numnotelist) - 2] + index, 3]    

    
def get_notelist(path: str, c= True, threshold= 5): #extract chromatic tones from wav file
    #when c is false, note names are returned, else a number 0-11 is returned
    #getting notes out of sample
    #parts for simple chord analysis
    #CQT fourier transform with a low-ish threshold to get rid of noise 
    
    samples, sample_rate = librosa.load(path, sr=None)
    
    #hey! if the program is broken and you just updated librosa, this is the problem here
    chrom_note = librosa.feature.chroma_cqt(y= samples, threshold= threshold)# make more robust noise threshold
    #boolean mask
    chordv = np.sum(chrom_note, axis= 1)
    chordv = np.nonzero(chordv > 20)
    #extract note names according to note_map
    if(np.size(chordv, 0) > 4):
        raise Exception('Too many tones found, try raising threshold.')
    else:
        if(c):
            notelist = note_map[chordv]
            return notelist
        else:
            return chordv

def get_chromograph(path: str, threshold):
    samples, sample_rate = librosa.load(path, sr=None)
    chrom_note= librosa.feature.chroma_cqt(samples, threshold= threshold)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(chrom_note, y_axis='chroma', x_axis= 'time', ax=ax)
    ax.set(title= os.path.basename(path))
    fig.colorbar(img, ax=ax)
    
    return fig


#determine intervals between notes (in half steps) 
def numnote_to_hsteps(numlist):
    hstep_arr = np.empty(shape= (np.size(numlist, 1), np.size(numlist, 0) - 1), dtype=(int))
    for x in range(np.size(numlist, axis= 0)):
        for y in range(np.size(numlist, axis= 1) - 1):
            if(numlist[x, y + 1] > numlist[x, y]):
                hstep_arr[x, y] = numlist[x, y + 1] - numlist[x, y]
            else:
                hstep_arr[x,y] = (12 - numlist[x, y]) + numlist[x, y + 1]  
    return(hstep_arr)
            
#get inversions using incursion
def inversions(a): #should raise exception if a is not ndarray 
    return inversions_helper(a=a, stat=a, inversion=1)
    
def inversions_helper(a, stat, inversion):
    
    if(inversion < np.size(stat)):
        a = np.concatenate((a, np.roll(stat, inversion)))
        return inversions_helper(a, stat, inversion + 1)
    else:
        return np.reshape(a, (int(np.size(a)/np.size(stat)), np.size(stat)))
     
get_chordname(gpath)

