import pygame
import pygame.locals
import sys

from drawing import pdrawstring
from drawing import ptilesheet

VERTICAL_ORIENTATION = 0
HORIZONTAL_ORIENTATION = 1

"""
Base class for widgets
"""
class PComponent:
	def __init__(self, x, y, width, height, debug_name = "Anonymous"):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.debug_name = debug_name
		self.components = []
		self.parent = None

	def paint(self, surface, window):
		pass

	def mouse_down(self, x, y, window):
		pass

	def mouse_up(self, x, y, window):
		pass

	def key_down(self, key, window):
		pass

	def key_up(self, key, window):
		pass

	def adjust_children(self):
		pass

	def adjust_parent(self):
		pass

	def contains_point(self, x, y):
		return (x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height)

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y
	
	def set_width(self, width):
		self.width = width
	
	def set_height(self, height):
		self.height = height
	
	def get_x(self):
		return self.x
	
	def get_y(self):
		return self.y
	
	def get_width(self):
		return self.width
	
	def get_height(self):
		return self.height

"""
PComponent to hold other PComponents
Automatically adjusts x, y, width and height values of all contained PComponents when a new one is added
Doesn't paint itself, but calls paint() for each of its sub-PComponents
Sends mouse events to appropriate sub-PComponent
"""
class PPanel(PComponent):
	def __init__(self, orientation, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 0, debug_name)
		self.orientation = orientation

	def paint(self, surface, window):
		for comp in self.components:
			comp.paint(surface, window)

	def mouse_down(self, x, y, window):
		window.set_focus(self)
		for comp in self.components:
			if comp.contains_point(x, y):
				comp.mouse_down(x, y, window)
				break

	def mouse_up(self, x, y, window):
		for comp in self.components:
			if comp.contains_point(x, y):
				comp.mouse_up(x, y, window)
				break

	def adjust_children(self):
		if len(self.components) != 0:
			if self.orientation == VERTICAL_ORIENTATION:
				currentY = self.get_y()
				for comp in self.components:
					comp.set_y(currentY)
					currentY += comp.get_height()
					comp.set_x(self.get_x())

			elif self.orientation == HORIZONTAL_ORIENTATION:
				currentX = self.get_x()
				for comp in self.components:
					comp.set_x(currentX)
					currentX += comp.get_width()
					comp.set_y(self.get_y())

			for comp in self.components:
				comp.adjust_children()
	
	def adjust_parent(self):
		if self.parent != None:
			if self.parent.orientation == VERTICAL_ORIENTATION:
				newHeight = 0
				newWidth = 0
				for comp in self.parent.components:
					newHeight += comp.get_height()
					newWidth = max(newWidth, comp.get_width())
				self.parent.set_height(newHeight)
				self.parent.set_width(newWidth)

			elif self.parent.orientation == HORIZONTAL_ORIENTATION:
				newHeight = 0
				newWidth = 0
				for comp in self.parent.components:
					newWidth += comp.get_width()
					newHeight = max(newHeight, comp.get_height())
				self.parent.set_height(newHeight)
				self.parent.set_width(newWidth)
			self.parent.adjust_parent()

		else:
			self.adjust_children()

	def add_component(self, component):
		if component == self:
			sys.exit("Can't add panel to itself")
		if self.orientation == VERTICAL_ORIENTATION:
			if len(self.components) == 0:
				component.set_x(self.get_x())
				component.set_y(self.get_y())
				self.set_height(self.get_height() + component.get_height())
				self.set_width(component.get_width())

			else:
				component.set_x(self.components[-1].get_x())
				component.set_y(self.components[-1].get_y() + self.components[-1].get_height())
				self.set_height(self.get_height() + component.get_height())
				self.set_width(max(self.get_width(), component.get_width()))

		elif self.orientation == HORIZONTAL_ORIENTATION:
			if len(self.components) == 0:
				component.set_x(self.get_x())
				component.set_y(self.get_y())
				self.set_width(self.get_width() + component.get_width())
				self.set_height(component.get_height())

			else:
				component.set_x(self.components[-1].get_x() + self.components[-1].get_width())
				component.set_y(self.components[-1].get_y())
				self.set_width(self.get_width() + component.get_width())
				self.set_height(max(self.get_height(), component.get_height()))

		component.parent = self
		self.components.append(component)
		self.adjust_parent()


