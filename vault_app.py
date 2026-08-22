import os
import uuid
import json
from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from werkzeug.utils import secure_filename
from double_crunch_marketplace import double_crunch_compress, iterative_decompress
import shutil

app = Flask(__name__)

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_STORAGE = os.path.join(BASE_DIR, 'vault_storage')
RESTORE_STORAGE = os.path.join(BASE_DIR, 'restored_storage')
TEMP_STORAGE = os.path.join(BASE_DIR, 'temp_storage')
METADATA_FILE = os.path.join(VAULT_STORAGE, 'metadata.json')

os.makedirs(VAULT_STORAGE, exist_ok=True)
os.makedirs(RESTORE_STORAGE, exist_ok=True)
os.makedirs(TEMP_STORAGE, exist_ok=True)

# Ensure metadata exists
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, 'w') as f:
        json.dump({}, f)

def get_metadata():
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)

def save_metadata(data):
    with open(METADATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/files', methods=['GET'])
def list_files():
    metadata = get_metadata()
    files = []
    for cdv6_id, info in metadata.items():
        cdv6_path = os.path.join(VAULT_STORAGE, f"{cdv6_id}.cdv6")
        rebuilt_path = os.path.join(RESTORE_STORAGE, info['original_filename'])
        files.append({
            'id': cdv6_id,
            'label': info['label'],
            'original_filename': info['original_filename'],
            'cdv6_exists': os.path.exists(cdv6_path),
            'rebuilt_exists': os.path.exists(rebuilt_path)
        })
    return jsonify({'files': files})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    label = request.form.get('label', 'Unnamed File')
    
    filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    temp_path = os.path.join(TEMP_STORAGE, filename)
    cdv6_path = os.path.join(VAULT_STORAGE, f"{file_id}.cdv6")
    
    file.save(temp_path)
    
    # Run Double Crunch
    result = double_crunch_compress(temp_path, cdv6_path)
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    if not result or not os.path.exists(cdv6_path):
        return jsonify({'error': 'Compression failed'}), 500
        
    # Update Metadata
    metadata = get_metadata()
    metadata[file_id] = {
        'label': label,
        'original_filename': filename
    }
    save_metadata(metadata)
    
    return jsonify({'success': True, 'id': file_id})

@app.route('/api/restore/<file_id>', methods=['POST'])
def restore_file(file_id):
    metadata = get_metadata()
    if file_id not in metadata:
        return jsonify({'error': 'File not found'}), 404
        
    info = metadata[file_id]
    cdv6_path = os.path.join(VAULT_STORAGE, f"{file_id}.cdv6")
    rebuilt_path = os.path.join(RESTORE_STORAGE, info['original_filename'])
    
    if not os.path.exists(cdv6_path):
        return jsonify({'error': 'CDV6 missing'}), 404
        
    # Run extractor
    result = iterative_decompress(cdv6_path, rebuilt_path)
    if not result or not os.path.exists(rebuilt_path):
        return jsonify({'error': 'Restore failed'}), 500
        
    return jsonify({'success': True})

@app.route('/api/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    metadata = get_metadata()
    if file_id in metadata:
        info = metadata[file_id]
        cdv6_path = os.path.join(VAULT_STORAGE, f"{file_id}.cdv6")
        if os.path.exists(cdv6_path):
            os.remove(cdv6_path)
        
        # Cleanup mapping logic
        del metadata[file_id]
        save_metadata(metadata)
        
    return jsonify({'success': True})

@app.route('/api/rebuilt/<file_id>', methods=['DELETE'])
def delete_rebuilt(file_id):
    metadata = get_metadata()
    if file_id in metadata:
        info = metadata[file_id]
        rebuilt_path = os.path.join(RESTORE_STORAGE, info['original_filename'])
        if os.path.exists(rebuilt_path):
            os.remove(rebuilt_path)
    return jsonify({'success': True})

@app.route('/api/download/<file_id>')
def download_rebuilt(file_id):
    metadata = get_metadata()
    if file_id in metadata:
        info = metadata[file_id]
        rebuilt_path = os.path.join(RESTORE_STORAGE, info['original_filename'])
        if os.path.exists(rebuilt_path):
            return send_file(rebuilt_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/api/download/cdv6/<file_id>')
def download_cdv6(file_id):
    metadata = get_metadata()
    if file_id in metadata:
        cdv6_path = os.path.join(VAULT_STORAGE, f"{file_id}.cdv6")
        if os.path.exists(cdv6_path):
            return send_file(cdv6_path, as_attachment=True, download_name=f"{metadata[file_id]['label']}.cdv6")
    return "File not found", 404
