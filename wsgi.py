from flask import request
text = "./api/text_adventure.py" 
from flask import Flask
app = Flask(text)

@app.route('/', methods=['GET', 'POST'])
def landing():
    return text