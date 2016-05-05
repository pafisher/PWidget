=======
PWidget
=======

IMPORTANT: In order to use this package, you need to have pygame installed!

PWidget provides a set of GUI widgets built on top of Pygame.
PComponents are top-down and are loosely modeled on the action-listener concepts and layout design of Java's Swing library as well as X-Windows.

This README covers the primary uses and functions of each class in this package and ignores functions that should only be used internally and shouldn't be called anywhere else

Almost everything in this package is derived from the PComponent base class. Additional widgets can easily be developed by inheriting from PComponent and overriding its purely virtual functions. You can read more in the PComponent section of this README.

Example use:

	from pwidget import pgui

	def main():
		width = 500
		height = 500
		fontfile = 'fonts/Black Font.png'
		fontdimensions = 10

		window = pgui.PWindow(width, height)
		
		font = pgui.PFont(fontfile, fontdimensions)
		gc = pgui.PGraphicsContext(font)

		label = pgui.PLabel(gc, "hello world!")
		window.add_component(label)

		FPS = 30
		window.start(FPS)

	if __name__ == "__main__":
		main()


Constants
=========

VERTICAL_ORIENTATION
--------------------

Constant defining a vertical orientation for PWindows and PPanels. Any PComponents added to a PWindow or PPanel with VERTICAL_ORIENTATION will be added beneath all of the other PComponents in the PWindow or PPanel.


HORIZONTAL_ORIENTATION
----------------------

Constant defining a horizontal orientation for PWindows and PPanels. Any PComponents added to a PWindow or PPanel with HORIZONTAL_ORIENTATION will be added to the right of all of the other PComponents in the PWindow or PPanel.


PWindow
=======

The PWindow instantiates the Pygame window and acts as the main container for the PComponents. If no orientation is specified at initialization, it defaults to vertical.

PWindow(width, height[, orientation])
# width is the width of the PWindow in pixels
# height is the height of the PWindow in pixels
# orientation is the orientation of the PWindow, either VERTICAL_ORIENTATION or HORIZONTAL_ORIENTATION

add_component(component)
# component is a PComponent
## PComponents need to be added to the PWindow to be painted

add_action(action)
# action is a function that takes the PWindow as an arugment
## actions are executed on each iteration of the PWindow's event loop

get_focus()
# no arguments
## returns the current focus attribute of the PWindow

set_focus(component)
# component is a PComponent
## sets the focus attribute of the PWindow to component. Traditionally the focus attribute is the last PComponent to receive a mouse_down() event. Use this when developing new PComponents

reset_focus()
# no arguments
## resets the focus attribute of the PWindow to None

start(fps)
# fps is the number of times the event loop iterates each second
## starts the event-loop, executing all actions on each iteration of the event-loop. Once this function is called, the program will execute this function until the program terminates

get_state()
# no arguments
## returns the current state of the PWindow's panels and actions

set_state(state)
# state is a PWindowState that has been returned by PWindow.get_state()
## sets the current state of the PWindow's panels and actions to those of the provided state

reset_state()
# no arguments
## resets the state of the PWindow's panels and actions allowing you to build up a new GUI from scratch


PFont
=====

A PFont is a custom font for PComponents to use when drawing text. Characters need to be specified in a fontfile .png or .bmp with equal widths and heights. Characters, in the order that they must appear in the fontfile are: abcdefghijklmnopqrstuvwxyz1234567890+-/[]:.,# _'?!

PFont(fontfile, fontsize)
# fontfile is a .png or .bmp including its directory location
# fontsize is the width/height of each character defined in fontfile


PGraphicsContext
================

A PGraphicsContext is a container for the combination of font and colours that a PComponent can use to draw itself. All painted PComponents require a PGraphicsContext object

