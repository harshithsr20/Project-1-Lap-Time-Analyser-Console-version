#  Lap Time Analyzer (Console Version)

A Python-based console application to analyze Formula 1–style lap time data using Pandas and NumPy.  
This project focuses on data cleaning, lap analysis, consistency checks, and performance insights from CSV files.

---

##  Features

- Read lap time data from a CSV file
- Clean and preprocess raw race data
- Calculate:
  - Best lap time
  - Average lap time
  - Lap time standard deviation (consistency)
  - Lap-to-lap deltas
  - Tyre degradation over a stint
- Detect and handle outliers
- Group analysis by driver, session, and stint
- Export processed data to text files

---

##  Input

The program takes a CSV file containing lap data with columns such as:
  
- Driver  
- Car    
- LapNumber  
- LapTime  
- TyreCompound  
- Timestamp  
---

##  Processing & Calculations

- Handle missing or invalid values (laps, stints)
- Sort and group data by driver and session
- Compute:
  - Best lap per driver
  - Mean lap time per stint
  - Standard deviation for consistency analysis
  - Lap time degradation using trend analysis
  - Remove outliers using statistical thresholds
   -  Formulate verdicts based on the calculations made
---

## Output

- Console output with lap performance summaries
- Optional `.txt` files containing formatted tables
- Cleaned and enriched DataFrames for further analysis

---

##  Technologies Used

- Python 3
- Pandas
- NumPy

---

## Project Goal

This project is designed to:
- Strengthen data analysis skills
- Practice real-world data cleaning
- Simulate motorsport performance analysis
- Build a foundation for future F1 analytics projects

---

##  Future Improvements

- Graphical visualizations (lap trends, degradation curves)
- Stint-wise lap analysis
- Driver comparison tools
