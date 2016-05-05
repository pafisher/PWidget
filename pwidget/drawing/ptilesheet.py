import pygame
import pygame.locals

"""
Contains a 2D list of tiles of size (tilewidth, tileheight) from the given filename
Uses the standard pink colorkey
get_tile(x, y) => tile at position (x, y) in filename
"""
class PTileSheet:
	def __init__(self, filename, tilewidth, tileheight = None, colorkey = (255, 0, 255)):
		if tileheight == None:
			tileheight = tilewidth
		self.sheet = []
		image = pygame.image.load(filename).convert()
		image.set_colorkey(colorkey)
		image_width, image_height = image.get_size()
		for y in range(image_height / tileheight):
			line = []
			self.sheet.append(line)
			for x in range(image_width / tilewidth):
				rect = (x * tilewidth, y * tileheight, tilewidth, tileheight)
				line.append(image.subsurface(rect))
	def get_sheet(self):
		return self.sheet
	def get_tile(self, x, y):
		return self.sheet[y][x]