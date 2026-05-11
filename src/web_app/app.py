from flask import Flask
from flask import render_template # allows flask to load HTML files
from flask import request # allows to read submitted form data
from werkzeug.utils import secure_filename

from datetime import datetime # for unique file timetstamps

from csv_loader import load_csv

from quality_check import run_quality_checks

from pathlib import Path
app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

UPLOAD_FOLDER = PROJECT_ROOT / "data" / "web_uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
    
# route can handle page loads and from submissions
@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":
        
        if "csv_file" not in request.files:
            return render_template("index.html", error="No file filed was submitted")
        
        uploaded_file = request.files["csv_file"]

        if uploaded_file.filename == "":
            return render_template("index.html", error="No file was selected")
        
        if not allowed_file(uploaded_file.filename):
            return render_template("index.html", error="Not Supported file type")
        
        safe_uploaded_filename = secure_filename(uploaded_file.filename)

        # build a unique timestamped filename for uploaded files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_stem = Path(safe_uploaded_filename).stem
        file_extension = Path(safe_uploaded_filename).suffix
        timestamped_filename = f"{file_stem}_{timestamp}{file_extension}"

        saved_path = UPLOAD_FOLDER / timestamped_filename

        # Save uploaded file and load/run quality checks
        uploaded_file.save(saved_path)
        dataframe = load_csv(saved_path)
        results = run_quality_checks(dataframe)

        return render_template("report.html", file_name=timestamped_filename, results=results)
        #return f"Uploaded file: {uploaded_file.filename}" # temp display
        #return f"Saved file to: {saved_path}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)