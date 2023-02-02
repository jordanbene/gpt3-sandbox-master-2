from flask import request
import api.text_adventure
text = "./api/text_adventure.py" 
from flask import Flask
from api import text_adventure

app = text_adventure.app

if __name__ == '__main__':
    app.run(debug=False)
 
@app.route('/')
def index():
    '''Index page route'''
    return app.send_static_file('index.html')