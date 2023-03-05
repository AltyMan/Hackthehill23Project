from flask import Flask, session, render_template, Response, request, url_for, flash, redirect
from ConversionFunctions import *

app = Flask(__name__, template_folder="FrontEnd", static_folder="static")

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


if __name__ == "__main__":
    app.run(debug=True)