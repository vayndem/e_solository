import re
import os
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from pymongo import MongoClient


def pencarian(inputan):
    def get_database():
        CONNECTION_STRING = "mongodb://localhost:27017"
        client = MongoClient(CONNECTION_STRING)
        return client['Prigel']  

    def load_data_from_mongodb():
        db = get_database()
        collection = db['buku']  
        documents = collection.find({})  
        data = []
        for document in documents:
            data.append(document)
        return data

    def clean_text(text):
        cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
        return cleaned_text

    def generate_summary(abstrak):
        kalimat = sent_tokenize(abstrak)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(kalimat)
        cosine_sim = np.dot(tfidf_matrix, tfidf_matrix.T)
        
        ringkasan = []
        indeks_kalimat_awal = np.argmax(np.sum(tfidf_matrix, axis=1))
        ringkasan.append(kalimat[indeks_kalimat_awal])

        while len(ringkasan) < summary_length:
            indeks_kalimat_terpilih = -1
            maksimal_nilai_mmr = -1

            for i in range(len(kalimat)):
                if kalimat[i] not in ringkasan:
                    #penilai MMR method
                    nilai_mmr = lambda_value * cosine_sim[i, indeks_kalimat_awal] - (1 - lambda_value) * np.max(cosine_sim[i, np.array(ringkasan) != ""])
                    
                    if nilai_mmr > maksimal_nilai_mmr:
                        maksimal_nilai_mmr = nilai_mmr
                        indeks_kalimat_terpilih = i

            ringkasan.append(kalimat[indeks_kalimat_terpilih])

        return " ".join(ringkasan)


    input_json = load_data_from_mongodb()

    summary_length = 3  
    lambda_value = 0.7  
    
    #mengambil data abstrak dan di MMR
    for buku in input_json:
        abstrak = buku.get('abstrak', '') 
        ringkasan = generate_summary(abstrak)
        buku['ringkasan'] = ringkasan

    texts = [buku['ringkasan'] for buku in input_json]
    ids = [buku['id_skripsi'] for buku in input_json]
    links = [buku['link'] for buku in input_json]

    vectorizer = CountVectorizer().fit(texts)
    texts_vectorized = vectorizer.transform(texts)
    text_clf = MultinomialNB()
    text_clf.fit(texts_vectorized, ids)

    teks_input = inputan
    teks_input = clean_text(teks_input)
    teks_input_vectorized = vectorizer.transform([teks_input])

    probabilities = text_clf.predict_proba(teks_input_vectorized)
    predictions_with_probabilities = list(zip(ids, probabilities[0], links))
    sorted_predictions = sorted(predictions_with_probabilities, key=lambda x: x[1], reverse=True)

    out = ""
    if all(probability == probabilities[0][0] for _, probability, _ in sorted_predictions):
        out = "Tidak ada"
    else:
        for id_skripsi, probability, link in sorted_predictions:
            out += f"Skripsi ID {id_skripsi}: {probability:.4f} dengan link : {link}\n"
    

    return out.strip()


    
