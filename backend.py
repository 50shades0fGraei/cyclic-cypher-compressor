
from flask import Flask, request, send_from_directory, jsonify, Response
import os
import subprocess
import uuid

app = Flask(__name__, static_folder='web')
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# @app.after_request
# def add_header(response: Response) -> Response:
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '-1'
#     return response

# --- Configuration -- -
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# --- Routes -- -
@app.route('/')
def index():
    return send_from_directory('web', 'index.html')

@app.route('/<path:path>')
def send_web_files(path):
    return send_from_directory('web', path)

@app.route('/compress', methods=['POST'])
def compress_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # --- Save the uploaded file -- -
    session_id = str(uuid.uuid4())
    input_dir = os.path.join(UPLOAD_FOLDER, session_id)
    output_dir = os.path.join(OUTPUT_FOLDER, session_id)
    os.makedirs(input_dir)
    os.makedirs(output_dir)
    input_path = os.path.join(input_dir, file.filename)
    file.save(input_path)

    # --- Run the HYBRID compression -- -
    # Your script creates a single compressed file.
    output_path = os.path.join(output_dir, f"{file.filename}.ccc.trace")
    
    # This is the corrected command to call your script.
    cmd = [
        'python', 
        'core/cyclic_hybrid.py', 
        'compress', 
        input_path, 
        output_path
    ]
    try:
        # We run the command. If it fails, it will raise an exception.
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Compression stdout:", process.stdout)
        print("Compression stderr:", process.stderr)
    except subprocess.CalledProcessError as e:
        # If the script returns a non-zero exit code, we return an error.
        print(f"ERROR during compression: {e}")
        print(f"Stderr: {e.stderr}")
        return jsonify({'error': 'Compression failed.', 'details': e.stderr}), 500

    # --- Prepare response -- -
    # We only have one download link now.
    trace_filename = os.path.basename(output_path)

    return jsonify({
        'message': 'Compression successful!',
        'trace_url': f'/download/{session_id}/{trace_filename}',
        'meta_url': None # Set to None, as there is no meta file
    })

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    return send_from_directory(os.path.join(OUTPUT_FOLDER, session_id), filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False)
