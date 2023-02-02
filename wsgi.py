from flask import request, url_for
import api.text_adventure
text = "./api/text_adventure.py" 
from flask import Flask
from api import text_adventure

app = text_adventure.app
app.static_folder = 'public'

if __name__ == '__main__':
    app.run(debug=True)
 
@app.route('/')
def index():
    '''Index page route'''
    #return app.send_static_file('public/index.html')
    return app.send_static_file(url_for('static', filename='index.html'))
