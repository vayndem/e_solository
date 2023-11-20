import pymongo

def insert_data_to_mongodb(database_name, collection_name, data):
    try:
        client = pymongo.MongoClient("mongodb://localhost:27018/")
        db = client[database_name]
        collection = db[collection_name]


        result = collection.insert_many(data)
        data = [
            {
        "id_skripsi": "1",
        "judul": "Pengaruh Teknologi Kecerdasan Buatan dalam Pengelolaan Sumber Daya Manusia",
        "abstrak": "Python adalah bahasa pemrograman tingkat tinggi yang dirancang untuk menjadi mudah dibaca dan ditulis. Hal ini membuatnya sangat cocok untuk pemula yang ingin mempelajari pemrograman. Python memiliki sintaksis yang bersih dan mudah dimengerti, yang memungkinkan pengembang untuk fokus pada logika program daripada terjebak dalam detail teknis yang rumit. Bahasa pemrograman tingkat tinggi seperti Python memungkinkan pengembang untuk menulis kode dengan lebih sedikit baris dibandingkan dengan bahasa pemrograman lainnya, membuatnya efisien dan cepat untuk pengembangan.",
        "link": "a"
        }
        ]



        print(f"Koleksi '{collection_name}' berhasil ditambahkan ke dalam database '{database_name}'.")
        print(f"{len(result.inserted_ids)} dokumen berhasil disisipkan.")

    except Exception as e:
        print(f"Error: {e}")

# Define target database name and new collection name
target_database_name = "Prigel"
new_collection_name = "buku"

# Define data to insert
data_to_insert = [
    {
        "id_skripsi": "1",
        "judul": "Pengaruh Teknologi Kecerdasan Buatan dalam Pengelolaan Sumber Daya Manusia",
        "abstrak": "Python adalah bahasa pemrograman tingkat tinggi yang dirancang untuk menjadi mudah dibaca dan ditulis. Hal ini membuatnya sangat cocok untuk pemula yang ingin mempelajari pemrograman. Python memiliki sintaksis yang bersih dan mudah dimengerti, yang memungkinkan pengembang untuk fokus pada logika program daripada terjebak dalam detail teknis yang rumit. Bahasa pemrograman tingkat tinggi seperti Python memungkinkan pengembang untuk menulis kode dengan lebih sedikit baris dibandingkan dengan bahasa pemrograman lainnya, membuatnya efisien dan cepat untuk pengembangan.",
        "link": "a"
    }

]


insert_data_to_mongodb(target_database_name, new_collection_name)
