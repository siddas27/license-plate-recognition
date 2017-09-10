import os
from flask import Flask, render_template, request
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def main():
   return render_template('index.html')

@app.route('/uploader', methods = ['POST'])
def upload_file():
   target = os.path.join(APP_ROOT, 'static/')
   print(target)

   if not os.path.isdir(target):
       os.mkdir(target)

   for file in request.files.getlist("file"):
       print(file)
       filename = file.filename
       destination = "/".join([target, filename])
       print(destination)
       file.save(destination)

   return render_template("save.html")

if __name__ == '__main__':
   app.run(host = 'localhost', port = 5000)
