# Simpsons Script Analysis Project

This project contains scripts to process and analyze Simpsons TV show scripts.

---

## 1. `extract.py`

**Description:**  
Extracts the lines spoken by each character from the formatted scripts into a csv file containg the name of the character, dialogue, and the episode it comes from.

**Purpose:**

- Extracts dialogue lines from formatted script files.
- Cleans and formats the text for further analysis.
- Generates CSV files containing characters and their corresponding lines.

---

## 2. `format.py`

**Description:**  
Takes the raw txt files and attempts to unify their format. This is to ensure the `extract.py` script runs as well as it possibly can.

**Purpose:**

- Formats the script text into a consistent style.
- Ensures character names appear on their own lines.
- Keeps stage directions and non-dialogue text separated.

---

## 3. `piechart.py`

**Description:**  
Creates a pie chart of the top 15 speaking side characters.

**Purpose:**

- Reads a CSV file containing character dialogue counts.
- Generates a pie chart showing the dialogue distribution for side characters (excluding Homer Simpson).
- Saves the chart as a PNG image for visualization.

---
