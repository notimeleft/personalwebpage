
from flask import Flask
app = Flask(__name__)

#will it work?
@app.route('/')
def hello():
    text = ''
    try:
        import cv2
        text = 'success' 
    except:
        text = 'fail'
        pass
    return text + ' to load openCV'


if __name__ == '__main__':
    app.run()