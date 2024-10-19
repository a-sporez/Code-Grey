import markdown

def convert_markdown_file(input_file, output_file):
    """
    Convert a Markdown file to an HTML file.
    
    Args:
        input_file (str): Path to the input Markdown file.
        output_file (str): Path to the output HTML file.
    """
    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_text = md_file.read()

    html = markdown.markdown(markdown_text)

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(html)

if __name__ == "__main__":
    input_markdown_file = r'C:\LOVEProjects\Python Scripts\Python-scripts\input\markdown_input.md'  # Specify your input markdown file here
    output_html_file = r'C:\LOVEProjects\Python Scripts\Python-scripts\output\output.html'              # Specify your output html file here
    
    convert_markdown_file(input_markdown_file, output_html_file)
    print(f'Converted {input_markdown_file} to {output_html_file}')