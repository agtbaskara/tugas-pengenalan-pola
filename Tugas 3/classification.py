"""
## Klasifikasi Text - Tugas 3 Pengenalan Pola

## Baskara - 16/398499/PA/17460

### Import Library
"""

import pandas as pd
import numpy as np
import nltk
import math
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

"""### Data Preparation (Pembagian Menjadi Training & Test)"""

df = pd.read_csv('data_penyakit.csv', names=['tanda_gejala','diagnosis_penyakit'])
training = df[df['diagnosis_penyakit'].notnull()]
test = df[df['diagnosis_penyakit'].isnull()]

training.head()

test.head()

"""### Tokenization & Stemming Data Training"""

factory = StemmerFactory()
stemmer = factory.create_stemmer()
tokenizer = nltk.RegexpTokenizer(r'\w+')

for index, row in training.iterrows():
    # Stemming
    stemmed = stemmer.stem(row[0])
    #Tokenization
    tokens = tokenizer.tokenize(row[0])
    #Case Folding
    words = [w.lower() for w in tokens]
    training.at[index, 'tanda_gejala'] = words

training.head()

"""### Membuat Kolom Untuk Setiap Kata"""

columnlist = []
for index, row in training.iterrows():
    columnlist = np.concatenate((columnlist, row[0]))
columnlist = np.unique(columnlist)

for index in range(len(columnlist)):
    training.insert(2, str(columnlist[index]), 0)

training.head()

"""### Menghitung Jumlah Frekuensi Setiap Kata"""

for index, row in training.iterrows():
    for columnindex in range(len(columnlist)):
        training.at[index, columnlist[columnindex]] = row[0].count(str(columnlist[columnindex]))

training.head()

"""### Prepare Test Data"""

test.insert(2, 'jarak', 0.0)

"""### Preprocessing dan Penghitungan Jumlah Frekuensi Setiap Kata"""

for index, row in test.iterrows():
    # Stemming
    stemmed = stemmer.stem(row[0])
    #Tokenization
    tokens = tokenizer.tokenize(row[0])
    #Case Folding
    words = [w.lower() for w in tokens]
    test.at[index, 'tanda_gejala'] = words
for index in range(len(columnlist)):
    test.insert(3, str(columnlist[index]), 0)
for index, row in test.iterrows():
    for columnindex in range(len(columnlist)):
        test.at[index, columnlist[columnindex]] = row[0].count(columnlist[columnindex])

"""### Penghitungan Jarak (Menggunakan Euclidean)"""

for test_index, test_row in test.iterrows():
    distance = []
    for train_index, train_row in training.iterrows():
        temp = 0
        for columnindex in range(len(columnlist)):
            temp = temp + (test_row[3+columnindex] - train_row[2+columnindex])**2
        distance += [math.sqrt(temp)]
    test.at[test_index, 'jarak'] = (np.min(distance))
    test.at[test_index, 'diagnosis_penyakit'] = str(df['diagnosis_penyakit'][np.argmin(distance)])

"""### Hasil Prediksi"""

test.iloc[:, : 3]