"""
PComponent to display text value using given font
"""
class PLabel(PComponent):
	def __init__(self, gc, value, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 0, debug_name)
		self.gc = gc
		self.value = str(value)
		self.set_width((len(value) * (gc.font.get_fontsize() + gc.font.get_fontspacing())) - gc.font.get_fontspacing())
		self.set_height(gc.font.get_fontsize())

	def paint(self, surface, window):
		pdrawstring.pdrawstring(surface, self.gc.font, self.x, self.y, self.value)

	def set_value(self, value):
		self.value = str(value)

	def get_value(self):
		return self.value

"""
PComponent that acts like a PLabel, but wraps lines that extend past max_width pixels and takes newline characters into consideration, left-aligning all lines
Does not support value set or get
Will wrap in the middle of a word - use caution when determining line length and max_width
"""
class PParagraph(PComponent):
	def __init__(self, gc, value, max_width, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 0, debug_name)
		self.gc = gc
		self.value = str(value)
		self.surface = self.paint_surface(max_width)

	def paint_surface(self, max_width):
		maxchars = max_width / (self.gc.font.get_fontsize() + self.gc.font.get_fontspacing())
		line = ""
		linelist = []
		width = 0
		for char in self.value:
			if char == "\n":
				linelist.append(line)
				width = max(width, len(line))
				line = ""
			elif len(line) >= maxchars:
				linelist.append(line)
				width = max(width, len(line))
				line = char
			else:
				line += char
		linelist.append(line)
		self.set_width(width * (self.gc.font.get_fontsize() + self.gc.font.get_fontspacing()) - self.gc.font.get_fontspacing())
		self.set_height(len(linelist) * (self.gc.font.get_fontsize() + self.gc.font.get_fontspacing()) - self.gc.font.get_fontspacing())
		ret_surface = pygame.Surface((self.get_width(), self.get_height()))
		ret_surface.fill((255, 0, 255))
		ret_surface.set_colorkey((255, 0, 255))
		for i, line in enumerate(linelist):
			pdrawstring.pdrawstring(ret_surface, self.gc.font, 0, i * (self.gc.font.get_fontspacing() + self.gc.font.get_fontsize()), line)
		return ret_surface

	def paint(self, surface, window):
		surface.blit(self.surface, (self.get_x(), self.get_y()))


"""
PComponent to separate other PComponents vertically within a PPanel
Does not paint
"""
class PVerticalStrut(PComponent):
	def __init__(self, height, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, height, debug_name)


"""
PComponent to separate other PComponents horizontally within a PPanel
Does not paint
"""
class PHorizontalStrut(PComponent):
	def __init__(self, width, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, width, 0, debug_name)


"""
PComponent that paints a rectangle and the string value and executes 0 or more functions upon receiving a mouse down event
Supports value set and get
"""
class PButton(PComponent):
	def __init__(self, gc, value, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 0, debug_name)
		self.set_width((len(value) * (gc.font.get_fontsize() + gc.font.get_fontspacing())) + gc.font.get_fontspacing() + 4)
		self.set_height(gc.font.get_fontsize() + 4 + (2 * gc.font.get_fontspacing()))
		self.gc = gc
		self.value = value
		self.actions = []

	def paint(self, surface, window):
		pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))
		pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()), 2)
		pdrawstring.pdrawstring(surface, self.gc.font, self.get_x() + self.gc.font.get_fontspacing() + 2, self.get_y() + self.gc.font.get_fontspacing() + 2, self.value)

	def mouse_down(self, x, y, window):
		window.set_focus(self)

	def mouse_up(self, x, y, window):
		if window.get_focus() == self:
			for action in self.actions:
				action(self)
			window.reset_focus()

	def set_value(self, value):
		self.value = str(value)

	def get_value(self):
		return self.value

	def add_action(self, action):
		self.actions.append(action)


"""
PComponent that toggles its value between True and False and executes 0 or more functions upon receiving a mouse down event
"""
class PCheckBox(PComponent):
	def __init__(self, gc, label = "", debug_name = "Anonymous"):
		if label == "":
			PComponent.__init__(self, 0, 0, 20, 20, debug_name)
		else:
			PComponent.__init__(self, 0, 0, 0, gc.font.get_fontsize(), debug_name)
			self.set_width(gc.font.get_fontsize() + (len(label) * (gc.font.get_fontsize() + gc.font.get_fontspacing())))
		self.value = False
		self.actions = []
		self.label = str(label)
		self.gc = gc

	def paint(self, surface, window):
		if self.label == "":
			pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))

		else:
			pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.gc.font.get_fontsize(), self.get_height()))
			pdrawstring.pdrawstring(surface, self.gc.font, self.get_x() + self.gc.font.get_fontsize() + self.gc.font.get_fontspacing(), self.get_y(), self.label)
		
		if self.value:
			pygame.draw.rect(surface, self.gc.foreground_colour, pygame.Rect(self.get_x() + 2, self.get_y() + 2, self.gc.font.get_fontsize() - 4, self.get_height() - 4))

	def mouse_down(self, x, y, window):
		window.set_focus(self)

	def mouse_up(self, x, y, window):
		if window.get_focus() == self:
			self.value = not self.value
			for action in self.actions:
				action(self)
			window.reset_focus()

	def add_action(self, action):
		self.actions.append(action)

	def toggle(self, value = None):
		if value == None:
			self.value = not self.value
		else:
			self.value = value


