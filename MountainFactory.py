import random
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from heightmap import get_normalized_height_data

HEIGHT_MULTIPLIER = 40

class MountainFactory:

	def __init__(self):
		self.mountain_size = (10, 10)
		self.tile_size = 7
		self.vertices_size = (self.mountain_size[0] + 1, self.mountain_size[1] + 1)

		self.num_tiles = self.mountain_size[0] * self.mountain_size[1]
		self.num_vertices = self.vertices_size[0] * self.vertices_size[1]
		self.num_tris = 2 * self.num_tiles
		
		self.vertices = np.zeros((self.num_vertices, 3))
		self.vertex_colors = np.zeros((self.num_vertices, 3))
		self.triangles = np.zeros(3 * self.num_tris, dtype=np.uint32)

		self.normals = np.array([[0,1,0] for i in range(self.num_tris * 3)])

		self.is_mesh_populated = False
		self.normals_calculated = False

		self.colors = {
			"snow": (0.99, 1.0, 0.98),
			"rocks": (0.35, 0.13, 0.27),
			"ground": (0.396, 0.765, 0.42)
		}

	def render(self, image_path = "heightmaps/everest_heightmap.jpg"):
		glColor3fv((.9,.9,1))
		if not self.is_mesh_populated:
			self.populate_vertices_and_triangles(image_path)

		glBegin(GL_TRIANGLES)
		i = 1
		j = 0
		for point in self.triangles:
			glColor3fv(self.vertex_colors[point])
			glVertex3fv(self.vertices[point])
			i +=  1

			if i == 3:
				# Calculate face normals
				if not self.normals_calculated:
					vector_one = np.subtract(self.vertices[point - 2], self.vertices[point - 3])
					vector_two = np.subtract(self.vertices[point - 1], self.vertices[point - 3])

					cross_product = np.cross(vector_one, vector_two)
					distance = np.sqrt(np.sum(np.square(cross_product)))

					if distance != 0:
						normal_vector = np.divide(cross_product, distance)
						self.normals[j] = normal_vector
					else:
						self.normals[j] = (0,1,0)

				glNormal3fv(self.normals[j])

				j += 1
				i = 1
		glEnd()

		if not self.normals_calculated:
			self.normals_calculated = True

	def populate_vertices_and_triangles(self, image_path):
		if not hasattr(self, 'height_data'):
			print("No height data")
			self.height_data = get_normalized_height_data(image_path)

		for z in range(0, self.vertices_size[0]):
			for x in range(0, self.vertices_size[1]):
				map_z = int(float(z) / self.vertices_size[0] * self.height_data.shape[0])
				map_x = int(float(x) / self.vertices_size[1] * self.height_data.shape[1])

				height = self.height_data[map_z][map_x]
				self.vertices[z * self.vertices_size[1] + x] = [self.tile_size * self.vertices_size[1] - x * self.tile_size, 
																height * HEIGHT_MULTIPLIER, 
																self.tile_size * self.vertices_size[0] - z * self.tile_size]

				color = self.colors['snow']

				self.vertex_colors[z * self.vertices_size[1] + x] = color

		for z in range(0, self.mountain_size[0]):
			for x in range(0, self.mountain_size[1]):
				square_index = z * self.mountain_size[1] + x
				triangle_offset = square_index * 6

				self.triangles[triangle_offset + 0] = z * self.vertices_size[1] + x + 						  0
				self.triangles[triangle_offset + 1] = z * self.vertices_size[1] + x + self.vertices_size[1]	+ 0
				self.triangles[triangle_offset + 2] = z * self.vertices_size[1] + x + self.vertices_size[1]	+ 1

				self.triangles[triangle_offset + 3] = z * self.vertices_size[1] + x + 				  		  0
				self.triangles[triangle_offset + 4] = z * self.vertices_size[1] + x + self.vertices_size[1]	+ 1
				self.triangles[triangle_offset + 5] = z * self.vertices_size[1] + x + 				  		  1

		self.is_mesh_populated = True