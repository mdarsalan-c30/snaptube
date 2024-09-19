from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__)

# Directory where downloaded videos will be saved
DOWNLOAD_FOLDER = 'downloaded_videos'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Route to download YouTube video
@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    try:
        # Use PyTube to download the video
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        
        # Download the video to the specified folder
        video_path = stream.download(output_path=DOWNLOAD_FOLDER)
        video_filename = os.path.basename(video_path)

        # Return the download link for the frontend
        return jsonify({'download_url': f'/downloaded_videos/{video_filename}'}), 200

    except Exception as e:
        # Return error message in case of failure
        return jsonify({'error': str(e)}), 400

# Route to serve the downloaded video file
@app.route('/downloaded_videos/<filename>')
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
