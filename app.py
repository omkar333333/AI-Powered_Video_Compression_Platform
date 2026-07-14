import os
import threading
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from utils.models import db, CompressionHistory
from utils.analyzer import analyze_video
from utils.predictor import predict_best_settings
from utils.compressor import compress_video
from datetime import datetime

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__name__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
app.config['COMPRESSED_FOLDER'] = os.path.join(BASE_DIR, 'compressed')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024 # 10 GB limit

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

# Global dict to store compression status (in a real app, use Redis or Celery)
# Format: { history_id: {"status": "processing/completed/failed", "progress": int} }
compression_tasks = {}

ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze video
        metadata = analyze_video(filepath)
        if "error" in metadata:
            return jsonify({'error': metadata['error']}), 500
            
        return jsonify({'message': 'File uploaded successfully', 'metadata': metadata, 'filename': filename})
        
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = predict_best_settings(data)
    return jsonify(prediction)

def background_compress(history_id, input_path, output_path, codec, crf, target_bitrate, app_context):
    with app_context:
        start_time = time.time()
        success, message = compress_video(input_path, output_path, codec=codec, crf=crf, target_bitrate=target_bitrate)
        end_time = time.time()
        
        history = db.session.get(CompressionHistory, history_id)
        if success:
            history.status = 'completed'
            history.compressed_size = round(os.path.getsize(output_path) / (1024 * 1024), 2)
            if history.original_size > 0:
                history.ratio = round((history.compressed_size / history.original_size) * 100, 2)
            history.processing_time = round(end_time - start_time, 2)
            compression_tasks[history_id] = {"status": "completed", "progress": 100}
        else:
            history.status = 'failed'
            print(f"Compression failed for {history_id}: {message}")
            compression_tasks[history_id] = {"status": "failed", "progress": 0, "error": message}
            
        db.session.commit()

@app.route('/start_compression', methods=['POST'])
def start_compression():
    data = request.json
    filename = data.get('filename')
    mode = data.get('mode', 'balanced') # high, balanced, max, custom
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(input_path):
        return jsonify({'error': 'File not found'}), 404
        
    original_size = round(os.path.getsize(input_path) / (1024 * 1024), 2)
    
    # Determine settings
    codec = "hevc_nvenc"
    crf = 28
    
    if mode == 'high':
        crf = 22
    elif mode == 'balanced':
        crf = 28
    elif mode == 'max':
        crf = 32
    elif mode == 'custom':
        codec = data.get('codec', 'hevc_nvenc')
        crf = int(data.get('crf', 28))
        
    output_filename = f"compressed_{int(time.time())}_{filename}"
    output_path = os.path.join(app.config['COMPRESSED_FOLDER'], output_filename)
    
    # Create DB entry
    history = CompressionHistory(
        filename=output_filename,
        original_size=original_size,
        compression_mode=f"{mode} (CRF {crf}, {codec})"
    )
    db.session.add(history)
    db.session.commit()
    
    # Calculate target bitrate to GUARANTEE size reduction
    metadata = analyze_video(input_path)
    original_bitrate = metadata.get('bitrate', 0)
    target_bitrate = None
    
    if original_bitrate > 0:
        if mode == 'high':
            target_bitrate = int(original_bitrate * 0.75)
        elif mode == 'balanced':
            target_bitrate = int(original_bitrate * 0.50)
        elif mode == 'max':
            target_bitrate = int(original_bitrate * 0.30)
        else:
            target_bitrate = int(original_bitrate * 0.60)
        target_bitrate = max(target_bitrate, 500000) # Minimum 500 kbps
        
    history_id = history.id
    compression_tasks[history_id] = {"status": "processing", "progress": 0}
    
    # Start thread
    app_context = app.app_context()
    thread = threading.Thread(target=background_compress, args=(history_id, input_path, output_path, codec, crf, target_bitrate, app_context))
    thread.daemon = True
    thread.start()
    
    return jsonify({'history_id': history_id, 'message': 'Compression started'})

@app.route('/processing', methods=['GET'])
def processing():
    history_id = request.args.get('id')
    if not history_id:
        return redirect(url_for('index'))
    return render_template('processing.html')

@app.route('/status/<int:history_id>', methods=['GET'])
def check_status(history_id):
    if history_id in compression_tasks:
        return jsonify(compression_tasks[history_id])
        
    # Check DB if not in memory dict (e.g. server restarted)
    history = db.session.get(CompressionHistory, history_id)
    if history:
        return jsonify({"status": history.status, "progress": 100 if history.status == 'completed' else 0})
        
    return jsonify({'error': 'Not found'}), 404
    
@app.route('/result/<int:history_id>', methods=['GET'])
def result(history_id):
    history = db.session.get(CompressionHistory, history_id)
    if not history:
        return "Not found", 404
    return render_template('result.html', history=history)

@app.route('/download/<int:history_id>', methods=['GET'])
def download(history_id):
    history = db.session.get(CompressionHistory, history_id)
    if not history or history.status != 'completed':
        return "File not available", 404
        
    filepath = os.path.join(app.config['COMPRESSED_FOLDER'], history.filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found on disk", 404

@app.route('/history', methods=['GET'])
def history():
    records = CompressionHistory.query.order_by(CompressionHistory.created_at.desc()).all()
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
