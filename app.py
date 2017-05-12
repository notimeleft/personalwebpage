import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

import cv2
import numpy as np

app = Flask(__name__)
#will work???
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    # Get the name of the uploaded file
    file = request.files['file']
    
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        basedir = os.path.abspath(os.path.dirname(__file__))
        #print "|%s|" % os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], 'original_img'))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('show_cvimg',
                                filename=filename))
    else:
        
        return render_template('index.html',nofile='Please select a file to upload!')    	

	
@app.route('/opencv/<filename>')	
def show_cvimg(filename):
	
	try:
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
		img = cv2.imread('uploads/original_img')
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
		    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		    roi_gray = gray[y:y+h, x:x+w]
		    roi_color = img[y:y+h, x:x+w]
		    eyes = eye_cascade.detectMultiScale(roi_gray)
		    for (ex,ey,ew,eh) in eyes:
		        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		#cv2.imshow('img',img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		cv2.imwrite('uploads/processed_img.jpg',img)
		#return "eh?"
		return send_from_directory(app.config['UPLOAD_FOLDER'],'processed_img.jpg')
	except:
		return render_template('index.html',nofile='Looks like the picture format wasn\'t acceptable! please try another picture.') 



if __name__ == '__main__':
    
    app.run()