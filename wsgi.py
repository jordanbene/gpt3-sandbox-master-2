from flask import request
from api import text_adventure
text = "./api/text_adventure.py" 
from flask import Flask
app = Flask(text_adventure)

@app.route('/', methods=['GET', 'POST'])
def landing():
    return text_adventure