@app.route("/run-ocr", methods=["POST"])
def run_ocr():
    if "image" not in request.files:
        return redirect("/")
    file = request.files["image"]
    if file.filename == "":
        return redirect("/")

    result = ocr(file)

    # 🟢 Also fetch total_income, total_expense, and amount_left again
    user_id = session['user_id']
    total_income, total_expense, amount_left = get_user_financials(session['user_id'])

    return render_template("analysis.html", 
                           result=result, 
                           total_income=total_income, 
                           total_expense=total_expense, 
                           amount_left=amount_left)
