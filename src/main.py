import os
import shutil
from block_markdown import markdown_to_html_node, extract_title

def copyfile_recursive(from_file, to_file):
    # If the file we're copying to exists, delete it
    if os.path.exists(to_file):
        print(f"Removing {to_file}")
        shutil.rmtree(to_file)
        if not os.path.isfile(to_file):
            print(f"Creating path to {to_file}")
            os.mkdir(to_file)

    elif not os.path.isfile(from_file):
        print(f"Creating path to {to_file}")
        os.mkdir(to_file)

    if os.path.isfile(from_file):
        print(f"Copying {from_file} to {to_file}")
        shutil.copy(from_file, to_file)
    else:
        for file in os.listdir(from_file):
            copyfile_recursive(os.path.join(from_file, file), os.path.join(to_file, file))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = None
    template = None

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()
    
    node = markdown_to_html_node(markdown)
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", node.to_html())

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    path = os.path.dirname(dest_path)
    with open(dest_path, 'w') as f:
        f.write(template)
    


    

def main():
    copyfile_recursive('static', 'public')
    generate_page('content/index.md', 'template.html', 'public/index.html')



if __name__ == '__main__':
    main()