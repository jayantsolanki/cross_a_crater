from PIL import Image, ImageEnhance, ImageFilter
from tesseract import image_to_string

print image_to_string(Image.open('photo_1'))
#print image_to_string(Image.open('test-english.jpg'), lang='eng')