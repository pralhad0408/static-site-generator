import os
import shutil
import sys

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node

def generate_page(
        from_path: str, 
        template_path: str, 
        dest_path: str,
        base_path:str,
    ) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html)

    full_html = full_html.replace(
        'href="/',
        f'href="{base_path}',
    )

    full_html = full_html.replace(
        'src="/',
        f'src="{base_path}',
    )

    dest_dir = os.path.dirname(dest_path)

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(
        dir_path_content: str,
        template_path: str,
        dest_dir_path:str,
        base_path: str,
) -> None:
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(content_path):
            if content_path.endswith(".md"):
                dest_path = os.path.splitext(dest_path)[0] + ".html"
                generate_page(
                    content_path, 
                    template_path, 
                    dest_path, 
                    base_path,
                )
        else:
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(
                content_path,
                template_path,
                dest_path,
                base_path,
            )

def copy_static_to_public(src: str, dst: str) -> None:
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)

    copy_directory(src, dst)

def copy_directory(src: str, dst: str) -> None:
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            copy_directory(src_path, dst_path)

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"

    copy_static_to_public("static", "docs")
    generate_pages_recursive(
        "content",
        "template.html",
        "docs",
        base_path,
    )

if __name__ == "__main__":
    main()