from flask import Flask, session, render_template, Response, request, url_for, flash, redirect
from flask_mysqldb import MySQL

from ConversionFunctions import *
from database import *

app = Flask(__name__, template_folder="FrontEnd", static_folder="static")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootpassword'
app.config['MYSQL_DB'] = 'userLogin'
 
mysql = MySQL(app)

text = [{'filename': 'Default',
             'content': 'Testing'},]

img = [{'filename': 'Default',
             'src': 'https://icon-library.com/images/windows-file-icon/windows-file-icon-16.jpg'},]

@app.route('/', methods=('GET','POST'))
def index():
    if request.method == 'GET':
        return render_template("index.html", text=text, img=img)
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            pass
        else:
            text.append({'filename': file.filename,
             'content': "gun"})
        privateKey, publicKey = loadKeys()
        # encText = encrypt(request.form['text'], publicKey)
        # decText = decrypt(encText, privateKey)
        return render_template("index.html", text=text, img=img)

@app.route('/form')
def form():
    return render_template('signup.html')
 
@app.route('/signup', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Sign up via the login Form"
     
    if request.method == 'POST':
        email = request.form['email'].replace("@", "_").replace(".", "_")
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS " + email + " (password TEXT, userID int PRIMARY KEY AUTO_INCREMENT)")
        cursor.execute("INSERT INTO " + email  + "(password) VALUES (" + password + ")")
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

if __name__ == "__main__":
    app.run(debug=True)