import json
import os
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def generate_summary(input_json, summary_length=2, lambda_value=0.7):
    ringkasan_per_buku = []

    for buku in input_json["buku"]:
        abstrak = buku["abstrak"]

        # Tokenisasi abstrak menjadi kalimat
        kalimat = sent_tokenize(abstrak)

        # Menghitung vektor TF-IDF untuk kalimat
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(kalimat)

        # Menghitung kemiripan kosinus antar kalimat
        cosine_sim = np.dot(tfidf_matrix, tfidf_matrix.T)

        # Menginisialisasi ringkasan
        ringkasan = []

        # Memilih kalimat dengan skor TF-IDF tertinggi sebagai kalimat pertama dalam ringkasan
        indeks_kalimat_awal = np.argmax(np.sum(tfidf_matrix, axis=1))
        ringkasan.append(kalimat[indeks_kalimat_awal])

        while len(ringkasan) < summary_length:
            indeks_kalimat_terpilih = -1
            maksimal_nilai_mmr = -1

            # Menghitung nilai MMR untuk setiap kalimat dan memilih kalimat dengan nilai tertinggi
            for i in range(len(kalimat)):
                if kalimat[i] not in ringkasan:
                    nilai_mmr = lambda_value * cosine_sim[i, indeks_kalimat_awal] - (1 - lambda_value) * np.max(cosine_sim[i, np.array(ringkasan) != ""])
                    if nilai_mmr > maksimal_nilai_mmr:
                        maksimal_nilai_mmr = nilai_mmr
                        indeks_kalimat_terpilih = i

            # Menambahkan kalimat terpilih ke dalam ringkasan
            ringkasan.append(kalimat[indeks_kalimat_terpilih])

        # Menambahkan ringkasan buku ke daftar ringkasan
        ringkasan_per_buku.append(" ".join(ringkasan))

    return ringkasan_per_buku




current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'that.json')

# Membaca data dari file JSON
input_json = load_data(file_path)

# Menghasilkan ringkasan untuk setiap abstrak dalam JSON
hasil_ringkasan = generate_summary(input_json)

# Menampilkan ringkasan
print("Ringkasan:")
for idx, ringkasan in enumerate(hasil_ringkasan, start=1):
    print(f"Buku {idx}: {ringkasan}")
