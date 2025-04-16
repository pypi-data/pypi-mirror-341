import argparse 
def num_letters(file_path):
    """" 
    Counts the number of letters in the document
    """
    try:
        with open(file_path, 'r') as file:
            content=file.read()   #Read the file content
            return len(content) 
    except FileNotFoundError:
        print(f"There is no '{file_path}'.\nTry entering the directory of the file")
        return 0

def num_bytes(file_path):
    """
    Counts the number of bytes in the document
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read() #Read the file content
            return len(content)
    except FileNotFoundError:
        print(f"There is no '{file_path}'\nTry entering the directory of the file")
        return 0

def num_lines(file_path):
    """Counts the numbers of lines in the document"""
    try:
        with open(file_path,'r') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        print(f"There is no '{file_path}'\nTry entering the directory of the file") 
        return 0   


def num_words(file_path):
    """
    Counts the number of words in the document
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read() #Read the file content
            words = content.split()
            return len(words)
    except FileNotFoundError:
        print(f"There is no '{file_path}'\nTry entering the directory of the file")
        return 0
def main():
    parser = argparse.ArgumentParser(description="Check all the information about a text file")  
    parser.add_argument("file_path", help="Path to the file")
    parser.add_argument("-l", "--lines", action="store_true", help="Count lines")
    parser.add_argument("-w", "--words", action="store_true", help="Count words")
    parser.add_argument("-b", "--bytes", action="store_true", help="Count bytes")
    parser.add_argument("-c", "--chars", action="store_true", help="Count characters")  

    args = parser.parse_args()

    if not (args.lines or args.words or args.bytes or args.chars):
        print("Displaying all information about the file")
        print(f"Number of lines: {num_lines(args.file_path)}")
        print(f"Number of words: {num_words(args.file_path)}")
        print(f"Number of bytes: {num_bytes(args.file_path)}")
        print(f"Number of characters: {num_letters(args.file_path)}") 

    else:
        if args.lines:
            print(f"Number of lines: {num_lines(args.file_path)}")
        if args.words:
            print(f"Number of words: {num_words(args.file_path)}")
        if args.bytes:
            print(f"Number of bytes: {num_bytes(args.file_path)}")
        if args.chars:
            print(f"Number of characters: {num_letters(args.file_path)}")   

    

    