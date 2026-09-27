import shutil, os


def copy_directory(source: str, destination: str) -> None:
    contents = os.listdir(source)
    for entry in contents:
        path = source + '/' + entry
        target = destination + '/' + entry
        if os.path.isfile(path):
            shutil.copy(path, destination)
            print(f'Copied "{path}" to "{target}".')
        if os.path.isdir(path):
            os.mkdir(target)
            print(f'Created "{target}" directory.')
            copy_directory(path, target)

def main() -> None:
    if os.path.exists("public"):
        shutil.rmtree("public")
        print("Removed old public directory.")
    
    os.mkdir("public")
    print("Created new public directory.")
    
    copy_directory("static", "public")

main()