"""
PComponent that contains a list of selectable strings as options, displaying at most rows options at a time
Supports scrolling through the use of scroll_up() and scroll_down() methods
Does not support the execution of any functions upon receiving a mouse down, but updates itself based on the location of the event
Supports access through the get_value() method and allows for additional options to be added with the add_option() method
"""
class PSelector(PComponent):
	def __init__(self, gc, width, rows, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, width, (rows * gc.font.get_fontsize()) + 4, debug_name)
		self.gc = gc
		self.options = []
		self.selection = 0
		self.offset = 0
		self.rows = rows
		for i in range(rows):
			self.options.append("")

	def paint(self, surface, window):
		pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))
		pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x() + 2, self.get_y() + 2 + (self.selection * self.gc.font.get_fontsize()), self.get_width() - 4, self.gc.font.get_fontsize()))
		for i, option in enumerate(self.options[self.offset : self.offset + self.rows]):
			pdrawstring.pdrawstring(surface, self.gc.font, self.get_x() + 2, self.get_y() + 2 + (self.gc.font.get_fontsize() * i), option, self.get_width() - 4)

	def mouse_down(self, x, y, window):
		window.set_focus(self)

	def mouse_up(self, x, y, window):
		if window.get_focus() == self:
			self.selection = min(max(((y - self.get_y()) - 2) / self.gc.font.get_fontsize(), 0), self.rows - 1)
			window.reset_focus()

	def add_option(self, value):
		self.options.insert(0, str(value))

	def scroll_up(self):
		self.offset = max(0, self.offset - 1)

	def scroll_down(self):
		self.offset = min(len(self.options) - self.rows, self.offset + 1)

	def scroll_to(self, option_number):
		self.offset = min(max(option_number, 0), len(self.options) - self.rows)

	def get_value(self):
		return self.options[self.offset + self.selection]


"""
PComponent that creates two buttons spanning the height of the panel they are in. Clicking on the top button decreases the value by 1, clicking on the bottom button
increases it by 1. Supports executing 0 or more functions upon receiving a mouse down event.
"""
class PVerticalScrollWheel(PComponent):
	def __init__(self, gc, maximum, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 20, 0, debug_name)
		self.value = 0
		self.gc = gc
		self.maximum = maximum
		self.actions = []

	def paint(self, surface, window):
		pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))
		pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x() + 2, self.get_y() + 2, self.get_width() - 4, (self.get_height() / 2) - 4))
		pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x() + 2, self.get_y() + (self.get_height() / 2) + 2, self.get_width() - 4, (self.get_height() / 2) - 4))
		pygame.draw.rect(surface, self.gc.foreground_colour, pygame.Rect(self.get_x() + 6, self.get_y() + 6, self.get_width() - 12, 12))
		pygame.draw.rect(surface, self.gc.foreground_colour, pygame.Rect(self.get_x() + 6, self.get_y() + self.get_height() - 18, self.get_width() - 12, 12))

	def mouse_down(self, x, y, window):
		window.set_focus(self)

	def mouse_up(self, x, y, window):
		if window.get_focus() == self:
			if (y - self.get_y() < (self.get_height() / 2)):
				self.value = max(0, self.value - 1)
			else:
				self.value = min(self.maximum, self.value + 1)
			for action in self.actions:
				action(self)
			window.reset_focus()

	def adjust_children(self):
		self.set_height(self.parent.get_height())

	def add_action(self, action):
		self.actions.append(action)

	def get_value(self):
		return self.value

	def get_maximum(self):
		return self.maximum


