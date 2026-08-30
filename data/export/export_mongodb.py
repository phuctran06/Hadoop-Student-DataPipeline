from pymongo import MongoClient
import csv
import os


# CONFIG
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "StudentManagementBigData"

OUTPUT_DIR = "data/export"

COLLECTIONS = ["Student","Course","Enrollment"]


# CONNECT MONGODB
client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

# Test connection
client.admin.command("ping")

print("MongoDB connected!")
print(f"Database: {DATABASE_NAME}")


#create output dir
os.makedirs(OUTPUT_DIR, exist_ok=True)


# EXPORT FUNCTION

def export_collection(collection_name):

    collection = db[collection_name]

    documents = list(collection.find())

    if not documents:
        print(f"{collection_name} is empty.")
        return

    # Lấy tất cả field xuất hiện trong documents
    fields = set()

    for document in documents:
        fields.update(document.keys())

    fields = list(fields)

    # Đưa _id xuống cuối
    if "_id" in fields:
        fields.remove("_id")
        fields.append("_id")

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{collection_name}.csv"
    )

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
            extrasaction="ignore"
        )

        writer.writeheader()

        for document in documents:

            # MongoDB ObjectId không ghi trực tiếp vào CSV được
            document["_id"] = str(document["_id"])

            writer.writerow(document)

    print(
        f"[OK] {collection_name}: "
        f"{len(documents)} records -> {output_file}"
    )


# EXPORT ALL COLLECTIONS
for collection_name in COLLECTIONS:
    export_collection(collection_name)


# CLOSE CONNECTION
client.close()

print("\nExport completed!")