from flask import request
import text_adventure;
from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def landing():
    return text_adventure