from flask import Flask, render_template, request, redirect
from ocr import ocr

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("pict.html", result=None)

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return redirect("/")
    file = request.files["image"]
    if file.filename == "":
        return redirect("/")

    result = ocr(file)
    if result:
        return render_template("pict.html", result=result)

    return render_template("pict.html", result=None)

if __name__ == "__main__":
    app.run(debug=True)