PGraphicsContext(font[, border_colour[, background_colour[, cursor_colour[, foreground_colour]]]])
# font is a PFont that can be used to display text
# border_colour is a 3-tuple of integers between 0 and 255 inclusive, representing the red, green, and blue values of the colour used to draw borders and lines
# background_colour is a 3-tuple of integers between 0 and 255 inclusive, representing the red, green, and blue values of the colour used to draw PComponent backgrounds
# cursor_colour is a 3-tuple of integers between 0 and 255 inclusive, representing the red, green, and blue values of the colour used to draw cursors and selections
# foreground_colour is a 3-tuple of integers between 0 and 255 inclusive, representing the red, green, and blue values of the colour used to draw PComponent foregrounds
## the default values for:
## border_colour = (0, 0, 0)
## background_colour = (150, 150, 150)
## cursor_colour = (200, 200, 200)
## foreground_colour = (250, 250, 250)


PComponent
==========

This acts as the base class for each of the other widgets. It provides the basic functionality for each widget and new PComponents must inherit from this class to integrate properly with the rest of this package

PComponent(x, y, width, height[, debugname])
# x is the x-offset of the PComponent from the left side of the PWindow in pixels
# y is the y-offset of the PComponent from the top of the PWindow in pixels
# width is the width of the PComponent in pixels
# height is the height of the PComponent in pixels
# debugname is an identifier string that can be used for debugging
## the x and y values of a PComponent are automatically adjusted when it is added to a PPanel or PWindow, so any values passed in will actually be ignored

paint(surface, window)
# surface is a Pygame surface object (usually the screen)
# window is the PWindow where the PComponent is being drawn
## paint() is purely virtual. If you inherit from this class, you must override this method using the same function signature and any Pygame drawing functions you require

mouse_down(x, y, window)
# x is the x co-ordinate of the mouse_down event
# y is the y co-ordinate of the mouse_down event
# window is the PWindow where the PComponent is being drawn
## mouse_down() is purely virtual. If you inherit from this class, you must override this method using the same function signature. Traditionally a mouse_down event will set the focus of the PWindow to the PComponent itself

mouse_up(x, y, window)
# x is the x co-ordinate of the mouse_down event
# y is the y co-ordinate of the mouse_down event
# window is the PWindow where the PComponent is being drawn
## mouse_up() is purely virtual. If you inherit from this class, you must override this method using the same function signature. Traditionally a mouse_down event will reset the focus of the PWindow

key_down(key, window)
# key is a Pygame event.key
# window is the PWindow where the PComponent is being drawn
## key_down() is purely virtual. If you inherit from this class, you must override this method using the same function signature. Only the PComponent that is set as the PWindow's focus attribute receives key_down() event

key_up(key, window)
# key is a Pygame event.key
# window is the PWindow where the PComponent is being drawn
## key_up() is purely virtual. If you inherit from this class, you must override this method using the same function signature. Only the PComponent that is set as the PWindow's focus attribute receives key_up() event

contains_point(x, y)
# x is the x co-ordinate of some point
# y is the y co-ordinate of some point
## returns True if the point defined by (x, y) is contained in PComponent

get_x()
# no arguments
## returns the x co-ordinate of the PComponent

get_y()
# no arguments
## returns the y co-ordinate of the PComponent

get_width()
# no arguments
## returns the width of the PComponent

get_height()
# no arguments
## returns the height of the PComponent


PComponents
===========

PPanel
------

Acts as a container for other PComponents, adjusting their x and y coordinates as new PComponents are added, as well as its own width and height

PPanel(orientation[, deubug_name])
# orientation is the orientation of the PPanel, either VERTICAL_ORIENTATION or HORIZONTAL_ORIENTATION
# debug_name for debugging purposes

add_component(component)
# component is a PComponent
## adds a PComponent to the PPanel


PScrollPanel
------------

Acts as a PPanel, that automatically adds scrollbars to the right and/or bottom if the contents of the panel extend beyond provided maximum width and height

PScrollPanel(gc, max_width, max_height, orientation[, debug_name])
# gc is a PGraphicsContext containing the border and background colours for the scroll bars
# max_width is the maximum width of the panel in pixels (including the scroll bar if it's added)
# max_height is the maximum height of the panel in pixels (including the scroll bar if it's added)
# orientation  is the orientation of the panel, either VERTICAL_ORIENTATION or HORIZONTAL_ORIENTATION
# debug_name for debugging purposes

add_component(component)
# component is a PComponent
## adds a PComponent to the PScrollPanel


