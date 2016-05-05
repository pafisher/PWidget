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