# 🏎️ F1 History Explorer (Streamlit App)

> **"What if Formula 1 had always used the modern 2024 scoring system?"**

## 📖 About the Project
This is an interactive Data Science Web App developed with **Python** and **Streamlit**. 
It reprocesses historical Formula 1 data (1950-2009) applying the **2024 Scoring System** (25 points for a win) to analyze how championship outcomes would change.

It features a specific focus on the controversial **2008 Season** (Hamilton vs. Massa), allowing users to visualize the race-by-race points evolution.

## 🚀 Features
* **Interactive Dashboard:** Select any season between 1950 and 2009.
* **Race-by-Race Evolution:** Dynamic line chart showing the championship battle.
* **Rewritten Standings:** Detailed table with flags, teams, and recalculated points.
* **Modern Rules:** Applies the current `25-18-15...` point distribution to historical races.

## 🛠️ Tech Stack
* **Python 3.11+**
* **Streamlit** (Frontend & Interactivity)
* **Pandas** (Data Processing)
* **Ergast Developer API** (Source Data - CSV)

## 📦 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/GuilhermeAlmeida10000/f1-history-rewrite.git](https://github.com/GuilhermeAlmeida10000/f1-history-rewrite.git)
    cd f1-history-rewrite
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App:**
    ```bash
    python -m streamlit run app.py
    ```
    The app will open in your browser at `http://localhost:8501`.

---
*Developed by Guilherme Almeida*