"""
PComponent that creates two buttons spanning the width of the panel they are in. Clicking on the left button decreases the value by 1, clicking on the right button
increases it by 1. Supports executing 0 or more functions upon receiving a mouse down event.
"""
class PHorizontalScrollWheel(PComponent):
	def __init__(self, gc, maximum, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 20, debug_name)
		self.gc = gc
		self.value = 0
		self.maximum = maximum
		self.actions = []

	def paint(self, surface, window):
		pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))
		pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x() + 2, self.get_y() + 2, (self.get_width() / 2) - 4, self.get_height() - 4))
		pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x() + 2 + (self.get_width() / 2), self.get_y() + 2, (self.get_width() / 2) - 4, self.get_height() - 4))
		pygame.draw.rect(surface, self.gc.foreground_colour, pygame.Rect(self.get_x() + 6, self.get_y() + 6, 12, self.get_height() - 12))
		pygame.draw.rect(surface, self.gc.foreground_colour, pygame.Rect(self.get_width() - 18, self.get_y() + 2, 12, self.get_height() - 12))

	def mouse_down(self, x, y, window):
		window.set_focus(self)

	def mouse_up(self, x, y, window):
		if window.get_focus() == self:
			if (x - self.get_x() < (self.get_width() / 2)):
				self.value = max(0, self.value - 1)
			else:
				self.value = min(self.maximum, self.value + 1)
			for action in self.actions:
				action(self)
			window.reset_focus()

	def adjust_children(self):
		self.set_width(self.parent.get_width())

	def add_action(self, action):
		self.actions.append(action)

	def get_maximum(self):
		return self.maximum


"""
PComponent that consumes keypresses and builds a string. Supports access at any point in the string through clicks. Requires focus to allow for text entry
"""
class PTextBox(PComponent):
	def __init__(self, gc, max_width, maxlength = 10000, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 0, debug_name)
		self.gc = gc
		self.value = ""
		self.maxlength = maxlength
		self.offset = 0
		self.cursor = 0
		width = max_width - (max_width % (gc.font.get_fontsize() + gc.font.get_fontspacing()))
		self.maxchars = (width - 4) / (gc.font.get_fontsize() + gc.font.get_fontspacing())
		self.set_width(width + 2)
		self.set_height(gc.font.get_fontsize() + 4 + (2 * gc.font.get_fontspacing()))

	def paint(self, surface, window):
		pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))
		pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()), 2)
		if window.get_focus() == self:
			pygame.draw.rect(surface, self.gc.cursor_colour, pygame.Rect(self.get_x() + ((self.cursor - self.offset) * (self.gc.font.get_fontsize() + self.gc.font.get_fontspacing())) + 2, self.get_y() + 2, self.gc.font.get_fontsize(), self.get_height() - 4))
		pdrawstring.pdrawstring(surface, self.gc.font, self.get_x() + self.gc.font.get_fontspacing() + 2, self.get_y() + self.gc.font.get_fontspacing() + 2, self.value[self.offset:])

	def mouse_down(self, x, y, window):
		window.set_focus(self)
		self.cursor = min(((x - self.get_x() - 2) / (self.gc.font.get_fontsize() + self.gc.font.get_fontspacing())) + self.offset, len(self.value))

	def key_down(self, key, window):
		if window.focus == self:
			if key == pygame.K_a and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "a" + self.value[self.cursor:]
			elif key == pygame.K_b and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "b" + self.value[self.cursor:]
			elif key == pygame.K_c and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "c" + self.value[self.cursor:]
			elif key == pygame.K_d and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "d" + self.value[self.cursor:]
			elif key == pygame.K_e and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "e" + self.value[self.cursor:]
			elif key == pygame.K_f and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "f" + self.value[self.cursor:]
			elif key == pygame.K_g and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "g" + self.value[self.cursor:]
			elif key == pygame.K_h and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "h" + self.value[self.cursor:]
			elif key == pygame.K_i and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "i" + self.value[self.cursor:]
			elif key == pygame.K_j and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "j" + self.value[self.cursor:]
			elif key == pygame.K_k and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "k" + self.value[self.cursor:]
			elif key == pygame.K_l and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "l" + self.value[self.cursor:]
			elif key == pygame.K_m and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "m" + self.value[self.cursor:]
			elif key == pygame.K_n and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "n" + self.value[self.cursor:]
			elif key == pygame.K_o and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "o" + self.value[self.cursor:]
			elif key == pygame.K_p and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "p" + self.value[self.cursor:]
			elif key == pygame.K_q and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "q" + self.value[self.cursor:]
			elif key == pygame.K_r and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "r" + self.value[self.cursor:]
			elif key == pygame.K_s and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "s" + self.value[self.cursor:]
			elif key == pygame.K_t and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "t" + self.value[self.cursor:]
			elif key == pygame.K_u and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "u" + self.value[self.cursor:]
			elif key == pygame.K_v and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "v" + self.value[self.cursor:]
			elif key == pygame.K_w and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "w" + self.value[self.cursor:]
			elif key == pygame.K_x and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "x" + self.value[self.cursor:]
			elif key == pygame.K_y and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "y" + self.value[self.cursor:]
			elif key == pygame.K_z and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "z" + self.value[self.cursor:]
			elif key == pygame.K_1 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "1" + self.value[self.cursor:]
			elif key == pygame.K_2 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "2" + self.value[self.cursor:]
			elif key == pygame.K_3 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "3" + self.value[self.cursor:]
			elif key == pygame.K_4 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "4" + self.value[self.cursor:]
			elif key == pygame.K_5 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "5" + self.value[self.cursor:]
			elif key == pygame.K_6 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "6" + self.value[self.cursor:]
			elif key == pygame.K_7 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "7" + self.value[self.cursor:]
			elif key == pygame.K_8 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "8" + self.value[self.cursor:]
			elif key == pygame.K_9 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "9" + self.value[self.cursor:]
			elif key == pygame.K_0 and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "0" + self.value[self.cursor:]
			elif key == pygame.K_SPACE and len(self.value) < self.maxlength:
				self.value = self.value[:self.cursor] + "_" + self.value[self.cursor:]
			elif key == pygame.K_BACKSPACE and len(self.value) > 0:
				self.offset = max(self.offset - 1, 0)
				self.cursor = max(self.cursor - 1, 0)
				self.value = self.value[:self.cursor] + self.value[self.cursor + 1:]
				return
			else:
				return
			if len(self.value) > self.maxchars:
				self.offset += 1
			self.cursor += 1

	def get_value(self):
		return self.value


