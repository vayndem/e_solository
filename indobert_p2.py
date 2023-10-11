import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB

# Membaca data dari file JSON
with open('that.json', 'r') as json_file:
    data = json.load(json_file)

# Mengambil abstrak dari setiap objek skripsi
texts = [cobaan['abstrak'] for cobaan in data['buku']]
ids = [cobaan['id_skripsi'] for cobaan in data['buku']]
links = [cobaan['link'] for cobaan in data['buku']]

# Membangun pipeline dengan CountVectorizer dan Multinomial Naive Bayes
vectorizer = CountVectorizer().fit(texts)
texts_vectorized = vectorizer.transform(texts)
text_clf = MultinomialNB()
text_clf.fit(texts_vectorized, ids)  # Label sesuai dengan data latih

# Meminta input dari pengguna
teks_input = input("Masukkan teks untuk mencari kemiripan: ")

# Mengonversi teks input ke bentuk vektor menggunakan vectorizer yang sudah dilatih
teks_input_vectorized = vectorizer.transform([teks_input])

# prediksi
similarities = cosine_similarity(teks_input_vectorized, texts_vectorized)[0]
probabilities = text_clf.predict_proba(teks_input_vectorized)

# Mendapatkan probabilitas prediksi kemiripan berdasarkan model Naive Bayes
predictions_with_probabilities = list(zip(ids, probabilities[0], links))

# Mengurutkan
sorted_predictions = sorted(predictions_with_probabilities, key=lambda x: x[1], reverse=True)

# Menampilkan hasil prediksi dengan probabilitas terbesar dan link yang sesuai
for id_skripsi, probability, link in sorted_predictions:
    print(f"Skripsi ID {id_skripsi}: {probability:.4f} dengan link : {link}")
