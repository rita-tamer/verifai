from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from analysis.metadata import analyze_metadata
from analysis.model_api import analyze_sightengine
from utils.verdict import classify_result
from analysis.dbcheck import analyze_byte_signatures


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"Error": "Unsupported or missing file"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    # Run analysis
    ai_score = analyze_sightengine(path)
    ai_tags = analyze_metadata(path)
    byte_result = analyze_byte_signatures(path)

    print("SightEngine score:", ai_score)
    print("Metadata tags:", ai_tags)
    print("Byte result:", byte_result)
    
    result, reason = classify_result(ai_score, ai_tags, byte_result)
    return jsonify({"result": result, "reason": reason})

if __name__ == '__main__':
    app.run(debug=True)
