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


    path = "/".join(dest_path.split('/')[:-1])
    if not os.path.exists(path):
        os.makedirs(path)

    with open(dest_path, 'w') as f:
        f.write(template)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, ".".join(dest_dir_path.split('.')[:-1]) + '.html')
    else:
        for file in os.listdir(dir_path_content):
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
    

def main():
    copyfile_recursive('static', 'public')
    generate_pages_recursive('content', 'template.html', 'public')



if __name__ == '__main__':
    main()