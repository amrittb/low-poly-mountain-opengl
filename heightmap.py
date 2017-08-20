import numpy as np

from PIL import Image

MAX_COLOR_VALUE = 255

def get_normalized_height_data(image_path):
	map_image = Image.open(image_path)
	map_data = map_image.load()

	height_data = []

	for y in range(0,map_image.size[1]):
		line_data = []
		for x in range(0,map_image.size[0]):
			line_data.append(map_data[x,y]/MAX_COLOR_VALUE)

		height_data.append(line_data)

	return np.array(height_data)