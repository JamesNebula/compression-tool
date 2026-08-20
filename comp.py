import argparse
import sys
import heapq

def read_file():
    parser = argparse.ArgumentParser(description="Process user-provided file.")
    parser.add_argument("filename", help="The path of the file you wish to process.")
    parser.add_argument("-d", "--debug", action="store_true", help="Print the frequecy table.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file.")

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

def read_compressed_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"The file '{filepath}' does not exist")
        return None

    if not content:
        print("No data in file.")
        return None

    return content        

class Node:
    def __init__(self, freq, char):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

class Compressor:
    def __init__(self, data):
        self.data = data
        self.mappings = {}
        self.padding = 0

    def character_frequencies(self):
        freq_map = {}

        for char in self.data:
            if char in freq_map:
                freq_map[char] += 1
            else:
                freq_map[char] = 1
        
        return freq_map
    
    def build_tree(self):
        heap = []
        freq_map = self.character_frequencies()
        for char, freq in freq_map.items():
            n = Node(freq, char)
            heapq.heappush(heap, n)
        
        while len(heap) > 1:
            lf1 = heapq.heappop(heap)
            lf2 = heapq.heappop(heap)

            pf = lf1.freq + lf2.freq
            pn = Node(pf, char=None)
            pn.left = lf1
            pn.right = lf2

            heapq.heappush(heap, pn)
        # print(heap[0].freq) == 8
        return heap[0]
    
    # ============
    # Compress
    # ============
    def prefix_code(self, curr_node, code_str=''):

        if not curr_node.left and not curr_node.right:
            self.mappings[curr_node.char] = code_str

        if curr_node.left:
            self.prefix_code(curr_node.left, code_str + '0')

        if curr_node.right:
            self.prefix_code(curr_node.right, code_str + '1')
            
        # print(self.mappings)
        return self.mappings
    
    def write_compressed_data(self, freq_map, comp_bytes, output_file):

        try:
            with open(output_file, 'wb') as f:
                entries = len(freq_map)
                encoded_entries = str(entries).encode()
                f.write(encoded_entries)
                for char, freq in freq_map.items():
                    header_str = f"\n{char} {freq}"
                    encoded_str = header_str.encode()
                    f.write(encoded_str)

                padding_count = bytes([self.padding])
                f.write(padding_count)
                f.write(comp_bytes)

        except Exception as e:
            print(f"Error writing to file: {e}")

        return 

    def encode_text(self):
        result = []
        
        for char in self.data:
            result.append(self.mappings[char]) 
        
        result_str = "".join(result)

        if len(result_str) % 8 != 0:
            leftover = (8 - (len(result_str)) % 8)
            self.padding = leftover
            result_str += self.padding  * '0'
        
        byte_collection = []
        for b in range(0, len(result_str), 8):
            byte = int(result_str[b:b+8], 2)
            byte_collection.append(byte)
        
        return bytes(byte_collection)
    
    # ============
    # Decompress
    # ============

    # b"4\nt 4\ne 2\ns 1\nx 1"  ← header looks like this for "testtext"
    def parse_header(self, data):
        # get entry count
        nl_idx = data.find(b'\n')
        entry = data[0:nl_idx]
        string_data = entry.decode()

        entry_count = int(string_data)

        # get each entry 
        frequency = {}
        current_pos = nl_idx

        for i in range(entry_count):

            if i == entry_count - 1:
                last_entry_space = data.find(b' ', current_pos+1)
                last_entry_char = data[current_pos+1:last_entry_space]

                freq_start_pos = last_entry_space + 1

                position = freq_start_pos

                while position < len(data) and chr(data[position]).isdigit():
                    position += 1
        
                header_end = position
                    
                last_entry_freq = data[freq_start_pos:header_end]
                char_str = last_entry_char.decode()
                freq_str = last_entry_freq.decode()
                freq_int = int(freq_str)
                frequency[char_str] = freq_int

                return (frequency, header_end)

            else:
                next_nl_idx = data.find(b'\n', current_pos+1)
                next_entry = data[current_pos+1:next_nl_idx]
                entry_str = next_entry.decode()

                entry_spl = entry_str.split()

                char = entry_spl[0]
                freq = int(entry_spl[1])

                frequency[char] = freq

                current_pos = next_nl_idx

def main():
    data, args = read_file()
    if data is None:
        sys.exit(1)

    c = Compressor(data)
    freq_map = c.character_frequencies()
    tree = c.build_tree()
    c.prefix_code(tree)
    comp_bytes = c.encode_text()
    c.write_compressed_data(freq_map, comp_bytes, args.output)  # type: ignore

    # optional debug logging:
    if args and args.debug:
        print("\n--- Frequency Table ---")
        for char, count in sorted(freq_map.items(), key=lambda item: item[1], reverse=True):
            print(f"{repr(char)}: {count}") 

if __name__ == "__main__":
    main()