PLabel
------

Displays text using the given PFont

PLabel(gc, value[, debug_name])
# gc is a PGraphicsContext containing the PFont used to draw the text value
# value is the text value of the label
# debug_name for debugging purposes

set_value(value)
# value is some value to set the label to
## sets the value of the PLabel

get_value()
# no arguments
## returns the current value of the PLabel as a string


PParagraph
----------

Displays text using the given PFont, wrapping text that extends beyond a provided maximum width. Unlike PLabel, does not support value setting or getting

PParagraph(gc, value, max_width[, debug_name])
# gc is a PGraphicsContext containing the PFont used to draw the text value
# value is the text value of the paragraph
# max_width is the maximum width of the PParagraph in pixels. Characters that extend beyond maxwidth are wrapped onto a new line
# debug_name for debugging purposes


PVerticalStrut
--------------

Separates other PComponents within a panel with vertical orientation

PVerticalStrut(height[, debug_name])
# height is the amount of separation the strut creates in pixels
# debug_name for debugging purposes


PHorizontalStrut
--------------

Separates other PComponents within a panel with horizontal orientation

PVerticalStrut(width[, debug_name])
# width is the amount of separation the strut creates in pixels
# debug_name for debugging purposes


PButton
-------

Creates a rectangular button with the text value displayed using the provided PFont. Executes each function that has been added to the PButton when it receives a click

PButton(gc, value[, debug_name])
# gc is a PGraphicsContext containing the PFont used to draw the text value and the border and background of the button
# value is the value displayed on the button
# debug_name for debugging purposes

add_action(action)
# action is a function that takes the PButton as an arugment
## adds an action to the PButton's list of actions that get executed on mouse click

set_value(value)
# value is some value to set the button label to
## sets the value of the PButton

get_value()
# no arguments
## returns the current value of the PButton as a string


PCheckBox
---------

Creates a box that can be toggled on or off with a click. Has an optional label that can be added which appears on the right of the checkbox. Defaults to False or unchecked

PCheckBox(gc[, label[, debug_name]])
# gc is a PGraphicsContext containing the PFont used for the label (if there is one) and the border and foreground of the checkbox
# label is the text value that can be displayed to the right of the checkbox
# debug_name for debugging purposes

add_action(action)
# action is a function that takes the PCheckBox as an argument
## adds an action to the PCheckBox's list of actions that get executed on mouse click

toggle_value([value])
# value is the value to set the PCheckbox to, either True or False
## toggles the value of the PCheckBox to the provided value, or to the opposite of its current value


PSelector
---------

Creates a pane of selectable lines of text options. The pane does not inherently scroll, and displays text only up to the provided width value, measured in pixels. The top option is selected by default. The currently selected option will remain selected whether the option itself is visible or if it has been scrolled out of the pane

PSelector(gc, width, rows[, debug_name])
# gc is a PGraphicsContext containing the PFont used for the options, and the border, background and cursor colours
# width is the width of the selector pane in pixels
# rows is the number of options to display on the pane at one time
# debug_name for debugging purposes

add_option(option)
# value is the name of an option
## adds the option value to the list of selectable options. Options are added to the PSelector in reverse order, so the option that is added first will appear at the bottom of the list, and the option that is added last will appear at the top

def scroll_up()
# no arguments
## scrolls the PSelector up 1 option (or does nothing if there are no options above to scroll to)

def scroll_down()
# no arguments
## scrolls the PSelector down 1 option (or does nothing if there are no options below to scroll to)

def scroll_to(option_number)
# option_number is an int
## scrolls the PSelector to display the option at the given option_number at the top (or elsewhere in the pane if there are not enough options below it)

def get_value()
# no arguments
## returns the currently selected option of the PSelector as a string


PVerticalScrollWheel
--------------------

Creates a pair of buttons spanning the height of the current panel. Increments its own value when the bottom button is clicked and decrements its value when the top button is clicked. Executes each function that has been added to it regardless of which button is clicked. The minimum value and the default current value are both 0

PVerticalScrollWheel(gc, maximum[, debug_name])
# gc is a PGraphicsContext containing the border, background and foreground colours
# maximum is the maximum value the scroll wheel can contain
# debug_name for debugging purposes