"""
PComponent that acts like a standard vertical scrollbar, executing 0 or more functions on updates
"""
class PVerticalScrollBar(PComponent):
	def __init__(self, gc, maximum, thumb_height = 30, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 15, 0, debug_name)
		self.gc = gc
		self.value = 0
		self.maximum = maximum
		self.thumb_height = thumb_height
		self.actions = []

	def paint(self, surface, window):
		pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))
		if window.get_focus() == self:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x(), max(min(mouse_y - (self.thumb_height / 2), self.get_height() + self.get_y() - self.thumb_height), self.get_y()), self.get_width(), self.thumb_height))
		else:
			pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x(), self.get_y() + max(min(self.value * (self.get_height() - self.thumb_height) / self.maximum, self.get_height() - self.thumb_height), 0), self.get_width(), self.thumb_height))

	def mouse_down(self, x, y, window):
		window.set_focus(self)

	def mouse_up(self, x, y, window):
		if window.get_focus() == self:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			self.value = max(min((mouse_y - self.get_y() - (self.thumb_height / 2)) * self.maximum / (self.get_height() - self.thumb_height), self.maximum),0)
			for action in self.actions:
				action(self)
			window.reset_focus()

	def adjust_children(self):
		self.set_height(self.parent.get_height())

	def add_action(self, action):
		self.actions.append(action)

	def get_maximum(self):
		return self.maximum

	def set_maximum(self, maximum):
		self.maximum = maximum

	def get_value(self):
		return self.value

	def set_thumb(self, value):
		self.thumb_height = max(min(value, self.get_height()), 1)


"""
PComponent that acts like a standard horizontal scrollbar, executing 0 or more functions on updates
"""
class PHorizontalScrollBar(PComponent):
	def __init__(self, gc, maximum, thumb_width = 30, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 15, debug_name)
		self.gc = gc
		self.value = 0
		self.maximum = maximum
		self.thumb_width = thumb_width
		self.actions = []

	def paint(self, surface, window):
		pygame.draw.rect(surface, self.gc.border_colour, pygame.Rect(self.get_x(), self.get_y(), self.get_width(), self.get_height()))
		if window.get_focus() == self:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(max(min(mouse_x - (self.thumb_width / 2), self.get_width() + self.get_x() - self.thumb_width), self.get_x()), self.get_y(), self.thumb_width, self.get_height()))
		else:
			pygame.draw.rect(surface, self.gc.background_colour, pygame.Rect(self.get_x() + max(min(self.value * (self.get_width() - self.thumb_width) / self.maximum, self.get_width() - self.thumb_width), 0), self.get_y(), self.thumb_width, self.get_height()))

	def mouse_down(self, x, y, window):
		window.set_focus(self)

	def mouse_up(self, x, y, window):
		if window.get_focus() == self:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			self.value = max(min((mouse_x - self.get_x() - (self.thumb_width / 2)) * self.maximum / (self.get_width() - self.thumb_width), self.maximum),0)
			for action in self.actions:
				action(self)
			window.reset_focus()

	def adjust_children(self):
		self.set_width(self.parent.get_width())

	def add_action(self, action):
		self.actions.append(action)

	def get_maximum(self):
		return self.maximum

	def set_maximum(self, maximum):
		self.maximum = maximum

	def get_value(self):
		return self.value

	def set_thumb(self, value):
		self.thumb_width = max(min(value, self.get_width()), 1)


