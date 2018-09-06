"""This is a photo album analyser, visually and audibly representing the occuring colors and contrasts"""

import os, colorsys, math
from PIL import Image, ImageStat, ImageDraw
from pysynth_b import *

supportedExts = (".bmp", ".dib ", ".dcx", ".eps ", ".pso", ".gif", ".im", ".jpg ", ".jpe ", ".jpeg", ".pcd", ".pcx", ".pdf", ".png", ".pbm ", ".pgm ", ".ppm", ".psd", ".tif ", ".tiff", ".xbm", ".xpm")
#YIQ formatted colours and their tonal equivalents
yiqToNote = (
 	((25, 124, 109), "f"),
    ((35, 135, 112), "f#"),
    ((54, 153, 119), "g"),
	((71, 171, 125), "g#"),
    ((134, 162, 101), "a"),
    ((215, 144, 65), "a#"),
    ((195, 111, 49), "b"),
    ((162, 77, 38), "c"),
    ((176, 28, 70), "c#"),
    ((102, 42, 107), "d"),
    ((31, 60, 140), "d#"),
    ((47, 83, 144), "e"),
    ((44, 100, 134), "f"),
)
prevMedianYiq = (0, 0, 0)
sumDists = 0 #will store the color distance between the images
tones = [] #will store the resulting music tones

#Calculates the distance between two given colors
def distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
	
#Converts a color to the according music note
def toNote(color):
	closestMatch = min(yiqToNote, key = lambda c: distance(c[0], color))
	return closestMatch[1]
	
#Converts a brightness value V ranging from 0 to 255 to an octave
def toOct(V):
	return str(V // 37 +1)
	
#Gets the median color of an image
def getMedianColor(img):
	return tuple(ImageStat.Stat(img).median)
	
while True:
	dir = input("Please enter the path to your album to perform magic on: ")
	#If the input is a directory
	if os.path.isdir(dir):
		dir = dir.replace('/', '\\')
		if not dir.endswith('\\'): dir += '\\'
		#Count the no. of images in the directory
		files = [f for f in os.listdir(dir) if f.endswith(supportedExts)]
		quantity = len(files)
		break
	else:
		print('"' + dir + '" is not a valid directory!')

#1:5 relation of the to-be-made visualisation image
imgHeight = quantity//5

#Initialise a now blank image
img = Image.new('RGB', (quantity, imgHeight))
draw = ImageDraw.Draw(img)

for i in range(quantity):
	#Print progress to the user
	print(str(i+1) + "/" + str(quantity) + " (" + str(100 * (i+1) // quantity) + "%)")
	
	#Extract median color of current image and store it as a 1px wide vertical band in the new image
	median = getMedianColor(Image.open(dir + files[i]))
	draw.line((i, 0, i, imgHeight), median)
	
	#Convert RGB median to YIQ for musical calculations
	medianYiq = colorsys.rgb_to_yiq(*median)
	
	#Store the distance of the current color compared to its predecessor
	sumDists += distance(prevMedianYiq, medianYiq)
	
	brightness = colorsys.rgb_to_hsv(*median)[2]
	#Create a tone out of note and octave
	tone = toNote(medianYiq) + toOct(brightness)
	
	#Check if the current tone is not amongst the previous ones to avoid too much repitition
	if(i == 0 or not any(t[0] == tone for t in tones[-1:])):
		tones.append((tone, 4))
	
	prevMedianYiq = medianYiq
	
#Calculate the music speed based on the magnitude of color contrasts throughout the album
bpm = sumDists // quantity * 50
#Calcuate the sound's fade
leg_stac = bpm / 40

#Name image and music file after the analysed photo album
name = dir.rsplit("\\", 1)[0]
img.save(name + ".png", "PNG")

print("Now it's time to play some sounds!")
make_wav(tones, fn = name + ".wav", leg_stac = leg_stac, bpm = bpm)
