from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

# Database model for files and YouTube links
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(200), nullable=False)

class YouTubeLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(200), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '123':  # Replace with your actual admin password
            files = request.files.getlist('file')
            names = request.form.getlist('display_name')
            yt_urls = request.form.getlist('yt_url')
            yt_names = request.form.getlist('yt_display_name')

            if len(files) == len(names):  # Ensure each file has a corresponding display name
                for i, file in enumerate(files):
                    if file and names[i]:
                        filename = file.filename
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        new_file = File(filename=filename, display_name=names[i])
                        db.session.add(new_file)
                db.session.commit()

            if len(yt_urls) == len(yt_names):  # Ensure each YouTube link has a corresponding display name
                for i, url in enumerate(yt_urls):
                    if url and yt_names[i]:
                        new_link = YouTubeLink(url=url, display_name=yt_names[i])
                        db.session.add(new_link)
                db.session.commit()
                
            return redirect('/admin')
        return 'Invalid password', 403
    
    files = File.query.all()
    youtube_links = YouTubeLink.query.all()
    return render_template('admin.html', files=files, youtube_links=youtube_links)

@app.route('/client')
def client():
    files = File.query.all()
    youtube_links = YouTubeLink.query.all()
    return render_template('client.html', files=files, youtube_links=youtube_links)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<int:file_id>')
def download(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

@app.route('/delete/<int:file_id>')
def delete(file_id):
    file = File.query.get_or_404(file_id)
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(file)
    db.session.commit()
    return redirect('/admin')

@app.route('/delete_link/<int:link_id>')
def delete_link(link_id):
    link = YouTubeLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
