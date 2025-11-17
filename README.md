# 🥗 Health & Nutrition Recommendation System

A Python-based project that provides personalized health and nutrition recommendations using user data and structured datasets.  
This system is designed to help individuals understand their health metrics and receive meaningful suggestions to improve their lifestyle, diet, and overall well-being.

---

## 📌 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Screenshots](#screenshots)
- [Dataset Description](#dataset-description)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How the Recommendation System Works](#how-the-recommendation-system-works)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🧠 Introduction

The **Health & Nutrition Recommendation System** analyzes a user’s health details, compares them with a dataset, and provides specific recommendations.  
It is ideal for beginners learning data analysis, machine learning basics, or creating simple recommendation-based applications.

---

## ⭐ Features

✔ User authentication system (Signup + Login)  
✔ Accepts user details such as age, gender, weight, height, diet preferences, and health conditions  
✔ Real-time deficiency & overnutrition detection  
✔ Interactive nutrition dashboard using **Chart.js**  
✔ PDF report generation using **jsPDF**  
✔ Fully responsive UI with modern gradients and glassmorphism  
✔ Easy to customize and extend for ML or API-based recommendations  

---

## 🖼 Screenshots

Add your screenshots inside an **images/** folder in the repository.

### 🔐 Login Page  
<img width="1823" height="906" alt="Screenshot 2025-11-17 112808" src="https://github.com/user-attachments/assets/7dc7a605-d0db-4d8e-ae06-0807ffed6e51" />


### 🏠 Dashboard  
<img width="1880" height="912" alt="Screenshot 2025-11-17 112827" src="https://github.com/user-attachments/assets/73f11ff9-3bd3-48f9-9434-e32751f12567" />


### 📊 Recommendation Page  
<img width="1876" height="913" alt="Screenshot 2025-11-17 113000" src="https://github.com/user-attachments/assets/d85e82f3-4802-48ad-b231-c6a6b36cb401" />


> Make sure your folder structure contains:  
> `Health-and-Nutrition-Recommendation-System/images/`

---

## 📊 Dataset Description

The dataset folder contains:

| File | Description |
|------|-------------|
| **health_nutrition_data.csv** | Nutrition and health dataset used to generate baseline comparisons |
| **users.csv** | Sample user entries for testing |

You can replace these datasets with your custom data for improved accuracy.

---

## 🛠 Tech Stack

- **Python 3.x**  
- **Flask** — Backend web framework  
- **SQLAlchemy** — Database ORM  
- **SQLite / MySQL** (configurable)  
- **Chart.js** — Graphs  
- **jsPDF** — PDF export  
- **Pandas & NumPy** — Data processing  
- **HTML / CSS / JavaScript** — Frontend interface  

---

## 🧩 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YugveerM/Health-and-Nutrition-Recommendation-System.git
cd Health-and-Nutrition-Recommendation-System
```

### 2️⃣ Create a virtual environment (optional)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate   # macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt is missing, install manually:

```bash
pip install flask pandas numpy sqlalchemy
```

---

## ▶ Usage

To start the Flask application:

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000/
```

### The system provides:

1. Secure user login  
2. Input form for nutrition values  
3. Instant health analysis  
4. Chart-based visual comparison of ideal vs. actual intake  
5. Downloadable PDF report  

---

## 📁 Project Structure

```
Health-and-Nutrition-Recommendation-System/
│
├── app.py                           # Flask backend
├── health_nutrition_data.csv         # Dataset
├── users.csv                         # Sample users
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── recommendation.html
│
├── static/
│   ├── style.css                     # (Optional external CSS)
│   ├── script.js                     # (Optional external JS)
│
├── images/                           # Screenshot folder
│   ├── login_page.png
│   ├── dashboard_page.png
│   ├── recommendation_page.png
│
├── requirements.txt
└── README.md
```

---

## 🧬 How the Recommendation System Works

### 1️⃣ User Inputs  
The user enters:

- Age  
- Gender  
- Height & weight  
- Daily calorie intake  
- Protein, carbs, fats  
- Exercise hours  
- Water intake  

### 2️⃣ Data Processing  
- BMI calculation  
- Energy balance  
- Macro-level comparison  
- Hydration & activity analysis  

### 3️⃣ Recommendation Engine  
Based on deficiencies or excessive values, the system suggests:

- Increase/Reduce calories  
- Improve protein, carb, or fat balance  
- Lifestyle fixes  
- Hydration advice  
- BMI improvement tips  

### 4️⃣ Output  
- Clean list of recommendations  
- Bar chart (ideal vs. actual)  
- PDF output with tips + chart  

---

## 🚀 Future Improvements

- Add a **Machine Learning model** for smarter predictions  
- Connect to **Wearable devices / APIs**  
- Build a **mobile app (Flutter / React Native)**  
- Create an **admin dashboard**  
- Add **user history tracking**  
- Create a **diet plan generator**  

---

## 🤝 Contributing

Contributions, suggestions, and improvements are always welcome!

### Steps:

1. Fork this repository  
2. Create a new branch  
3. Add your changes  
4. Commit & push  
5. Create a Pull Request 🎉  

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Yugveer Mehndiratta**  
GitHub: [YugveerM](https://github.com/YugveerM)

---

