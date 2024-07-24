import heapq
import os
from functools import total_ordering

@total_ordering
class TreeNode:
        def __init__(self, chars, frequency):
                self.chars = chars
                self.frequency = frequency
                self.leftNode = None
                self.rightNode = None
        def __lt__(self, othernode):
                return self.frequency < othernode.frequency
        def __eq__(self, othernode):
                if(othernode == None):
                        return False
                if(not isinstance(othernode, TreeNode)):
                        return False
                return self.frequency == other.frequency


class HuffmanLZWCoding:
	def __init__(self, filepath):
		self.filepath = filepath
		self.heap_arr = []
		self.codes_arr = {}
		self.reverse_mapping_arr = {}

	# functions for compression:

	def huffman_dict(self, text_char):
		frequency_arr = {}
		for characters in text_char:
			if not characters in frequency_arr:
				frequency_arr[characters] = 0
			frequency_arr[characters] += 1
		return frequency_arr

	def addNode(self, frequency_arr):
		for keys in frequency_arr:
			treenode = TreeNode(keys, frequency_arr[keys])
			heapq.heappush(self.heap_arr, treenode)

	def mergeNodes(self):
		while(len(self.heap_arr)>1):
			node1 = heapq.heappop(self.heap_arr)
			node2 = heapq.heappop(self.heap_arr)

			mergednode = TreeNode(None, node1.frequency + node2.frequency)
			mergednode.leftnode = node1
			mergednode.rightnode = node2

			heapq.heappush(self.heap_arr, mergednode)


	def createCode(self, rootnode, currentcode):
		if(rootnode == None):
			return

		if(rootnode.chars != None):
			self.codes_arr[rootnode.chars] = currentcode
			self.reverse_mapping_arr[currentcode] = rootnode.chars
			return

		self.createCode(rootnode.leftnode, currentcode + "0")
		self.createCode(rootnode.rightnode, currentcode + "1")


	def addCodes(self):
		rootnode = heapq.heappop(self.heap_arr)
		currentcode = ""
		self.createCode(rootnode, currentcode)


	def LZW_encoded_text(self, textdata):
		encodedtext = ""
		for characters in textdata:
			encodedtext += self.codes_arr[characters]
		return encodedtext


	def LZWpad_encoded_text(self, encodedtext):
		extrapadding = 8 - len(encodedtext) % 8
		for i in range(extrapadding):
			encodedtext += "0"

		paddedinfo = "{0:08b}".format(extrapadding)
		encodedtext = paddedinfo + encodedtext
		return encodedtext


	def LZW_byte_array(self, paddedencoded_text):
		if(len(paddedencoded_text) % 8 != 0):
			print("Encoding textdata not properly padded")
			exit(0)

		b_arr = bytearray()
		for i in range(0, len(paddedencoded_text), 8):
			byte = paddedencoded_text[i:i+8]
			b_arr.append(int(byte, 2))
		return b_arr


	def compressHuffman(self):
		input_file, file_extension = os.path.splitext(self.filepath)
		outputpath = "compress/compress.bin"

		with open(self.filepath, 'r+') as file, open(outputpath, 'wb') as output:
			textdata = file.read()
			textdata = textdata.rstrip()

			frequency_arr = self.huffman_dict(textdata)
			self.addNode(frequency_arr)
			self.mergeNodes()
			self.addCodes()

			encodedText = self.LZW_encoded_text(textdata)
			paddedencoded_text = self.LZWpad_encoded_text(encodedText)

			b_arr = self.LZW_byte_array(paddedencoded_text)
			output.write(bytes(b_arr))

		print("Compression Completed")
		return outputpath


	""" functions for decompression: """


	def removePadding(self, paddedencoded_text):
		paddedInfo = paddedencoded_text[:8]
		extraPadding = int(paddedInfo, 2)

		paddedencoded_text = paddedencoded_text[8:] 
		encodedText = paddedencoded_text[:-1*extraPadding]

		return encodedText

	def textDecode(self, encodedText):
		currentCode = ""
		decodedText = ""

		for bits in encodedText:
			currentCode += bits
			if(currentCode in self.reverse_mapping_arr):
				characters = self.reverse_mapping_arr[currentCode]
				decodedText += characters
				currentCode = ""

		return decodedText


	def decompressHuffman(self, inputPath):
                inputfile, file_extension = os.path.splitext(self.filepath)
                outputPath = "compress/decompress.txt"
                print(outputPath)
                with open(inputPath, 'rb') as file, open(outputPath, 'w') as output:
                        bitStrings = ""
                        bytes = file.read(1)
                        while(len(bytes) > 0):
                                bytes = ord(bytes)
                                bit = bin(bytes)[2:].rjust(8, '0')
                                bitStrings += bit
                                bytes = file.read(1)

                        encodedText = self.removePadding(bitStrings)
                        decompressedText = self.textDecode(encodedText)
                        output.write(decompressedText)
                print("Decompression Process Completed")
                return outputPath
