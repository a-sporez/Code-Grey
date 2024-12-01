import pandas as pd

# Load CSV file
file_path = "input/table.csv"  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Export to Markdown
markdown_table = data.to_markdown(index=False)

# Save to a file (optional)
with open("table.md", "w") as f:
    f.write(markdown_table)

print("Markdown table saved to 'table.md'.")