import argparse
import sys

def read_file():
    parser = argparse.ArgumentParser(description="Process user-provided file.")
    parser.add_argument("filename", help="The path of the file you wish to process.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print the frequecy table.")

    args = parser.parse_args()

    try:
        with open(args.filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{args.filename}' does not exist.")
        return None, None
    
    if not content:
        print("No data in file.")
        return None, None
    
    return content, args

class Compressor:
    def __init__(self, data):
        self.data = data

    def character_frequencies(self):
        freq_map = {}

        for char in self.data:
            if char in freq_map:
                freq_map[char] += 1
            else:
                freq_map[char] = 1
        
        return freq_map

def main():
    data, args = read_file()
    if data is None:
        sys.exit(1)

    c = Compressor(data)
    freq_map = c.character_frequencies()

    # optional debug logging:
    if args and args.debug:
        print("\n--- Frequency Table ---")
        for char, count in sorted(freq_map.items(), key=lambda item: item[1], reverse=True):
            print(f"{repr(char)}: {count}")

if __name__ == "__main__":
    main()