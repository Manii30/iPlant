from keras.models import load_model
from flask import Flask, render_template, request,Response,jsonify,session
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from werkzeug.utils import secure_filename
import numpy as np
import os
import tensorflow as tf
import mysql.connector

app = Flask(__name__)
app.secret_key="helloManii"

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="identify"
)


def getdata(p):
	my_cursor = mydb.cursor()
	my_cursor.execute("select * from plants where names='"+p+"'")
	data = my_cursor.fetchall()
	my_cursor.close()
	return data

classes = ['Alstonia Scholaris Plant',
           'Arjun Plant',
           'Basil Plant',
           'Chinar Plant',
           'Gauva plant',
           'Jamun Plant',
           'Jatropha Plant',
           'Lemon plant',
           'Mango Plant',
           'Pomegranate plant',
           'Pongamia Pinnata plant',
           'Tamato Plant']

model = load_model('classify.h5')

model.make_predict_function()

def predict_label(img_path):
	i = load_img(img_path, target_size=(256,256))
	i = np.expand_dims(i,0)
	p = model.predict(i)
	return classes[np.argmax(p[0])]

upload_folder = os.path.join('static/image')

app.config['UPLOAD'] = upload_folder

# routes
@app.route("/")
def main():
	return render_template("main.html")


@app.route("/team.html")
def team():
	return render_template("team.html")

@app.route("/view.html")
def view():
	return render_template("view.html")

session = []

@app.route("/view.html", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		file = request.files['my_image']
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD'], filename))
		img = os.path.join(app.config['UPLOAD'], filename)
		p = predict_label(img)
		data = getdata(p)
		img = file.filename
		benfit = data[0][3].split(",")
		session.append(data)
		return render_template('view.html', prediction = p, img = img , student = data, benefits = benfit)
        
	else:
		return render_template('upload.html',prediction = "there should be a problem in prediction!!!")
	
@app.route('/history.html')
def profile():
    # Get the value from the session
    return render_template('history.html', session = session)

@app.route('/history.html')
def history():
	return render_template('history.html')   

@app.route("/upload.html")
def upload():
	return render_template("upload.html")



if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)


