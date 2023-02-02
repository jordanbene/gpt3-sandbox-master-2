from flask import request
import api.text_adventure
text = "./api/text_adventure.py" 
from flask import Flask
from api import text_adventure

if __name__ == '__main__':
    text_adventure.app.run(debug=False)
