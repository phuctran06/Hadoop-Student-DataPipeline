from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "StudentManagementBigData"

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

student_collection = db["Student"]
course_collection = db["Course"]
enrollment_collection = db["Enrollment"]