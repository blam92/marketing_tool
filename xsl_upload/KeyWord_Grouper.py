
# coding: utf-8

# ### Hacer Click en Kernel > Restart and Run All
# ### Luego Introducir nombre de Archivo en la función

# In[6]:

Agrupador('pasaporteSefaradiTEST')


# In[2]:

#IMPORTS

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('spanish')
stop.append('mas')

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

from nltk.stem.porter import *


# In[3]:

#Instanceo Stemmer y CountVectorizer

stemmer = PorterStemmer()
analyzer = CountVectorizer(strip_accents='ascii',stop_words=stop).build_analyzer()

#Armo la función que fitea ambas cosas
def stemmed_words(kws):
    return (stemmer.stem(w) for w in analyzer(kws))


# In[4]:

#Armamos una Función que tome como Parámetro el Excel con las palabras, y me devuelva un excel con las palabras
#y su grupo.


# In[5]:

def Agrupador(archivo):
    
    #Leo Excel con Kws
    Data = pd.read_excel(archivo+'.xlsx',skiprows=10)
    #Me quedo solo con la columna de Keywords del archivo
    kws = Data['Keyword']
    print('Excel Cargado')
    
    #Llamo a la funcion de arriba para que me fitee las KeyWords
    stem_vectorizer = CountVectorizer(analyzer=stemmed_words)
    a = stem_vectorizer.fit_transform(kws)
    
    #Armo el DataFrame del Vectorizer
    mat = pd.DataFrame(a.A, columns=stem_vectorizer.get_feature_names())
    print('Matriz Armada, ahora Looping...')

    #Reemplazo 1s por Nombre y 0s por NaN - ESTO TARDA
    for col_name in mat.columns:
        for row in range(len(mat)):
            if mat[col_name][row] == 1:
                mat[col_name][row] = str(col_name)
    print('Loop OK')
    
    
    #Ordeno las Columnas por frecuencia.
    freqs = [(word, a.getcol(idx).sum()) for word, idx in stem_vectorizer.vocabulary_.items()]
    
    sortedfreqs =  sorted (freqs, key = lambda x: -x[1])

    sortedcolumns = []
    for i in sortedfreqs:
        sortedcolumns.append(i[0])

    sorted_mat = mat[sortedcolumns]
    
    
    #Creo el Df para Grupos
    grupos = pd.DataFrame()
    print('Armando los Grupos...')

    #Le doy nombre a la Columna y aplico la función que va a traer solo los que no son nulos.
    grupos['AdGroup'] = sorted_mat.apply(lambda x: ' - '.join([unicode(y) for y in x if y != 0]), axis=1)

    #Agrego el grupo a la Data original
    Data['Python AdGroup'] = grupos['AdGroup']

    #Devuelvo Data
    Data.to_excel(archivo+'_PythonAdGroups.xlsx')
    print('Las Kws y sus AdGroups se encuentran en > '+archivo+'_PythonAdGroups.xlsx')

