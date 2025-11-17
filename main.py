from flask import Flask, render_template, request, redirect, url_for, session, make_response
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import webbrowser
import threading
import os
import json
import re
from io import BytesIO

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

# -----------------------
# User Management
# -----------------------
USER_FILE = "users.csv"
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index=False)

def load_users():
    try:
        df = pd.read_csv(USER_FILE)
        return dict(zip(df.username, df.password))
    except Exception:
        return {}

def add_user(username, password):
    df = pd.read_csv(USER_FILE)
    if username in df["username"].values:
        return False
    new_row = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

# -----------------------
# Dataset & Model
# -----------------------
DATA_FILE = "health_nutrition_data.csv"
try:
    data = pd.read_csv(DATA_FILE)
    print("✅ Dataset loaded successfully!")
except Exception as e:
    print("⚠ Error loading dataset:", e)
    raise SystemExit("Dataset required: health_nutrition_data.csv")

if "gender" in data.columns:
    data["gender"] = data["gender"].map({"male": 0, "female": 1})

expected_cols = [
    "age", "gender", "weight_kg", "height_cm", "daily_calories",
    "protein_g", "carbs_g", "fat_g", "exercise_hours_per_week", "water_liters_per_day"
]

def classify_status(row):
    if (row["protein_g"] < 50) or (row["carbs_g"] < 130) or (row["fat_g"] < 35) or (row["daily_calories"] < 1500):
        return 1
    elif (row["daily_calories"] > 4000) or (row["protein_g"] > 180) or (row["fat_g"] > 100) or (row["weight_kg"] > 100):
        return 2
    else:
        return 0

data["nutrition_status"] = data.apply(classify_status, axis=1)

X = data[expected_cols]
y = data["nutrition_status"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)
print("✅ Model trained successfully!")

# -----------------------
# Nutrition Recommendation Logic
# -----------------------
def recommend_nutrition(user_input):
    # Rename keys to match model input
    user_input_fixed = {
        "age": user_input.get("age", 0),
        "gender": 0 if str(user_input.get("gender", "male")).lower() == "male" else 1,
        "weight_kg": user_input.get("weight_kg", 0),
        "height_cm": user_input.get("height_cm", 0),
        "daily_calories": user_input.get("daily_calories", 0),
        "protein_g": user_input.get("protein_g", 0),
        "carbs_g": user_input.get("carbs_g", 0),
        "fat_g": user_input.get("fat_g", 0),
        "exercise_hours_per_week": user_input.get("exercise_hours", 0),
        "water_liters_per_day": user_input.get("water_liters", 0)
    }

    user_df = pd.DataFrame([user_input_fixed])
    user_scaled = scaler.transform(user_df[expected_cols])
    pred = model.predict(user_scaled)[0]

    recommendations = []
    bmi = round(user_input["weight_kg"] / ((user_input["height_cm"]/100) ** 2), 2)
    if bmi < 18.5:
        recommendations.append(f"⚠ Your BMI is {bmi} — underweight. Include calorie-dense nutritious foods.")
    elif bmi > 25:
        recommendations.append(f"⚠ Your BMI is {bmi} — overweight. Focus on balanced calorie control and more activity.")
    else:
        recommendations.append(f"✅ Your BMI is {bmi}, within the healthy range.")

    if pred == 1:
        recommendations.append("🧾 Your diet seems nutrient-deficient. Focus on improving protein, fats, and calorie intake.")
        if user_input["protein_g"] < 50:
            recommendations.append("🍳 Protein: Low intake detected. Increase protein to 1.0–1.2g/kg body weight. Add eggs, lentils, paneer, tofu, or fish.")
        if user_input["fat_g"] < 35:
            recommendations.append("🥑 Healthy Fats: Add almonds, walnuts, chia seeds, olive oil, or avocado. Necessary for hormone balance and energy.")
        if user_input["daily_calories"] < 1500:
            recommendations.append("🍽 Calories: Too low — Add snacks like smoothies, nuts, or banana with peanut butter.")
    elif pred == 2:
        recommendations.append("🧾 Your diet shows signs of overnutrition. Reduce portion sizes and refined food.")
        if user_input["daily_calories"] > 4000:
            recommendations.append("🥗 Calories: Too high. Lower fried, processed, and late-night meals. Add salads, fruits, and high-fiber foods.")
        if user_input["fat_g"] > 100:
            recommendations.append("🍟 Fats: Too much saturated fat. Avoid butter, fried food, or creamy desserts. Prefer olive oil and nuts in moderation.")
    else:
        recommendations.append("🌟 You appear balanced nutritionally. Maintain variety: whole grains, lean proteins, fruits, and vegetables.")

    return pred, recommendations

IDEAL = {"protein": 70, "carbs": 250, "fat": 60}

