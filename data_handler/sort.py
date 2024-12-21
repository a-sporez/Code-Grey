import csv
import os
from datetime import datetime

# File paths
input_file = "input/data.csv"
output_dir = "output"
execution_date = datetime.now().strftime("%Y-%m-%d")
output_file = os.path.join(output_dir, f"database_{execution_date}.md")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def read_csv(filepath):
    """Reads CSV data into a list of dictionaries."""
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader), reader.fieldnames

def generate_markdown_table(data, headers):
    """Generates a properly formatted Markdown table."""
    table = []
    table.append("| " + " | ".join(headers) + " |")
    table.append("|" + " | ".join(["-" * len(header) for header in headers]) + "|")
    for row in data:
        row_data = []
        for header in headers:
            value = row.get(header, "").replace("\n", " ").strip()
            if header == "Profile URL" and value:  # Convert URL to clickable Markdown link
                value = f"[Profile]({value})"
            row_data.append(value)
        table.append("| " + " | ".join(row_data) + " |")
    return "\n".join(table)

def sort_data(data, sort_key):
    """Sorts data by the specified key."""
    return sorted(data, key=lambda x: x.get(sort_key, ""))

def reorder_columns(data, primary_column):
    """Reorders the columns to move the primary_column to the first position."""
    reordered_data = []
    for row in data:
        reordered_row = {key: row[key] for key in row}  # Copy the original row
        reordered_row = {primary_column: row[primary_column]} | reordered_row  # Move primary column to front
        reordered_data.append(reordered_row)
    return reordered_data

def write_markdown(data, headers):
    """Writes the Markdown file with alphabetically and date-sorted tables."""
    # Generate the table sorted alphabetically
    alphabetically_sorted_data = sort_data(data, "Name")  # Assuming "Name" is the field for alphabetical sorting
    alphabetically_sorted_table = generate_markdown_table(alphabetically_sorted_data, headers)

    # Generate the table sorted by Date of death and reorder columns
    date_sorted_data = sort_data(data, "Date of death")
    reordered_date_sorted_data = reorder_columns(date_sorted_data, "Date of death")  # Move date column to the front
    reordered_headers = ["Date of death"] + [header for header in headers if header != "Date of death"]
    reordered_table = generate_markdown_table(reordered_date_sorted_data, reordered_headers)

    # Write the Markdown file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("# Database\n\n")
        file.write("## **Table Sorted Alphabetically**\n\n")
        file.write(alphabetically_sorted_table)
        file.write("\n\n---\n\n")
        file.write("## **Table Sorted by Date of Death**\n\n")
        file.write(reordered_table)
        file.write("\n\n")
    print(f"Markdown table saved to '{output_file}'")

# Main script execution
if __name__ == "__main__":
    print("Reading CSV data...")
    csv_data, headers = read_csv(input_file)

    print("Generating Markdown table...")
    write_markdown(csv_data, headers)

    print("Done!")