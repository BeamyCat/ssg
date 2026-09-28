import re
from blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    return re.search(r"(?<!#)# (.*)", markdown).group(1)


def generate_page(from_path: str, template_path: str, to_path: str) -> None:
    print(f'Generating page from "{from_path}" to "{to_path}" using "{template_path}"')
    source = open(from_path).read()
    template = open(template_path).read()
    
    title = extract_title(source)
    content = markdown_to_html_node(source).to_html()
    
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    
    open(to_path, 'w').write(page)
    print(f'Generated "{to_path}"')
    
