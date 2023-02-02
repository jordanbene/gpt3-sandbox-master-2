from flask import request
import api.text_adventure
text = "./api/text_adventure.py" 
from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def landing():
    return api.text_adventure