"""
PComponent that acts as a PPanel that contains scrollbars on the bottom and right sides if the panel's size exceeds the given maximum width and/or height
Does not exceed max_width or max_height
"""
class PScrollPanel(PComponent):
	def __init__(self, gc, max_width, max_height, orientation, debug_name = "Anonymous"):
		PComponent.__init__(self, 0, 0, 0, 0, debug_name)
		self.gc = gc
		self.main_panel = PPanel(orientation, debug_name + "_main_panel")
		self.max_width = max_width
		self.max_height = max_height
		self.surface = pygame.Surface((0, 0))
		self.surface.fill((255, 0, 255))
		self.surface.set_colorkey((255, 0, 255))
		self.y_offset = 0
		self.x_offset = 0
		self.scroll_vertical = False
		self.scroll_horizontal = False
		self.vertical_scroll = PVerticalScrollBar(self.gc, self.max_height, 30, debug_name + "_vertical_scroll")
		self.vertical_scroll.set_x(-50)
		self.vertical_scroll.set_y(-50)
		self.vertical_scroll.set_width(0)
		self.vertical_scroll.set_height(0)
		self.horizontal_scroll = PHorizontalScrollBar(self.gc, self.max_width, 30, debug_name + "_horizontal_scroll")
		self.horizontal_scroll.set_x(-50)
		self.horizontal_scroll.set_y(-50)
		self.horizontal_scroll.set_width(0)
		self.horizontal_scroll.set_height(0)

	def paint(self, surface, window):
		self.main_panel.paint(self.surface, window)
		width = self.get_width()
		height = self.get_height()
		if self.scroll_vertical:
			width -= self.vertical_scroll.get_width()
		if self.scroll_horizontal:
			height -= self.horizontal_scroll.get_height()
		surface.blit(self.surface, (self.get_x(), self.get_y()), pygame.Rect(self.x_offset, self.y_offset, width, height))
		self.vertical_scroll.paint(surface, window)
		self.horizontal_scroll.paint(surface, window)

	def mouse_down(self, x, y, window):
		if self.vertical_scroll.contains_point(x, y):
			self.vertical_scroll.mouse_down(x, y, window)
		elif self.horizontal_scroll.contains_point(x, y):
			self.horizontal_scroll.mouse_down(x, y, window)
		elif self.main_panel.contains_point(x, y):
			self.main_panel.mouse_down(x + self.x_offset - self.get_x(), y + self.y_offset - self.get_y(), window)

	def mouse_up(self, x, y, window):
		if self.vertical_scroll.contains_point(x, y):
			self.vertical_scroll.mouse_up(x, y, window)
		elif self.horizontal_scroll.contains_point(x, y):
			self.horizontal_scroll.mouse_up(x, y, window)
		elif self.main_panel.contains_point(x, y):
			self.main_panel.mouse_up(x + self.x_offset - self.get_x(), y + self.y_offset - self.get_y(), window)

	def adjust_children(self):
		if self.scroll_vertical:
			self.vertical_scroll.set_y(self.get_y())
			self.vertical_scroll.set_x(self.get_width() + self.get_x() - self.vertical_scroll.get_width())
		if self.scroll_horizontal:
			self.horizontal_scroll.set_y(self.get_height() + self.get_y() - self.horizontal_scroll.get_height())
			self.horizontal_scroll.set_x(self.get_x())
		self.main_panel.set_x(self.get_x())
		self.main_panel.set_y(self.get_y())

	def action_scroll_v(self, bar):
		self.y_offset = bar.get_value()

	def action_scroll_h(self, bar):
		self.x_offset = bar.get_value()

	def add_component(self, component):
		self.main_panel.add_component(component)
		self.surface = pygame.Surface((self.main_panel.get_width(), self.main_panel.get_height()))
		self.surface.fill((255, 0, 255))
		self.surface.set_colorkey((255, 0, 255))
		self.set_width(min(self.main_panel.get_width(), self.max_width))
		self.set_height(min(self.main_panel.get_height(), self.max_height))

		if not self.scroll_vertical:
			if self.main_panel.get_height() > self.max_height:
				self.scroll_vertical = True
				self.vertical_scroll.add_action(self.action_scroll_v)

		if self.scroll_vertical:
			self.vertical_scroll.set_x(self.get_x() + self.get_width() - self.vertical_scroll.get_width())
			self.vertical_scroll.set_y(self.get_y())
			self.vertical_scroll.set_height(self.max_height - self.horizontal_scroll.get_height())
			self.vertical_scroll.set_width(15)
			self.vertical_scroll.set_maximum(self.main_panel.get_height() - self.max_height + self.horizontal_scroll.get_height())
			self.set_width(min(self.main_panel.get_width() + self.horizontal_scroll.get_width(), self.max_width))

		if not self.scroll_horizontal:
			if self.main_panel.get_width() > self.max_width:
				self.scroll_horizontal = True
				self.horizontal_scroll.add_action(self.action_scroll_h)

		if self.scroll_horizontal:
			self.horizontal_scroll.set_x(self.get_x())
			self.horizontal_scroll.set_y(self.get_y() + self.get_height() - self.horizontal_scroll.get_height())
			self.horizontal_scroll.set_height(15)
			self.horizontal_scroll.set_width(self.max_width - self.vertical_scroll.get_width())
			self.horizontal_scroll.set_maximum(self.main_panel.get_width() - self.max_width + self.vertical_scroll.get_width())
			self.set_height(min(self.main_panel.get_height() + self.horizontal_scroll.get_height(), self.max_height))




