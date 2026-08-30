from src.database.mongodb import client, db


try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
    print("Database:", db.name)

except Exception as e:
    print("MongoDB connection failed!")
    print(e)