from flask import Flask, render_template, request, secure_filename
app = Flask(__name__)

@app.route("/")
def main():
   return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


if __name__ == '__main__':
   app.run(host = 'localhost', port = 5000)
