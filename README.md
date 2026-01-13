# 🏎️ F1 History Rewrite Project

> **"What if Formula 1 had always used the modern scoring system?"**

## 📖 About the Project
This project is a Data Science experiment that reprocesses historical Formula 1 data (1950-2009) applying the modern **2024 Scoring System** (25 points for a win).

The goal is to analyze how championship outcomes would change if today's rules were applied to the past, specifically targeting controversial seasons like **2008 (Hamilton vs. Massa)**.

## 🚀 Key Findings
After processing 50+ seasons of data, the script generates detailed Markdown reports for each year.

### The 2008 Verdict 🇧🇷 vs 🇬🇧
In the real world, Lewis Hamilton won by 1 point.
**With the Rewrite (Modern System):**
* **Lewis Hamilton:** 243 pts
* **Felipe Massa:** 240 pts

**Conclusion:** Even with the modern system rewarding victories (25 pts) more heavily, Hamilton's consistency would still secure him the title by a slim 3-point margin.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Library:** Pandas (Data Cleaning, Manipulation, and Aggregation)
* **Input:** CSV Data from Ergast Developer API
* **Output:** Dynamic Markdown reports with aligned tables.

## ⚙️ How it Works (The Logic)
1.  **Ingestion:** Reads raw CSV files (`races`, `results`, `drivers`, `constructors`).
2.  **Cleaning:** Handles messy data, encoding issues (`utf-8-sig`), and inconsistent column spacing.
3.  **Processing:** * Filters seasons chronologically.
    * Discards the original points.
    * Applies a mapping dictionary: `{1: 25, 2: 18, ... 10: 1}`.
4.  **Reporting:** Generates a formatted `.md` file for each season in the `seasons_data/` folder, calculating the new champion dynamically.

## 📦 How to Run
1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the script:
    ```bash
    python main.py
    ```
4.  Check the `seasons_data` folder for the results!

---
*Developed by Guilherme Almeida*