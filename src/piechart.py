import pandas as pd
import matplotlib.pyplot as plt
import os

# Construct path to CSV
csv_path = os.path.join("..", "data", "character_line_counts.csv")

# Load the CSV
df = pd.read_csv(csv_path)

# Exclude Homer Simpson
df_side_chars = df[df['character'].str.upper() != 'HOMER']
df_top15 = df_side_chars.nlargest(15, 'dialogue_blocks')


# Function to display actual number on pie slices
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        index = values.index(int(round(pct * total / 100.0)))
        return f'{values[index]}'
    return my_autopct

# Plot pie chart
plt.figure(figsize=(8, 8))
plt.pie(
    df_top15['dialogue_blocks'],
    labels=df_top15['character'],
    autopct=lambda pct: str(int(round(pct * sum(df_top15['dialogue_blocks']) / 100))),
    startangle=140
)
plt.title("Top 15 Side Character Dialogue Counts")
plt.tight_layout()

# Save PNG
plt.savefig(os.path.join("..", "data", "side_character_dialogue_count.png"))
plt.show()
