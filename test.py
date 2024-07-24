from HuffmanDataLZW import HuffmanLZWCoding
import os
#input file path
path = "myfile.txt"

h = HuffmanLZWCoding(path)

output_path = h.compressHuffman()
h.decompressHuffman(output_path)

original = os.stat(path).st_size
compress = os.stat(output_path).st_size

print(str(original)+" "+str(compress))
