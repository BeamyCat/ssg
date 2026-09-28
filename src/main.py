import shutil, os, sys
from generate import generate_page


basepath = "/"

def copy_directory(source: str, destination: str) -> None:
    contents = os.listdir(source)
    for entry in contents:
        path = source + '/' + entry
        target = destination + '/' + entry
        if os.path.isfile(path):
            shutil.copy(path, destination)
            print(f'Copied "{path}" to "{target}".')
        if os.path.isdir(path):
            if not os.path.exists(target):
                os.mkdir(target)
                print(f'Created "{target}" directory.')
            copy_directory(path, target)


def generate_pages_recursive(source: str, destination: str) -> None:
    contents = os.listdir(source)
    for entry in contents:
        path = source + '/' + entry
        target = destination + '/' + entry
        if os.path.isfile(path) and path.endswith('.md'):
            generate_page(path, "template.html", target.replace('.md', '.html'), basepath)
        if os.path.isdir(path):
            if not os.path.exists(target):
                os.mkdir(target)
                print(f'Created "{target}" directory.')
            generate_pages_recursive(path, target)


def main() -> None:
    global basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    if os.path.exists("docs"):
        shutil.rmtree("docs")
        print("Removed old docs directory.")
    
    os.mkdir("docs")
    print("Created new docs directory.")
    
    copy_directory("static", "docs")
    
    generate_pages_recursive("content", "docs")

main()
