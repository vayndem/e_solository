import json
import re
import os
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Fungsi untuk memuat data dari file JSON
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def clean_text(text):
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    return cleaned_text

# Fungsi untuk menghasilkan ringkasan menggunakan TF-IDF dan MMR
def generate_summary(abstrak):
    # Tokenisasi abstrak menjadi kalimat
    kalimat = sent_tokenize(abstrak)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(kalimat)

    # Menghitung kemiripan kosinus antar kalimat
    cosine_sim = np.dot(tfidf_matrix, tfidf_matrix.T)
    
    ringkasan = []
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

    return " ".join(ringkasan)


# Membaca data dari file JSON
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'that.json')
input_json = load_data(file_path)


summary_length = 3  # Tentukan panjang ringkasan yang diinginkan
lambda_value = 0.7  # Tentukan nilai lambda untuk MMR
for buku in input_json['buku']:
    abstrak = buku['abstrak']
    ringkasan = generate_summary(abstrak)
    buku['ringkasan'] = ringkasan

# Mengambil abstrak ringkasan dari setiap objek skripsi
texts = [cobaan['ringkasan'] for cobaan in input_json['buku']]
ids = [cobaan['id_skripsi'] for cobaan in input_json['buku']]
links = [cobaan['link'] for cobaan in input_json['buku']]

# Membangun pipeline dengan CountVectorizer dan Multinomial Naive Bayes
vectorizer = CountVectorizer().fit(texts)
texts_vectorized = vectorizer.transform(texts)
text_clf = MultinomialNB()
text_clf.fit(texts_vectorized, ids)  # Label sesuai dengan data latih

# Meminta input dari pengguna
teks_input = input("Masukkan teks untuk mencari kemiripan: ")
teks_input = clean_text(teks_input)

# Mengonversi teks input ke bentuk vektor menggunakan vectorizer yang sudah dilatih
teks_input_vectorized = vectorizer.transform([teks_input])

# prediksi
probabilities = text_clf.predict_proba(teks_input_vectorized)
predictions_with_probabilities = list(zip(ids, probabilities[0], links))

# Mengurutkan dan output
sorted_predictions = sorted(predictions_with_probabilities, key=lambda x: x[1], reverse=True)

out = ""
if all(probability == probabilities[0][0] for _, probability, _ in sorted_predictions):
    out = "Tidak ada"
else:
    for id_skripsi, probability, link in sorted_predictions:
        out += f"Skripsi ID {id_skripsi}: {probability:.4f} dengan link : {link}\n"

print(out.strip())

# print("-------")
# for i in range (len(texts)):
#     print(texts[i])
#     print("\n")
