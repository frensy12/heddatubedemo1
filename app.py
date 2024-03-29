from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['THUMBNAIL_FOLDER'] = 'thumbnails'
app.config['TITLE_FOLDER'] = 'titles'

ALLOWED_EXTENSIONS = {'mp4', 'webm', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_thumbnail(video_path, thumbnail_path):
    clip = VideoFileClip(video_path)
    clip.save_frame(thumbnail_path, t=1)  # Save a thumbnail from the 1-second mark
    clip.close()
    
    

@app.route('/')
def index():
    videos = [video for video in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(video)]
    thumbnails = [f"{os.path.splitext(video)[0]}.png" for video in videos]
    video_data = list(zip(videos, thumbnails))
    return render_template('index.html', videos=video_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], f"{os.path.splitext(filename)[0]}.png")

            file.save(video_path)
            generate_thumbnail(video_path, thumbnail_path)

            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/thumbnails/<filename>')
def thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

@app.route('/videos/<filename>')
def video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)