import markdown
from weasyprint import HTML
# Get Pygments default style CSS
from pygments.formatters.html import HtmlFormatter
from pathlib import Path


def markdown_to_pdf(markdown_file_path, output_dir:str=None, output_file_name:str=None)->str:
    """
    This function converts a markdown file to a PDF file. If no output directory is specified, it will use the same
    directory as the markdown file. If the output file name is not specified, it will use the same as the
    markdown filename.
    :param markdown_file_path: The source markdown file path.
    :param output_dir: The output directory to save the PDF file. If not specified, it will use the source file parent dir
    :param output_file_name: The file name of the output PDF file. If not specified, it will use the same as the markdown filename.
    :return: The path of the generated PDF file.
    """
    # get the markdown file parent dir, name, extension
    parent_dir, file_name, file_extension = get_file_name_without_extension(markdown_file_path)
    # build the output html file path
    output_pdf_path = build_output_file_path(parent_dir, file_name, "pdf", output_dir, output_file_name)
    # Read a markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # Convert the markdown file to HTML
    html_body = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code', 'codehilite'])

    pygments_css = HtmlFormatter().get_style_defs('.codehilite')

    # Add some basic CSS for better formatting
    html_with_css = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            code {{ background-color: #f0f0f0; padding: 0.2em; }}
            pre {{ background-color: #f0f0f0; padding: 1em; }}
            blockquote {{ border-left: 3px solid #ccc; margin-left: 0; padding-left: 1em; }}
            
            /* Table styling with borders and separators */
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
                font-size: 0.9em;
            }}
            
            table, th, td {{
                border: 1px solid #ddd;
            }}
            
            th {{
                background-color: #f2f2f2;
                color: #333;
                font-weight: bold;
                text-align: left;
                padding: 10px;
            }}
            
            td {{
                padding: 8px;
                vertical-align: top;
            }}
            
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            
            /* Add Pygments CSS for syntax highlighting */
            {pygments_css}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html_with_css).write_pdf(output_pdf_path)

    return output_pdf_path


def get_file_name_without_extension(file_path: str) -> tuple[str, str, str]:
    """
    This function parses a file path and returns the parent directory, filename without extension, and file extension.
    It raises ValueError, if the file path is empty or invalid
    :param file_path:
    :return:
    """

    try:
        # Check if the file path is empty
        if not file_path:
            raise ValueError("File path cannot be empty")

        # Create a Path object from the input string
        path = Path(file_path)

        # Check if the file exists
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {file_path}")

        # Check if it's actually a file (not a directory)
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Get the parent directory
        parent_directory = str(path.parent)

        # If parent_directory is empty, it's in the current directory
        if parent_directory == '.':
            parent_directory = "."

        # Check if the filename itself is valid
        if not path.name:
            raise ValueError("Invalid filename: filename cannot be empty")

        # Get the filename without extension
        filename = path.stem

        # Get the extension without the leading dot
        extension = path.suffix[1:] if path.suffix else ""

        return parent_directory, filename, extension

    except Exception as e:
        raise ValueError(f"Invalid file path: {file_path}. Error: {str(e)}")


def build_output_file_path(origin_parent_directory: str, origin_file_name: str, output_file_extension: str,
                           output_dir: str = None, output_file_name: str = None) -> str:
    """
    This function builds the output file path.
    :param origin_parent_directory: The parent directory of the source markdown file.
    :param origin_file_name: The file name of the source markdown file.
    :param output_file_extension: The file extension of the generated file.
    :param output_dir: The output directory to save the output file. If not specified, it will use the origin parent directory
    :param output_file_name: The file name of the output file. If not specified, it will use the origin file name
    :return:
    """
    # if no output_dir provided
    if output_dir is None:
        if output_file_name is None:
            output_file_path = f"{origin_parent_directory}/{origin_file_name}.{output_file_extension}"
        # output file name provided
        else:
            output_file_path = f"{origin_parent_directory}/{output_file_name}.{output_file_extension}"
    # if output_dir provided, need to valid the dir path
    else:
        output_dir_path = Path(output_dir)
        # if the given output dir does not exist, create it
        if not output_dir_path.exists():
            output_dir_path.mkdir(parents=True)
        # if the given output dir is not a dir, raise exception.
        if not output_dir_path.is_dir():
            raise ValueError(f"The provided output directory path is not valid(not a directory): {output_dir_path}")
        if output_file_name is None:
            output_file_path = f"{output_dir}/{origin_file_name}.{output_file_extension}"
        # output file name provided
        else:
            output_file_path = f"{output_dir}/{output_file_name}.{output_file_extension}"
    return output_file_path



def markdown_to_html(markdown_file_path: str, output_dir: str = None, output_file_name: str = None):
    """
    This function converts a markdown file to a html file. If no output directory is specified, it will use the same
    directory as the markdown file. If the output file name is not specified, it will use the same as the
    markdown filename.
    :param markdown_file_path: The source markdown file path.
    :param output_dir: The output directory to save the html file. If not specified, it will use the source file parent dir
    :param output_file_name: The file name of the output html file. If not specified, it will use the same as the markdown filename.
    :return: The path of the generated PDF file.
    """

    # get the markdown file parent dir, name, extension
    parent_dir, file_name, file_extension = get_file_name_without_extension(markdown_file_path)
    # build the output html file path
    output_html_path = build_output_file_path(parent_dir, file_name, "html", output_dir, output_file_name)

    # Read markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # Convert markdown to HTML with syntax highlighting
    html_content = markdown.markdown(
        markdown_text,
        extensions=[
            'tables',
            'fenced_code',
            'codehilite'
        ]
    )

    # Get Pygments default style CSS
    pygments_css = HtmlFormatter().get_style_defs('.codehilite')

    # Add the CSS for better formatting, with improved table styling
    html_with_css = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{file_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            code {{ background-color: #f0f0f0; padding: 0.2em; }}
            pre {{ background-color: #f0f0f0; padding: 1em; }}
            blockquote {{ border-left: 3px solid #ccc; margin-left: 0; padding-left: 1em; }}

            /* Table styling with borders and separators */
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
                font-size: 0.9em;
            }}

            table, th, td {{
                border: 1px solid #ddd;
            }}

            th {{
                background-color: #f2f2f2;
                color: #333;
                font-weight: bold;
                text-align: left;
                padding: 10px;
            }}

            td {{
                padding: 8px;
                vertical-align: top;
            }}

            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            /* Add Pygments CSS for syntax highlighting */
            {pygments_css}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Write the HTML file
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_with_css)

    return output_html_path
