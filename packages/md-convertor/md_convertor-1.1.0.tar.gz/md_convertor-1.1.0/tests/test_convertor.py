import pytest
from md_convertor.convertor import markdown_to_pdf, get_file_name_without_extension, markdown_to_html

def test_markdown_to_pdf_with_auto_parent_dir_and_file_name():
    markdown_file_path = '../data/sample.md'
    pdf_path = markdown_to_pdf(markdown_file_path)
    print(f"PDF created: {pdf_path}")


def test_markdown_to_pdf_with_custom_name():
    markdown_file_path = '../data/sample.md'
    pdf_path = markdown_to_pdf(markdown_file_path, output_file_name='toto')
    print(f"PDF created: {pdf_path}")


def test_markdown_to_pdf_with_custom_outdir_and_name():
    markdown_file_path = '../data/sample.md'
    pdf_path = markdown_to_pdf(markdown_file_path, output_dir="/tmp", output_file_name='toto')
    print(f"PDF created: {pdf_path}")


def test_markdown_to_pdf_with_custom_non_exist_outdir_and_name():
    markdown_file_path = '../data/sample.md'
    pdf_path = markdown_to_pdf(markdown_file_path, output_dir="/tmp/test_md_to_pdf", output_file_name='toto')
    print(f"PDF created: {pdf_path}")



def test_markdown_to_html():
    markdown_file_path = '../data/sample.md'
    html_path = markdown_to_html(markdown_file_path)
    print(f"HTML created: {html_path}")


def test_get_file_name_without_extension_with_valid_path():
    file_path = '../data/sample.md'
    parent_dir, file_name, extension = get_file_name_without_extension(file_path)
    print(f"Parent dir: {parent_dir}" )
    print(f"File name without extension: {file_name}")
    print(f"Extension: {extension}")


def test_get_file_name_without_extension_with_bad_path():
    file_path = '../data/bad.md'
    with pytest.raises(ValueError) as e:
        parent_dir, file_name, extension = get_file_name_without_extension(file_path)
    print(f"throw exception: {e.value}" )