"""
Contains a dictionary mapping characters to the images defined in fontfile
Character images must be square with dimensions (fontsize, fontsize)
Supported characters, in the order they must appear in the fontfile are:
abcdefghijklmnopqrstuvwxyz1234567890+-/[]:.,# _'?!
Both the space character and the underscore character are mapped to the same image
"""
class PFont:
	def __init__(self, fontfile, fontsize):
		fontsheet = ptilesheet.PTileSheet(fontfile, fontsize)
		self.fontsize = fontsize
		self.fontspacing = min(max(1, fontsize / 10), 10)
		self.dict = {}
		self.dict['a'] = fontsheet.get_tile(0, 0)
		self.dict['b'] = fontsheet.get_tile(1, 0)
		self.dict['c'] = fontsheet.get_tile(2, 0)
		self.dict['d'] = fontsheet.get_tile(3, 0)
		self.dict['e'] = fontsheet.get_tile(4, 0)
		self.dict['f'] = fontsheet.get_tile(5, 0)
		self.dict['g'] = fontsheet.get_tile(6, 0)
		self.dict['h'] = fontsheet.get_tile(7, 0)
		self.dict['i'] = fontsheet.get_tile(8, 0)
		self.dict['j'] = fontsheet.get_tile(9, 0)
		self.dict['k'] = fontsheet.get_tile(10, 0)
		self.dict['l'] = fontsheet.get_tile(11, 0)
		self.dict['m'] = fontsheet.get_tile(12, 0)
		self.dict['n'] = fontsheet.get_tile(13, 0)
		self.dict['o'] = fontsheet.get_tile(14, 0)
		self.dict['p'] = fontsheet.get_tile(15, 0)
		self.dict['q'] = fontsheet.get_tile(16, 0)
		self.dict['r'] = fontsheet.get_tile(17, 0)
		self.dict['s'] = fontsheet.get_tile(18, 0)
		self.dict['t'] = fontsheet.get_tile(19, 0)
		self.dict['u'] = fontsheet.get_tile(20, 0)
		self.dict['v'] = fontsheet.get_tile(21, 0)
		self.dict['w'] = fontsheet.get_tile(22, 0)
		self.dict['x'] = fontsheet.get_tile(23, 0)
		self.dict['y'] = fontsheet.get_tile(24, 0)
		self.dict['z'] = fontsheet.get_tile(25, 0)
		self.dict['1'] = fontsheet.get_tile(26, 0)
		self.dict['2'] = fontsheet.get_tile(27, 0)
		self.dict['3'] = fontsheet.get_tile(28, 0)
		self.dict['4'] = fontsheet.get_tile(29, 0)
		self.dict['5'] = fontsheet.get_tile(30, 0)
		self.dict['6'] = fontsheet.get_tile(31, 0)
		self.dict['7'] = fontsheet.get_tile(32, 0)
		self.dict['8'] = fontsheet.get_tile(33, 0)
		self.dict['9'] = fontsheet.get_tile(34, 0)
		self.dict['0'] = fontsheet.get_tile(35, 0)
		self.dict['+'] = fontsheet.get_tile(36, 0)
		self.dict['-'] = fontsheet.get_tile(37, 0)
		self.dict['/'] = fontsheet.get_tile(38, 0)
		self.dict['['] = fontsheet.get_tile(39, 0)
		self.dict[']'] = fontsheet.get_tile(40, 0)
		self.dict[':'] = fontsheet.get_tile(41, 0)
		self.dict['.'] = fontsheet.get_tile(42, 0)
		self.dict[','] = fontsheet.get_tile(43, 0)
		self.dict['#'] = fontsheet.get_tile(44, 0)
		self.dict[' '] = fontsheet.get_tile(45, 0)
		self.dict['_'] = fontsheet.get_tile(45, 0) # Underscores are painted as whitespace
		self.dict["'"] = fontsheet.get_tile(46, 0)
		self.dict['?'] = fontsheet.get_tile(47, 0)
		self.dict['!'] = fontsheet.get_tile(48, 0)

	def get_char(self, char):
		return self.dict.get(char.lower(), self.dict['?'])

	def get_fontsize(self):
		return self.fontsize

	def get_fontspacing(self):
		return self.fontspacing




