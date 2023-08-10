from pymongo import MongoClient

# Replace this with your MongoDB Atlas URI
MONGO_URI = 'your-mongodb-uri-here'

# Create a MongoDB client using the provided URI
mongo_client = MongoClient(MONGO_URI)

# Connect to the 'Note_app' database
db = mongo_client.Note_app

# Access the 'notes' collection
notes_collection = db.notes
