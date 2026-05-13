from flask import Flask
from flask import render_template # allows flask to load HTML files
from flask import request # allows to read submitted form data
from werkzeug.utils import secure_filename

from datetime import datetime # for unique file timetstamps
from pathlib import Path

from batch_processor import process_csv_folder
from rules_validator import load_rules_file


app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

UPLOAD_FOLDER = PROJECT_ROOT / "data" / "web_uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

# check uploaded rules files is JSON file
def allowed_rules_file(filename):

    # must have extension
    if "." not in filename:
        return False
    
    file_extension = filename.rsplit(".",1)[1].lower()

    if file_extension == "json":
        return True

def create_timestamp():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return timestamp

# build a unique timestamped filename for uploaded files
def create_timestamped_filename(original_filename):

    safe_filename = secure_filename(original_filename)

    file_stem = Path(safe_filename).stem
    file_extension = Path(safe_filename).suffix

    timestamp = create_timestamp()
    timestamped_filename = f"{file_stem}_{timestamp}{file_extension}"

    return timestamped_filename

# save all valid uploaded files into one batch folder
def save_uploaded_files(uploaded_files):

    # create folder
    batch_folder = UPLOAD_FOLDER / f"batch_{create_timestamp()}"
    batch_folder.mkdir(parents=True,exist_ok=True)

    rejected_files = []
    saved_files = []

    for uploaded_file in uploaded_files:
        
        original_filename = uploaded_file.filename

        if original_filename == "":
            continue

        if not allowed_file(original_filename):
            
            rejected_files.append({
                "file_name": original_filename,
                "status": "failed",
                "error": "Unsupported file type",
            })

            continue

        saved_filename = create_timestamped_filename(original_filename)
        saved_path = batch_folder / saved_filename

        uploaded_file.save(saved_path)
        saved_files.append(saved_path)

    return batch_folder, saved_files, rejected_files 


    
# route can handle page loads and from submissions
@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":
        
        if "csv_files" not in request.files:
            return render_template("index.html", error="No file field was submitted")
        
        uploaded_files = request.files.getlist("csv_files")

        batch_folder, saved_files, rejected_files = save_uploaded_files(uploaded_files) 

        if not saved_files:
            return render_template("index.html", error="No valid CSV files were selected")
        
        rules = None
        rules_file = request.files.get("rules_file")

        if rules_file and rules_file.filename != "":

            if not allowed_rules_file(rules_file.filename):
                return render_template("index.hmtl", error="Rules file must be a .json file",)
            
            rules_filename = create_timestamped_filename(rules_file.filename)

            rules_path = batch_folder / rules_filename
            rules_file.save(rules_path)

            try: 
                rules = load_rules_file(rules_path)
            
            except Exception as error:

                return render_template("index.html", error=str(error))
        
        batch_results = process_csv_folder(batch_folder,rules=rules)
        batch_results.extend(rejected_files) 
        
        successful_files = sum(
            1 
            for file_result in batch_results 
            if file_result["status"] == "success"
        )
        
        failed_files = sum(
            1
            for file_result in batch_results 
            if file_result["status"] == "failed"
        )

        return render_template("report.html",batch_results=batch_results, successful_files=successful_files,failed_files=failed_files)
      

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)