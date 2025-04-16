from md_convertor.convertor import markdown_to_pdf
import click

from md_convertor.convertor import markdown_to_html


@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               epilog="""
               Examples:\n
               # By default the output format is PDF  \n
               python -m md-convertor sample.md \n   
               # It should work without python -m   \n
               md-convertor sample.md \n
               # Output in html format with option --html    \n
               md-convertor --html sample.md \n
               # Output file in /tmp/out.pdf  \n
               md-convertor sample.md --out_dir /tmp --filename out
                 
               """
               )
@click.argument('markdown_file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--html', '-m', is_flag=True, help='Output in html format, if nothing specified, output pdf')
@click.option('--out_dir', '-o', default=None, help='The parent dir of the output file (default: None)')
@click.option('--filename', '-n', default=None, help='The output file name (default: None)')
def main(markdown_file_path, html, out_dir, filename):
    if html:
        markdown_to_html(markdown_file_path, out_dir, filename)
    else:
        markdown_to_pdf(markdown_file_path, out_dir, filename)

if __name__ == "__main__":
    main()