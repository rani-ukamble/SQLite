from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy # type: ignore
import os 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warnings
app.config['UPLOAD_FOLDER'] = 'uploads'  # create uploads folder manually

db = SQLAlchemy(app)

#create file model which containd Id , filename stores name of image
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)

#creating database tables
with app.app_context():
    db.create_all()



@app.route('/')
def index():
    #pass all images in frontend
    files = File.query.all()
    return render_template('index.html', files = files)

@app.route('/uploads', methods=['POST'])
def uploads():
    if request.method == 'POST':
        #upload image
        file = request.files['file']
        if file:
            filename = file.filename
            #save
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file = File(filename=filename)
            db.session.add(new_file) #store file in database
            db.session.commit()
            return redirect('/')
        return 'something wrong, please try again'
      #After submitting image will store in uploads folder  
      

#All uploaded images will shown at the frontend
@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#download images button
@app.route('/download/int:<file_id>')
def download(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

#Delete images button
@app.route('/delete/int:<file_id>')
def delete(file_id):
    file = File.query.get_or_404(file_id)
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    return redirect('/')

    
        
if __name__ == '__main__':
    app.run(debug=True)
