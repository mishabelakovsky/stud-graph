import random
from PIL import Image, ImageDraw 
import itertools
''' How to use:

Choose dithering algo
Enter the filename
Then chose threshold walue or matrix of dithering (in algo 3)
Press enter and observe results in output file 'out.jpg'

Set of algorithms:
1. Fixed threshold
2. Random threshold
3. Dithering matrix
4. Error diffusion by string
5. Error diffusion by cross-string
6. Error diffusion by matrix & cross

example of input:
2
'lena.jpg'
128

'''

threshold_matrix=[[[0.2,0.6],[0.8,0.4]],[[0.1,0.8,0.4],[0.7,0.6,0.3],[0.5,0.2,0.9]]]

mode = int(input('mode:=')) #read arg as num
fd = input('image:')
image = Image.open(fd)  
draw = ImageDraw.Draw(image) #draw instrument
pix = list(image.getdata())
width, height = image.size
pix = [pix[i * width:(i + 1) * width] for i in xrange(height)]

for i in range(height):
	for j in range(width):
		pix[i][j] = list(pix[i][j])

if (mode == 1): #b/w with user-setting factor 
	factor = int(input('factor:='))
	for i in range(width):
		for j in range(height):
			S = sum(pix[i][j])
			if (S > (factor) * 3):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((j, i), (a, b, c))
import random
if (mode == 2): #b/w with per-pixel randomized factor 
	for i in range(width):
		for j in range(height):

			factor = random.randrange(0,255,1)
			S = sum(pix[i][j])
			if (S > ((factor) * 3)):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((j, i), (a, b, c))

if (mode == 3): #ordered dithering on matrix
	num = int(input('Number of dithering matrix (1,2):='))
	for i in range(height):
		for j in range(width):
			S = sum(pix[i][j])
			if ( ((255*3) // 2) < (S+S*threshold_matrix[num-1][i % len(threshold_matrix[num-1][0])][j % len(threshold_matrix[num-1])])):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((j, i), (a, b, c))
			
if (mode == 4):#string diff
	factor = int(input('factor:='))
	for j in range(height):
		i = 0
		for i in range(width-1):
			oldpix = pix[i][j]
			S = sum(pix[i][j])
			if (S > ( factor)*3):
				pix[i][j][0] = pix[i][j][1] = pix[i][j][2] = 255#; [255,255,255]
			else:
				pix[i][j][0] = pix[i][j][1] = pix[i][j][2] = 0#;

			quant_error = sum(oldpix) - sum(pix[i][j])
			for k in range(3):
				pix[i+1][j][k] = pix[i+1][j][k] + quant_error * 7/16
			draw.point((j, i), (pix[i][j][0], pix[i][j][1], pix[i][j][2]))

if (mode == 5):#cross diff
	factor = int(input('factor:='))
	for i in range(height):
		if not (i % 2):
			j = 1
			for j in range(width-1):
				oldpix = pix[i][j]
				S = sum(pix[i][j])
				if (S >  (factor)*3):
					pix[i][j] = [255,255,255]
				else:
					pix[i][j] = [0,0,0]

				quant_error = (sum(oldpix) - sum(pix[i][j]))//3
				for k in range(3):	
					pix[i-1][j][k] = pix[i-1][j][k] + quant_error * 7/16
				draw.point((j, i), (pix[i][j][0], pix[i][j][1], pix[i][j][2]))
		else:
			j = height - 1
			while j > 0:
				oldpix = pix[i][j]
				S = sum(pix[i][j])
				if (S > (factor)*3):
					pix[i][j] = [255,255,255]
				else:
					pix[i][j] = [0,0,0]

				quant_error = sum(oldpix) - sum(pix[i][j])
				for k in range(3):	
					pix[i-1][j][k] = pix[i-1][j][k] + quant_error * 7/16
				draw.point((j, i), (pix[i][j][0], pix[i][j][1], pix[i][j][2]))
				j-=1

if (mode == 6):#floyd-steinberg
	factor = int(input('factor:='))
	for i in range(height-1):
		if not (i % 2):
			j = 1
			for j in range(width-1):
				oldpix = pix[i][j]
				S = sum(pix[i][j])
				if (S > (factor*3)):
					pix[i][j] = [255,255,255]
				else:
					pix[i][j] = [0,0,0]

				quant_error = (sum(oldpix) - sum(pix[i][j]))//3
				if (i == height - 1):
					for k in range(3):	
						pix[i][j+1][k] = pix[i][j+1][k] + quant_error * 7/16
				else:
					for k in range(3):
						pix[i][j+1][k] = pix[i][j+1][k] + quant_error * 7/16
						pix[i+1][j-1][k] = pix[i+1][j-1][k] + quant_error * 3/16
						pix[i+1][j][k] = pix[i+1][j][k] + quant_error * 5/16
						pix[i+1][j+1][k] = pix [i+1][j+1][k] + quant_error /16	
					
				draw.point((j, i), (pix[i][j][0], pix[i][j][1], pix[i][j][2]))
		else:
			j = width - 2
			while j > 0:
				oldpix = pix[i][j]
				S = sum(pix[i][j])
				if (S > (factor)*3): 
					pix[i][j] = [255,255,255]
				else:
					pix[i][j] = [0,0,0]

				quant_error = (sum(oldpix) - sum(pix[i][j]))//3
				if (i == height - 1):
					for k in range(3):	
						pix[i][j-1][k] = pix[i][j-1][k] + quant_error * 7/16
				else:
					for k in range(3):
						pix[i][j-1][k] = pix[i][j-1][k] + quant_error * 5 /16
						pix[i+1][j-1][k] = pix[i+1][j-1][k] + quant_error * 3/16
						pix[i+1][j][k] = pix[i+1][j][k] + quant_error * 7/16
						pix[i+1][j+1][k] = pix[i+1][j][k] + quant_error * 1/16	
				draw.point((j, i), (pix[i][j][0], pix[i][j][1], pix[i][j][2]))
				j-=1

image.save("out.jpg", "JPEG")
del draw
