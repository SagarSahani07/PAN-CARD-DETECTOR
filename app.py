from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils.image_compare import compare_images
import os

app = Flask(__name__)

# =========================
# CONFIGURATION
# =========================
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create folders if not present
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# =========================
# HELPER FUNCTION
# =========================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =========================
# HOME ROUTE
# =========================
@app.route('/')
def home():
    return render_template('index.html')

# =========================
# IMAGE UPLOAD + COMPARISON
# =========================
@app.route('/upload', methods=['POST'])
def upload():
    if 'original_image' not in request.files or 'tampered_image' not in request.files:
        return "Please upload both images."

    original_image = request.files['original_image']
    tampered_image = request.files['tampered_image']

    if original_image.filename == '' or tampered_image.filename == '':
        return "No selected file."

    if not (allowed_file(original_image.filename) and allowed_file(tampered_image.filename)):
        return "Only PNG, JPG, JPEG, and WEBP images are allowed."

    # Secure filenames
    original_filename = secure_filename(original_image.filename)
    tampered_filename = secure_filename(tampered_image.filename)

    # Save paths
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
    tampered_path = os.path.join(app.config['UPLOAD_FOLDER'], tampered_filename)

    # Save uploaded images
    original_image.save(original_path)
    tampered_image.save(tampered_path)

    # Compare images
    result = compare_images(original_path, tampered_path)

    return render_template(
        'result.html',
        similarity_score=result['similarity_score'],
        status=result['status'],
        original_result=result['original_result'],
        tampered_result=result['tampered_result'],
        difference_result=result['difference_result'],
        tampered_regions=result['tampered_regions']
    )


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)