add_action(action)
# action is a function that takes the PVerticalScrollWheel as an argument
## adds an action to the PVerticalScrollWheel's list of actions that get executed on mouse clicks

get_value()
# no arguments
## returns the current value of the scroll wheel as an int

get_maximum()
# no arguments
## returns the maximum value of the scroll wheel that was provided at object creation as an int


PHorizontalScrollWheel
--------------------

Creates a pair of buttons spanning the width of the current panel. Increments its own value when the right button is clicked and decrements its value when the left button is clicked. Executes each function that has been added to it regardless of which button is clicked. The minimum value and the default current value are both 0

PHorizontalScrollWheel(gc, maximum[, debug_name])
# gc is a PGraphicsContext containing the border, background and foreground colours
# maximum is the maximum value the scroll wheel can contain
# debug_name for debugging purposes

add_action(action)
# action is a function that takes the PHorizontalScrollWheel as an argument
## adds the action to the PHorizontalScrollWheel's list of actions that get executed on mouse clicks

get_value()
# no arguments
## returns the current value of the scroll wheel as an int

get_maximum()
# no arguments
## returns the maximum value of the scroll wheel that was provided at object creation as an int


PTextBox
--------

Creates a text box that allows for rudimentary text entry. Text can be inserted into any point in the currently inputted string by selecting that point with the mouse

PTextBox(gc, max_width[, max_length[, debug_name]])
# gc is a PGraphicsContext containing the border, background and cursor colours used to draw the text box
# max_width is the maximum width of the text box, measured in pixels. The actual width will be in the range (max_width - fontdimensions, max_width)
# max_length is the maximum length of the string that can be input. Any additional key presses (excluding backspace) will be ignored when max_length is reached
# debug_name for debugging purposes

get_value()
# no arguments
## returns the value of the currently inputted text string as a str


PVerticalScrollBar
------------------

Creates a basic vertical scroll bar that spans the height of its containing panel which executes all of the functions that have been added to it when it updates. The thumb button defaults to a height of 15 if no value is provided, regardless of the height of the entire bar. Clicking anywhere on the bar will move the thumb button to the cursor's current location

PVerticalScrollBar(gc, maximum[, thumb_height[, debug_name]])
# gc is a PGraphicsContext containing the border and background colours used to draw the scroll bar
# maximum is the maximum value of the scroll bar
# thumb_height is the height of the thumb button used for scrolling
# debug_name for debugging purposes

add_action(action)
# action is a function that takes the PVerticalScrollBar as an argument
## adds the action to the PVerticalScrollBar's list of actions that get executed on mouse clicks

get_maximum()
# no arguments
## returns the maximum value of the scroll bar as an int

set_maximum(maximum)
# maximum is an int
## sets the maximum value of the scroll bar

get_value()
# no arguments
## returns the current value of the scroll bar

set_thumb(value)
# value is an int
## sets the height of the thumb button in the scroll bar to the provided value, measured in pixels


PHorizontalScrollBar
------------------

Creates a basic horizontal scroll bar that spans the width of its containing panel which executes all of the functions that have been added to it when it updates. The thumb button defaults to a width of 15 if no value is provided, regardless of the width of the entire bar. Clicking anywhere on the bar will move the thumb button to the cursor's current location

PHorizontalScrollBar(gc, maximum[, thumb_width[, debug_name]])
# gc is a PGraphicsContext containing the border and background colours used to draw the scroll bar
# maximum is the maximum value of the scroll bar
# thumb_width is the width of the thumb button used for scrolling
# debug_name for debugging purposes

add_action(action)
# action is a function that takes the PVerticalScrollBar as an argument
## adds the action to the PHorizontalScrollBar's list of actions that get executed on mouse clicks

get_maximum()
# no arguments
## returns the maximum value of the scroll bar as an int

set_maximum(maximum)
# maximum is an int
## sets the maximum value of the scroll bar

get_value()
# no arguments
## returns the current value of the scroll bar

set_thumb(value)
# value is an int
## sets the width of the thumb button in the scroll bar to the provided value, measured in pixels