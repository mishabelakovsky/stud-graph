import random
from PIL import Image, ImageDraw 

mode = int(input('mode:=')) #read arg as num
fd = input('image:')
image = Image.open(fd)  
draw = ImageDraw.Draw(image) #draw instrument
width = image.size[0] 
height = image.size[1] 	
pix = image.load() 

if (mode == 1): #b/w with user-setting factor 
	factor = int(input('factor:='))
	for i in range(width):
		for j in range(height):
			a = pix[i, j][0]
			b = pix[i, j][1]
			c = pix[i, j][2]
			S = a + b + c
			if (S > (((255 + factor) // 2) * 3)):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((i, j), (a, b, c))

if (mode == 2): #b/w with per-pixel randomized factor 
	for i in range(width):
		for j in range(height):
			factor = randrange(0,255,1)
			a = pix[i, j][0]
			b = pix[i, j][1]
			c = pix[i, j][2]
			S = a + b + c
			if (S > (((255 + factor) // 2) * 3)):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((i, j), (a, b, c))

if (mode == 3): #ordered dithering
	factor = int(input('factor:='))
	order_fn = input('order_matrix:=')
	order_fd = open(order_fn,'r')
	orders = order_fd.read(order_fd)

	for i in range(width):
		for j in range(height):

			factor = randrange(0,255,1)
			a = pix[i, j][0]
			b = pix[i, j][1]
			c = pix[i, j][2]
			S = a + b + c
			if (S > (((255 + orders[i][j]) // 2) * 3)):
				a, b, c = 255, 255, 255
			else:
				a, b, c = 0, 0, 0
			draw.point((i, j), (a, b, c))

if (mode == 4):#string diff
	factor = int(input('factor:='))
	for j in range(height):
		i = 0
		for i in range(width-1):
			oldpix = pix[i,j]
			a = pix[i,j][0]
			b = pix[i,j][1]
			c = pix[i,j][2]
			S = a+b+c
			if (S > (((255 + factor) //2)*3)):
				pix[i,j] = [255,255,255]
			else:
				pix[i,j] = [0,0,0]

			quant_error = sum(oldpix) - sum(pix[i,j])
			pix[x+1][y] = pix[x+1][y] + quant_error * 7/16
				
if (mode == 5):#cross diff
	factor = int(input('factor:='))
	for j in range(height):
		i = 1
		for i in range(width-1):
			oldpix = pix[i,j]
			a = pix[i,j][0]
			b = pix[i,j][1]
			c = pix[i,j][2]
			S = a+b+c
			if (S > (((255 + factor) //2)*3)):
				pix[i,j] = [255,255,255]
			else:
				pix[i,j] = [0,0,0]

			quant_error = sum(oldpix) - sum(pix[i,j])
			if (j % 2):
				pix[x+1][y] = pix[x+1][y] + quant_error * 7/16
			else:
				pix[width-x-1][y] = pix[width-x-1][y] + quant_error * 7/16

if (mode == 6):#floyd-steinberg 
	factor = int(input('factor:='))
	for j in range(height):
		i=1
		for i in range(width-1):
			oldpix = pix[i,j]
			a = pix[i,j][0]
			b = pix[i,j][1]
			c = pix[i,j][2]
			S = a+b+c
			if (S > (((255 + factor) //2)*3)):
				pix[i,j] = [255,255,255]
			else:
				pix[i,j] = [0,0,0]

			quant_error = sum(oldpix) - sum(pix[i,j])
			if (j == height - 1):
				if (j % 2):
					pix[x+1][y] = pix[x+1][y] + quant_error * 7/16
				else:
					pix[x-1][y] = pix[x-1][y] + quant_error * 5 /16
			elif (j % 2):
					pix[x+1][y] = pix[x+1][y] + quant_error * 7/16
					pix[x-1][y+1] = pix[x-1][y+1] + quant_error * 3/16
					pix[x][y+1] = pix[x][y+1] + quant_error * 5/16
					pix[x+1][y+1] = pix [x+1][y+1] + quant_error /16
			else:
					pix[x-1][y] = pix[x-1][y] + quant_error * 5 /16
					pix[x-1][y+1] = pix [x-1][y+1] + quant_error * 3/16
					pix[x][y+1] = pix[x][y+1] + quant_error * 7/16
					pix[x+1][y+1] = pix[x][y+1] + quant_error * 1/16

image.save("out.jpg", "JPEG")
del draw