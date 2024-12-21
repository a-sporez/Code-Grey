import csv
import os
import matplotlib.pyplot as plt

# Specify the input CSV file and output directory.
input_file = "input/data.csv"  # The path to the input CSV file containing data.
output_dir = "output"  # The directory where output files will be saved.

# Ensure the output directory exists; if it doesn't, create it.
os.makedirs(output_dir, exist_ok=True)

def read_csv(filepath):
    """
    Reads CSV data into a list of dictionaries and extracts headers.

    Parameters:
        filepath (str): The path to the CSV file.

    Returns:
        tuple: A list of dictionaries representing the rows of the CSV file,
               and a list of fieldnames (column headers).
    
    Method:
        - Open the CSV file with UTF-8 encoding to handle special characters.
        - Use `csv.DictReader` to parse the CSV into dictionaries where keys are column headers.
        - Collect all rows into a list and return it along with the column headers.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Parse the CSV file as dictionaries.
        return list(reader), reader.fieldnames  # Return all rows and the column headers.

def analyze_column_values(data, headers):
    """
    Analyzes the frequency of values in each column of the dataset.

    Parameters:
        data (list of dict): A list of dictionaries representing rows of the CSV file.
        headers (list of str): The list of column headers from the CSV file.

    Returns:
        dict: A dictionary where keys are column headers and values are dictionaries
              mapping unique values to their counts in that column.
    
    Method:
        - Create a `column_stats` dictionary where each key is a column header
          and its value is an empty dictionary for storing value counts.
        - Iterate through each row in the dataset.
            - For each column header, retrieve the corresponding cell value.
            - Replace missing or empty values with the string "Unknown".
            - Increment the count of the value in the corresponding column's dictionary.
        - Return the complete statistics dictionary with value counts per column.
    """
    # Initialize statistics dictionary with column headers.
    column_stats = {header: {} for header in headers}
    
    # Loop through each row in the dataset.
    for row in data:
        # Process each column for the current row.
        for header in headers:
            # Retrieve the value for the column, defaulting to "Unknown" if absent.
            value = row.get(header, "Unknown").strip()
            # Increment the count for the value in the column's stats dictionary.
            column_stats[header][value] = column_stats[header].get(value, 0) + 1
    
    # Return the completed statistics.
    return column_stats

def generate_bar_chart(column_name, data_counts, output_dir):
    """
    Generates a customized vertical bar chart for the column data.

    Parameters:
    - column_name (str): The name of the column being visualized.
    - data_counts (dict): A dictionary where keys are unique values from the column and values are their frequencies.
    - output_dir (str): The directory where the chart image will be saved.

    Returns:
    - chart_path (str): The file path of the saved chart image.
    """
    # Extract labels (unique values) and their corresponding counts (frequencies).
    labels = list(data_counts.keys())
    counts = list(data_counts.values())

    # Set up the figure size; (3, 2) makes it small. Adjust numbers to resize.
    plt.figure(figsize=(6, 4))

    # Set the background color of the entire figure (grey in this case).
    plt.gcf().set_facecolor("lightgrey")

    # Create the bar chart:
    # - Bars are olive green for better visibility
    # - Edge color is black for a clear boundary
    plt.bar(labels, counts, color='olive', edgecolor='black')

    # Add labels for the x-axis and y-axis to make the chart informative.
    plt.xlabel("Categories")  # You can change "Categories" to something specific to your data.
    plt.ylabel("Count")       # Change "Count" if you need a different term.

    # Add a title, e.g., "Distribution of Age Groups" for better context.
    plt.title(f"Distribution of {column_name}")

    # Rotate the x-axis labels slightly for better readability, especially for long text.
    # 'fontsize=8' reduces label size for better alignment in a smaller chart.
    plt.xticks(rotation=45, ha='right', fontsize=8)

    # Reduce the size of y-axis tick labels for consistency.
    plt.yticks(fontsize=8)

    # Tight layout minimizes padding and adjusts the chart to fit the smaller size well.
    plt.tight_layout()

    # Save the chart as a PNG file in the output directory:
    # - 'dpi=100' makes the resolution slightly lower (smaller file size).
    # - Adjust DPI higher (e.g., 150 or 200) for higher-quality images if needed.
    chart_path = os.path.join(output_dir, f"{column_name}_bar_chart.png")
    plt.savefig(chart_path, dpi=100)

    # Close the plot to free up memory when generating multiple charts.
    plt.close()

    # Return the path of the saved chart for reference.
    return chart_path

def generate_markdown(stats, headers):
    """
    Generates a Markdown report with statistics and embedded bar charts for each column.

    Parameters:
        stats (dict): A dictionary of column statistics, where keys are column names
                      and values are dictionaries mapping unique values to their counts.
        headers (list of str): A list of column headers (keys in the `stats` dictionary).

    Returns:
        str: A string containing the Markdown-formatted report with statistics and
             links to bar charts for visual representation.
    
    Method:
        - Start the Markdown content with a header and initialize a list to store lines.
        - Iterate over each column (header):
            - Calculate the number of unique values in the column.
            - Skip processing for columns with more than 30 unique values.
            - Add a Markdown table with the value counts for each unique entry in the column.
            - Generate a bar chart for the column's value distribution and embed its link
              into the Markdown content.
        - Join all lines into a single Markdown string and return it.
    """
    markdown = ["# Column Statistics and Bar Charts\n"]  # Start the Markdown document.

    # Process each column header.
    for header in headers:
        unique_values = len(stats[header])  # Count the number of unique values.
        
        # Skip columns with too many unique values to avoid clutter.
        if unique_values > 30:
            print(f"Skipping column '{header}' with {unique_values} unique values.")
            continue

        # Add a header and table to the Markdown for the current column.
        markdown.append(f"## {header}\n")
        markdown.append("| Value | Count |")
        markdown.append("|-------|-------|")
        
        # Populate the table rows, sorted by count in descending order.
        for value, count in sorted(stats[header].items(), key=lambda x: x[1], reverse=True):
            markdown.append(f"| {value} | {count} |")
        markdown.append("\n")  # Add spacing between sections.

        # Generate and embed the bar chart for the column.
        chart_file = generate_bar_chart(header, stats[header], output_dir)
        markdown.append(f"![{header} Distribution]({chart_file})\n")  # Markdown for image.

    # Combine all Markdown lines into a single string and return it.
    return "\n".join(markdown)

def write_markdown(markdown_content):
    """
    Writes the generated Markdown report to a file in the output directory.

    Parameters:
        markdown_content (str): The content of the Markdown report.

    Returns:
        None
    
    Method:
        - Define the output file path as "output/column_stats.md".
        - Open the file in write mode with UTF-8 encoding.
        - Write the Markdown content to the file.
        - Print a success message indicating the location of the saved report.
    """
    # Define the output file path.
    output_file = os.path.join(output_dir, "column_stats.md")
    
    # Write the Markdown content to the file.
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    
    # Inform the user that the Markdown report was successfully saved.
    print(f"Markdown report with charts saved to '{output_file}'")

# Main script execution block.
if __name__ == "__main__":
    """
    Main script logic:
        - Reads the CSV data and extracts headers.
        - Analyzes the frequency of values for each column in the dataset.
        - Generates a Markdown report with statistics and embedded bar charts.
        - Saves the Markdown report to a file.
    """
    # Read the input CSV file and extract data and headers.
    print("Reading CSV data...")
    csv_data, headers = read_csv(input_file)

    # Analyze the frequency of values in each column.
    print("Analyzing column values...")
    column_stats = analyze_column_values(csv_data, headers)

    # Generate a Markdown report with statistics and charts.
    print("Generating Markdown report...")
    markdown_content = generate_markdown(column_stats, headers)
    
    # Write the generated Markdown report to an output file.
    write_markdown(markdown_content)

    # Indicate that the process is complete.
    print("Done!")