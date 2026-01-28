import matplotlib.pyplot as plt
import numpy as np

# Data from the R output image
topics = [1, 2, 3, 4, 5, 6, 7, 8]
topic_labels = [
    "Themselves", 
    "Core Family", 
    "Non-Core Family", 
    "Location", 
    "Object", 
    "Event", 
    "Emotion", 
    "Opinion"
]

bart_counts = [33, 48, 83, 14, 39, 12, 18, 53]
lisa_counts = [9, 87, 58, 8, 40, 6, 24, 68]
marge_counts = [5, 97, 38, 14, 27, 10, 35, 74]

x = np.arange(len(topics))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 6))
rects1 = ax.bar(x - width, bart_counts, width, label='Bart')
rects2 = ax.bar(x, lisa_counts, width, label='Lisa')
rects3 = ax.bar(x + width, marge_counts, width, label='Marge')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Line Counts')
ax.set_title('Topic Distribution by Character')
ax.set_xticks(x)
ax.set_xticklabels(topic_labels, rotation=45, ha="right")
ax.legend()

fig.tight_layout()

output_path = "topic_distribution.png"
plt.savefig(output_path, dpi=300)
print(f"Chart saved to {output_path}")
