import tempfile
import re
from tqdm import tqdm
from pathlib import Path
import subprocess
import argparse

# Install beautifulsoup4 and ebooklib packages
subprocess.run(["pip", "install", "beautifulsoup4", "ebooklib"])

from bs4 import BeautifulSoup
import bs4
from ebooklib import epub

def _convert_file_path(path, original_name):
    path_obj = Path(path)
    new_name = f"Bionic_{original_name}"
    new_path = path_obj.with_name(new_name)
    return str(new_path)

def convert_to_bionic_str(soup: BeautifulSoup, s: str):
    new_parent = soup.new_tag("span")
    words = re.split(r'.,;:!?-|\s', s)
    for word in words:
        if len(word) >= 2:
            mid = (len(word) // 2) + 1
            first_half, second_half = word[:mid], word[mid:]
            b_tag = soup.new_tag("b")
            b_tag.append(soup.new_string(first_half))
            new_parent.append(b_tag)
            new_parent.append(soup.new_string(second_half + " "))
        else:
            new_parent.append(soup.new_string(word + " "))
    return new_parent

def convert_to_bionic(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    for e in soup.descendants:
        if isinstance(e, bs4.element.Tag):
            if e.name == "p":
                children = list(e.children)
                for child in children:
                    if isinstance(child, bs4.element.NavigableString):
                        if len(child.text.strip()):
                            child.replace_with(convert_to_bionic_str(soup, child.text))
    return str(soup).encode()

def convert_book(book_path):
    original_name = Path(book_path).name
    source = epub.read_epub(book_path)
    
    for item in tqdm(source.items, desc="Converting to Bionic"):
        if item.media_type == "application/xhtml+xml":
            content = item.content.decode('utf-8')
            item.content = convert_to_bionic(content)
    
    converted_path = _convert_file_path(book_path, original_name)
    epub.write_epub(converted_path, source)
    
    print(f"Conversion completed! File saved as {converted_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert an EPUB file to a Bionic Reading-like format.")
    parser.add_argument("book_path", help="The path to the EPUB file to convert.")
    args = parser.parse_args()
    
    convert_book(args.book_path)

if __name__ == "__main__":
    main()