"""
Stores the font and basic colours used in drawing PComponents. Allows for setting and getting of all attributes
"""
class PGraphicsContext:
	def __init__(self, font, border_colour = (0, 0, 0), background_colour = (150, 150, 150), cursor_colour = (200, 200, 200), foreground_colour = (255, 255, 255)):
		self.font = font
		self.border_colour = border_colour
		self.background_colour = background_colour
		self.cursor_colour = cursor_colour
		self.foreground_colour = foreground_colour

	def set_font(self, font):
		self.font = font

	def set_border_colour(self, colour):
		self.border_colour = colour

	def set_background_colour(self, colour):
		self.background_colour = colour

	def set_cursor_colour(self, colour):
		self.cursor_colour = colour

	def set_foreground_colour(self, colour):
		self.foreground_colour = colour

	def get_font(self):
		return self.font

	def get_border_colour(self):
		return self.border_colour

	def get_background_colour(self):
		return self.background_colour

	def get_cursor_colour(self):
		return self.cursor_colour

	def get_foreground_colour(self):
		return self.foreground_colour




"""
Allows for saving a restoring the state of a PWindow. Should only be used within PWindow methods and not by users
"""
class PWindowState:
	def __init__(self, main_panel, actions):
		self.main_panel = main_panel
		self.actions = actions

	def get_main_panel(self):
		return self.main_panel

	def get_actions(self):
		return self. actions



"""
PWindow wrapper for pygame window containing a PPanel which can have other PComponents added to it. Executes 0 or more functions on each iteration of the event loop
Start the application with start()
"""
class PWindow:
	def __init__(self, width, height, orientation = VERTICAL_ORIENTATION):
		self.width = width
		self.height = height
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((width, height))
		self.focus = None
		self.main_panel = PPanel(orientation, "Main Panel")
		self.actions = []

	def get_state(self):
		return PWindowState(self.main_panel, self.actions)

	def reset_state(self):
		self.main_panel = PPanel(orientation, "Main Panel")
		self.actions = []

	def set_state(self, pwindowstate):
		self.main_panel = pwindowstate.get_main_panel()
		self.actions = pwindowstate.get_actions()

	def add_component(self, comp):
		self.main_panel.add_component(comp)

	def add_action(self, action):
		self.actions.append(action)

	def set_focus(self, comp):
		self.focus = comp

	def reset_focus(self):
		self.focus = None

	def get_focus(self):
		return self.focus

	def start(self, fps):
		while (True):
			self.clock.tick(fps)
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT:
					pygame.quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos
					self.main_panel.mouse_down(x, y, self)
				if event.type == pygame.MOUSEBUTTONUP:
					x, y = event.pos
					self.main_panel.mouse_up(x, y, self)
					if self.focus != None:
						self.focus.mouse_up(x, y, self)
				if event.type == pygame.KEYDOWN:
					if self.focus != None:
						self.focus.key_down(event.key, self)
				if event.type == pygame.KEYUP:
					if self.focus != None:
						self.focus.key_up(event.key, self)
			for action in self.actions:
				action(self)
			self.screen.fill((255, 255, 255))
			self.main_panel.paint(self.screen, self)
			pygame.display.update()