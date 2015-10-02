import random
from PIL import Image, ImageDraw 
import itertools

mode = int(input('mode:=')) #read arg as num
#fd = input('image:')
image = Image.open("lena.jpg")  
draw = ImageDraw.Draw(image) #draw instrument
pix = list(image.getdata())
width, height = image.size
pix = [pix[i * width:(i + 1) * width] for i in xrange(height)]

print pix[1][1]
#pix = [pix[i*width:(i+1) * width] for i in xrange(height)]
#pix = list(itertools.chain(*pix))
for i in range(height):
	for j in range(width):
		pix[i][j] = list(pix[i][j])

if (mode == 1): #b/w with user-setting factor 
	factor = int(input('factor:='))
	for i in range(width):
		for j in range(height):
			a = pix[i][j][0]
			b = pix[i][j][1]
			c = pix[i][j][2]
			S = a + b + c
			if (S > (((255 + factor) // 2) * 3)):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((j, i), (a, b, c))
import random
if (mode == 2): #b/w with per-pixel randomized factor 
	for i in range(width):
		for j in range(height):

			factor = random.randrange(0,255,1)
			a = pix[i][j][0]
			b = pix[i][j][1]
			c = pix[i][j][2]
			S = a + b + c
			if (S > (((255 + factor) // 2) * 3)):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((j, i), (a, b, c))

if (mode == 3): #ordered dithering
	factor = int(input('factor:='))
	order_fn = input('order_matrix:=')
	order_fd = open(order_fn,'r')
	orders = order_fd.read(order_fd)

	for i in range(width):
		for j in range(height):

			factor = random.randrange(0,255,1)
			a = pix[i][j][0]
			b = pix[i][j][1]
			c = pix[i][j][2]
			S = a + b + c
			if (S > (((255 + orders[i][j]) // 2) * 3)):
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
			a = pix[i][j][0]
			b = pix[i][j][1]
			c = pix[i][j][2]
			S = a+b+c
			print pix[i][j]
			if (S > (((255 + factor) //2)*3)):
				pix[i][j][0] = pix[i][j][1] = pix[i][j][2] = 255#; [255,255,255]
			else:
				pix[i][j][0] = pix[i][j][1] = pix[i][j][2] = 0#;

			quant_error = sum(oldpix) - sum(pix[i][j])
			pix[i+1][j] = pix[i+1][j] + quant_error * 7/16
			draw.point((j, i), (pix[i][j][0], pix[i][j][1], pix[i][j][2]))

if (mode == 5):#cross diff
	factor = int(input('factor:='))
	for j in range(height):
		i = 1
		for i in range(width-1):
			oldpix = pix[i][j]
			a = pix[i][j][0]
			b = pix[i][j][1]
			c = pix[i][j][2]
			S = a+b+c
			if (S > (((255 + factor) //2)*3)):
				pix[i][j] = [255,255,255]
			else:
				pix[i][j] = [0,0,0]

			quant_error = sum(oldpix) - sum(pix[i][j])
			if (j % 2):
				pix[x+1][y] = pix[x+1][y] + quant_error * 7/16
			else:
				pix[width-i-1][j] = pix[width-i-1][j] + quant_error * 7/16
			draw.point((j, i), (pix[i,j][0], pix[i,j][1], pix[i,j][2]))

if (mode == 6):#floyd-steinberg 
	factor = int(input('factor:='))
	for j in range(height):
		i=1
		for i in range(width-1):
			oldpix = pix[i][j]
			a = pix[i][j][0]
			b = pix[i][j][1]
			c = pix[i][j][2]
			S = a+b+c
			if (S > (((255 + factor) //2)*3)):
				pix[i][j] = [255,255,255]
			else:
				pix[i][j] = [0,0,0]

			quant_error = sum(oldpix) - sum(pix[i][j])
			if (j == height - 1):
				if (j % 2):
					pix[i+1][j] = pix[i+1][j] + quant_error * 7/16
				else:
					pix[i-1][j] = pix[i-1][j] + quant_error * 5 /16
			elif (j % 2):
					pix[i+1][j] = pix[i+1][j] + quant_error * 7/16
					pix[i-1][j+1] = pix[i-1][j+1] + quant_error * 3/16
					pix[i][j+1] = pix[i][j+1] + quant_error * 5/16
					pix[i+1][j+1] = pix [i+1][j+1] + quant_error /16
			else:
					pix[i-1][j] = pix[i-1][j] + quant_error * 5 /16
					pix[i-1][j+1] = pix [i-1][j+1] + quant_error * 3/16
					pix[i][j+1] = pix[i][j+1] + quant_error * 7/16
					pix[i+1][j+1] = pix[i][j+1] + quant_error * 1/16

			draw.point((j, i), (pix[i][j][0], pix[i][j][1], pix[i][j][2]))
image.save("out.jpg", "JPEG")
del draw