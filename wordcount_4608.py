# This Python program implements the following use case:
# Write code which takes a command line input of a word doc or docx file and opens it and counts the number of words, and characters in it and prints all

import docx
import sys

def count_words_and_chars(file_path):
    try:
        doc = docx.Document(file_path)
        text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
        words = len(text.split())
        characters = len(text.replace(' ', ''))
        return words, characters
    except Exception as e:
        print(f"Error: {e}")
        return None, None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <file_path>")
    else:
        file_path = sys.argv[1]
        words, characters = count_words_and_chars(file_path)
        if words is not None and characters is not None:
            print(f"Word count: {words}")
            print(f"Character count: {characters}")