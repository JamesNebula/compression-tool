# Features
- Compresses text files into binary format
- Decompresses back to original text
- Custom binary header format for storing frequency tables
- CLI flags for compression, decompression and debug output
- Got -43% compression on a 3.5MB text file

# Overview
- Character frequency analysis
- Huffman tree construction using a min-heap
- Variable length prefix code generation
- Bit-level packing with padding management
- Binary serialisation with a custom header format

# Usage
- **python comp.py input.txt -o compressed.bin**
- **python comp.py compressed.bin -d -o output.txt**
- **python comp.py input.txt -o compressed.bin -ft**
