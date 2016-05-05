import pygame
import pygame.locals

"""
Draws text on the given surface at the given x and y coordinates up to maxwidth pixels
"""
def pdrawstring(surface, font, x, y, text, maxwidth = 10000):
	for i, char in enumerate(str(text)):
		if x + (i * font.get_fontsize()) + (i * min(max(1, font.get_fontsize() / 10), 10)) + font.get_fontsize() < maxwidth:
			surface.blit(font.get_char(char), (x + (i * font.get_fontsize()) + (i * min(max(1, font.get_fontsize() / 10), 10)), y))
		else:
			break