# -----------------------
# PDF Generation Function
# -----------------------
def generate_pdf(recommendations, user_input):
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont('DejaVuSans-Bold', 22)
    c.setFillColor(HexColor('#00bfff'))
    c.drawCentredString(300, 760, "Health & Nutrition Report")

    c.setFont('DejaVuSans', 12)
    c.setFillColor(HexColor('#444444'))
    c.drawCentredString(300, 740, "Personalized Summary & Recommendations")

    y = 710
    c.setFont('DejaVuSans-Bold', 14)
    c.setFillColor(HexColor('#00d4ff'))
    c.drawString(50, y, "User Summary:")
    y -= 20

    c.setFont('DejaVuSans', 12)
    c.setFillColor(HexColor('#000000'))

    user_summary = [
        f"Age: {user_input.get('age', 'N/A')}",
        f"Gender: {user_input.get('gender', 'N/A').capitalize()}",
        f"Weight: {user_input.get('weight_kg', 'N/A')} kg",
        f"Height: {user_input.get('height_cm', 'N/A')} cm",
        f"Calories per day: {user_input.get('daily_calories', 'N/A')} kcal",
        f"Protein intake: {user_input.get('protein_g', 'N/A')} g",
        f"Carbohydrates: {user_input.get('carbs_g', 'N/A')} g",
        f"Fat intake: {user_input.get('fat_g', 'N/A')} g",
        f"Exercise: {user_input.get('exercise_hours', 'N/A')} hrs/week",
        f"Water: {user_input.get('water_liters', 'N/A')} L/day",
    ]

    for line in user_summary:
        c.drawString(70, y, f"• {line}")
        y -= 18

    y -= 15
    c.setStrokeColor(HexColor('#00bfff'))
    c.line(50, y, 560, y)
    y -= 25

    c.setFont('DejaVuSans-Bold', 14)
    c.setFillColor(HexColor('#00d4ff'))
    c.drawString(50, y, "Personalized Recommendations:")
    y -= 25

    highlight_words = ["Increase", "Reduce", "Add", "Avoid", "Lower", "Balanced", "Overnutrition", "Deficiency", "Focus", "Improve"]

    for i, rec in enumerate(recommendations, 1):
        if y < 100:
            c.showPage()
            c.setFont('DejaVuSans', 12)
            y = 750

        c.setFont('DejaVuSans-Bold', 13)
        c.setFillColor(HexColor('#00d4ff'))
        c.drawString(50, y, f"Tip {i}")
        y -= 20

        text_obj = c.beginText(60, y)
        text_obj.setFont('DejaVuSans', 11)
        text_obj.setFillColor(HexColor('#000000'))

        words = re.split(r'(\s+)', rec)
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in highlight_words:
                text_obj.setFont('DejaVuSans-Bold', 11)
                text_obj.setFillColor(HexColor('#00bfff'))
            else:
                text_obj.setFont('DejaVuSans', 11)
                text_obj.setFillColor(HexColor('#000000'))
            text_obj.textOut(word)
        c.drawText(text_obj)
        y -= 60

    c.save()
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename="health_report.pdf"'
    return response

# -----------------------
# Routes
# -----------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            return render_template("signup.html", error="⚠ Username and password required")
        if add_user(username, password):
            return redirect(url_for("login"))
        else:
            return render_template("signup.html", error="⚠ Username already exists!")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="❌ Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    recommendations = []
    user_input = {}
    nutrition_status = None

    if request.method == "POST":
        try:
            user_input = {
                "age": int(request.form.get("age", 0)),
                "gender": request.form.get("gender", "male"),
                "weight_kg": float(request.form.get("weight_kg", 0.0)),
                "height_cm": float(request.form.get("height_cm", 0.0)),
                "daily_calories": int(request.form.get("daily_calories", 0)),
                "protein_g": int(request.form.get("protein_g", 0)),
                "carbs_g": int(request.form.get("carbs_g", 0)),
                "fat_g": int(request.form.get("fat_g", 0)),
                "exercise_hours": float(request.form.get("exercise_hours", 0.0)),
                "water_liters": float(request.form.get("water_liters", 0.0))
            }
            nutrition_status, recommendations = recommend_nutrition(user_input)
            session["recommendations"] = recommendations
            session["user_input"] = user_input
        except Exception as e:
            recommendations = [f"⚠ Error processing input: {str(e)}"]
            user_input = {}

    return render_template(
        "index.html",
        recommendations=recommendations,
        user_input=user_input,
        username=session.get("user"),
        ideal=IDEAL,
        nutrition_status=nutrition_status,
        user_input_json=json.dumps(user_input) if user_input else "null",
        ideal_json=json.dumps(IDEAL)
    )

@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    recommendations = session.get("recommendations", [])
    user_input = session.get("user_input", {})
    return generate_pdf(recommendations, user_input)

# -----------------------
# Auto Open Browser
# -----------------------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/login")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
