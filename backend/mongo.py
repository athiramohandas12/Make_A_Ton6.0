from flask import Flask
from flask_pymongo import PyMongo



# Configure your MongoDB URI here
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'

# Initialize PyMongo
mongo = PyMongo(app)

