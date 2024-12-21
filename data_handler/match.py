import csv
from difflib import SequenceMatcher
import os

# Define input CSV file paths
input_file_1 = "input/data1.csv"
input_file_2 = "input/data2.csv"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Define similarity threshold (e.g., 0.85 means 85% similarity)
SIMILARITY_THRESHOLD = 0.85

def read_csv(filepath):
    """
    Reads a CSV file and returns the data as a list of dictionaries.
    Parameters:
        filepath (str): Path to the CSV file.
    Returns:
        list of dict: The data from the CSV file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader), reader.fieldnames

def preprocess_name(name):
    """
    Normalizes a name by trimming whitespace and converting it to lowercase.
    Parameters:
        name (str): The name to preprocess.
    Returns:
        str: The normalized name.
    """
    return name.strip().lower()

def calculate_similarity(name1, name2):
    """
    Calculates the similarity between two strings using SequenceMatcher.
    Parameters:
        name1 (str): First name string.
        name2 (str): Second name string.
    Returns:
        float: Similarity ratio (0 to 1).
    """
    return SequenceMatcher(None, name1, name2).ratio()

def compare_names(data1, data2, key):
    """
    Compares names from two datasets and identifies identical and similar matches.
    Parameters:
        data1 (list of dict): First dataset.
        data2 (list of dict): Second dataset.
        key (str): The column key containing names to compare.
    Returns:
        list of dict: Matches containing both identical and similar pairs with similarity scores.
    """
    matches = []

    for entry1 in data1:
        name1 = preprocess_name(entry1[key])
        for entry2 in data2:
            name2 = preprocess_name(entry2[key])

            similarity = calculate_similarity(name1, name2)

            # Add identical or similar matches with their similarity scores
            if similarity >= SIMILARITY_THRESHOLD:
                matches.append({
                    "name_1": entry1[key],
                    "name_2": entry2[key],
                    "similarity": similarity,
                    "row_1": entry1,
                    "row_2": entry2,
                })

    return matches

def write_results(matches, key):
    """
    Writes the comparison results to a CSV file and prints them to the console.
    Parameters:
        matches (list of dict): List of matches with both identical and similar pairs.
        key (str): The column key containing names.
    """
    output_file = os.path.join(output_dir, "name_matches.csv")
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        fieldnames = [f"{key}_1", f"{key}_2", "Similarity", "Row_1", "Row_2"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for match in matches:
            # Write to the CSV file
            writer.writerow({
                f"{key}_1": match["name_1"],
                f"{key}_2": match["name_2"],
                "Similarity": f"{match['similarity']:.2f}",
                "Row_1": match["row_1"],
                "Row_2": match["row_2"],
            })

            # Print to the console
            print(f"Match found:")
            print(f"  {key}_1: {match['name_1']}")
            print(f"  {key}_2: {match['name_2']}")
            print(f"  Similarity: {match['similarity']:.2f}")
            print(f"  Row_1: {match['row_1']}")
            print(f"  Row_2: {match['row_2']}")
            print("-" * 40)

    print(f"Matches saved to '{output_file}'")

# Main script execution
if __name__ == "__main__":
    print("Reading CSV files...")
    data1, headers1 = read_csv(input_file_1)
    data2, headers2 = read_csv(input_file_2)

    # Define the column key for name comparison
    name_key = "Name"  # Adjust this based on your CSV column headers

    print(f"Comparing names in column '{name_key}'...")
    matches = compare_names(data1, data2, name_key)

    print("Writing results...")
    write_results(matches, name_key)

    print("Done!")