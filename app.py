
# app.py

import os
import sqlite3
import pickle

from flask import Flask, render_template, request, redirect, url_for, flash
from database import create_tables, get_connection

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-secret"

# Find the model file in the same folder as app.py.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "dropout_model.pkl")

# Load the trained model once when the application starts.
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

create_tables()


def predict_risk(attendance, marks, assignments, previous_performance):
    """
    Use the trained Logistic Regression model to estimate risk.

    This model was trained on synthetic practice data.
    Its predictions are for demonstration only.
    """

    # Keep the same input order used during model training.
    features = [[
        attendance,
        marks,
        assignments,
        previous_performance
    ]]

    # Predict the probability of the class labelled 1.
    dropout_probability = model.predict_proba(features)[0][1]

    # Convert the probability into a display category.
    # These thresholds are chosen for demonstration, not validated.
    if dropout_probability >= 0.70:
        risk = "High Risk"
    elif dropout_probability >= 0.40:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return risk, round(dropout_probability * 100, 2)


@app.route("/")
def home():
    connection = get_connection()

    students = connection.execute(
        "SELECT * FROM students ORDER BY name"
    ).fetchall()

    connection.close()

    student_list = []

    for student in students:
        student_data = dict(student)

        risk, probability = predict_risk(
            student["attendance"],
            student["internal_marks"],
            student["assignment_completion"],
            student["previous_performance"]
        )

        student_data["risk"] = risk
        student_data["dropout_probability"] = probability

        student_list.append(student_data)

    total_students = len(student_list)
    high_risk_count = sum(
        s["risk"] == "High Risk" for s in student_list
    )
    medium_risk_count = sum(
        s["risk"] == "Medium Risk" for s in student_list
    )
    low_risk_count = sum(
        s["risk"] == "Low Risk" for s in student_list
    )

    return render_template(
        "dashboard.html",
        students=student_list,
        total_students=total_students,
        high_risk_count=high_risk_count,
        medium_risk_count=medium_risk_count,
        low_risk_count=low_risk_count
    )


@app.route("/add-student", methods=["POST"])
def add_student():
    usn = request.form.get("usn", "").strip().upper()
    name = request.form.get("name", "").strip()

    if len(usn) != 10 or not usn.isalnum():
        flash("USN must contain exactly 10 letters or numbers.", "error")
        return redirect(url_for("home"))

    if not name:
        flash("Please enter the student's name.", "error")
        return redirect(url_for("home"))

    try:
        attendance = float(request.form.get("attendance", ""))
        marks = float(request.form.get("internal_marks", ""))
        assignments = float(
            request.form.get("assignment_completion", "")
        )
        previous = float(
            request.form.get("previous_performance", "")
        )
    except (ValueError, TypeError):
        flash("Enter valid numbers in all performance fields.", "error")
        return redirect(url_for("home"))

    values = [attendance, marks, assignments, previous]

    if any(value < 0 or value > 100 for value in values):
        flash("All scores must be between 0 and 100.", "error")
        return redirect(url_for("home"))

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO students (
                usn, name, attendance, internal_marks,
                assignment_completion, previous_performance
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            usn, name, attendance, marks, assignments, previous
        ))

        connection.commit()
        flash("Student added successfully!", "success")

    except sqlite3.IntegrityError:
        flash("This USN already exists or the data is invalid.", "error")

    finally:
        connection.close()

    return redirect(url_for("home"))


@app.route("/delete-student/<usn>", methods=["POST"])
def delete_student(usn):
    connection = get_connection()

    connection.execute(
        "DELETE FROM students WHERE usn = ?",
        (usn,)
    )

    connection.commit()
    connection.close()

    flash("Student record deleted.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
