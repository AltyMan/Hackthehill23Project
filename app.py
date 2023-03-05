from flask import Flask, session, render_template, Response, request, url_for, flash, redirect
from flask_mysqldb import MySQL

from ConversionFunctions import *
from database import *

app = Flask(__name__, template_folder="FrontEnd", static_folder="static")

privateKey, publicKey = loadKeys()

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
        # encText = encrypt(request.form['text'], publicKey)
        # decText = decrypt(encText, privateKey)
        return render_template("index.html", text=text, img=img)

@app.route('/form')
def form():
    return render_template('signup.html')
 
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return "Sign up via the login Form"
    if request.method == 'POST':
        email = request.form['email'].replace("@", "_").replace(".", "_")
        password = deconstructSTR(request.form['password'])
        
        ifExists = checkCredentialExistance(email)
        if (ifExists):
            return f"Can't sign up, account already exists"
        else :
            createCredentials(email, password)
            return f"Done!!"

if __name__ == "__main__":
    app.run(debug=True)