  
import io
from PIL import Image
import numpy
import matplotlib.pyplot as plt
import cv2
from collections import defaultdict
import os

img_pixels = defaultdict(list)
global height
global width

def huffmanCompress(compressed_image):
    # building dictionary here.
    dictionary_size = 256
    dictionary_arr = dict((i, chr(i)) for i in range(dictionary_size))
    results = io.StringIO()
    pixel = chr(compressed_image.pop(0))
    results.write(pixel)
    for m in compressed_image:
        if m in dictionary_arr:
            entry_pixel = dictionary_arr[m]
        elif m == dictionary_size:
            entry_pixel = pixel + pixel[0]
        else:
            raise ValueError('Bad compression m: %s' % m)
        results.write(entry_pixel)
 
        # Adding pixel to the dictionary.
        dictionary_arr[dictionary_size] = pixel + entry_pixel[0]
        dictionary_size += 1
        pixel = entry_pixel
    return results.getvalue()


def huffmanCompressDict(uncompressed_image):
    dictionary_size = 256
    dictionary_arr = dict((chr(i), i) for i in range(dictionary_size))
    pixel = ""
    results = []
    for chars in uncompressed_image:
        pixel_chars = pixel + chars
        if pixel_chars in dictionary_arr:
            pixel = pixel_chars
        else:
            results.append(dictionary_arr[pixel])
            dictionary_arr[pixel_chars] = dictionary_size
            dictionary_size += 1
            pixel = chars

    new_dictionary = list(dictionary_arr.items())
    if pixel:
        results.append(dictionary_arr[pixel])
    return results

def Retinex(image, gamma_value=0.5):
    inv_Gamma = 1.0 / gamma_value
    lookup_colour_improve_table = numpy.array([((i / 255.0) ** inv_Gamma) * 255 for i in numpy.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, lookup_colour_improve_table)

def LZWEncodeImage(codes,image_name,retinex_image):
    pixel_list = []
    for code in codes:
        pixel_list.append(ord(code))
    
    arr = numpy.asarray(pixel_list)
    img = arr.reshape(height,width)
    print(img.shape)

    orig = numpy.zeros((height,width,3))
    for i in range(width):
        for j in range(height):
            value = int(img[j,i])
            values = img_pixels.get(str(i)+","+str(j))
            if values is not None:
                values = values[0]
                r = values[0]
                g = values[1]
                b = values[2]
                orig[j][i][0] = b
                orig[j][i][1] = g
                orig[j][i][2] = r
    cv2.imwrite(image_name, orig,[cv2.IMWRITE_JPEG_QUALITY, 35])
    img = cv2.imread(image_name)            
    img = Retinex(img)            
    cv2.imwrite(retinex_image, img,[cv2.IMWRITE_JPEG_QUALITY, 45])
    

    
def compressImage(uncompress_image):
    compress_image = huffmanCompressDict(uncompress_image)
    arr = numpy.asarray(compress_image)
    arr1 = numpy.zeros(10000)
    for i in range(len(arr1)):
        arr1[i] = arr[i]
    compress_image = huffmanCompress(compress_image)
    LZWEncodeImage(compress_image,'compress/Compress.jpg','compress/retinex_Compress.jpg')


def getImagePixels(image_path):
    global height
    global width
    input_image = Image.open(image_path)
    pixels = input_image.load() 
    widths, heights = input_image.size
    width = widths
    height = heights
    pixels_arr = []
    for i in range(widths):
        for j in range(heights):
            color_pixel = pixels[i, j]
            gray_value = int(round(sum(color_pixel) / float(len(color_pixel))))
            img_pixels[str(i)+","+str(j)].append(color_pixel)
            pixels_arr.append(gray_value)
     
    return pixels_arr

def huffmanImageCompression(input_image):
    img_pixels.clear()
    pixel_values = []
    for p in getImagePixels(input_image):
        pixel_values.append(p)
    pixelString = []
    String_pixel = ""
    for f in pixel_values:
        pixelString.append(chr(f))
    for ps in pixelString:
        String_pixel +=str(ps)
    compressImage(String_pixel)

#huffmanImageCompression('images.jpg')

#original_size = os.stat('images.jpg').st_size
#compress_size = os.stat('Compress.jpg').st_size

#original_image = cv2.imread('images.jpg')
#original_image = cv2.resize(original_image,(500,500))
#compress_image = cv2.imread('Compress.jpg')
#compress_image = cv2.resize(compress_image,(500,500))
#cv2.imshow("Original Image & its Size : "+str(original_size),original_image);
#cv2.imshow("Compress Image & its Size : "+str(compress_size),compress_image);
#cv2.waitKey();


    
