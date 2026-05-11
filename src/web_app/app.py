from flask import Flask
from flask import render_template # allows flask to load HTML files
from flask import request # allows to read submitted form data

app = Flask(__name__)

# route can handle page loads and from submissions
@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":
        
        uploaded_file = request.files["csv_file"]

        return f"Uploaded file: {uploaded_file.filename}" # temp display


    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)