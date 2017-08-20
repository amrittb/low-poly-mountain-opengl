import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from MountainFactory import *
from PIL import Image

skybox = { 
			"tex_rt": {"data": "", "textureID": 0}, 
			"tex_lf": {"data": "", "textureID": 0}, 
			"tex_up": {"data": "", "textureID": 0},
			"tex_bt": {"data": "", "textureID": 0}, 
			"tex_bk": {"data": "", "textureID": 0}, 
			"tex_ft": {"data": "", "textureID": 0} 
		}

def load_skybox():
	im_lf = Image.open("skybox/alps_lf.tga").rotate(180).resize((512,512))
	im_rt = Image.open("skybox/alps_rt.tga").rotate(180).resize((512,512))
	im_up = Image.open("skybox/alps_up.tga").resize((512,512))
	im_bt = Image.open("skybox/alps_dn.tga").rotate(180).transpose(Image.FLIP_LEFT_RIGHT).resize((512,512))
	im_bk = Image.open("skybox/alps_bk.tga").rotate(180).transpose(Image.FLIP_LEFT_RIGHT).resize((512,512))
	im_ft = Image.open("skybox/alps_ft.tga").rotate(180).resize((512,512))

	skybox["tex_lf"]["data"] = im_lf.tobytes()
	skybox["tex_rt"]["data"] = im_rt.tobytes()
	skybox["tex_up"]["data"] = im_up.tobytes()
	skybox["tex_bt"]["data"] = im_bt.tobytes()
	skybox["tex_bk"]["data"] = im_bk.tobytes()
	skybox["tex_ft"]["data"] = im_ft.tobytes()

	for i, texture in enumerate(skybox):
		textureID = glGenTextures(1)
		skybox[texture]['textureID'] = textureID

		glBindTexture(GL_TEXTURE_2D, textureID)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, skybox[texture]["data"])

def draw_skybox():
	plane_distance = 150
	glEnable(GL_TEXTURE_2D)
	glDisable(GL_DEPTH_TEST)
	glDisable(GL_LIGHTING)
	glDisable(GL_LIGHT0)

	# Top Plane
	glColor3f(1,1,1)
	glBindTexture(GL_TEXTURE_2D, skybox["tex_up"]["textureID"])
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex3f(-plane_distance, plane_distance, -plane_distance)
	glTexCoord2f(1, 0)
	glVertex3f(plane_distance, plane_distance, -plane_distance)
	glTexCoord2f(1, 1)
	glVertex3f(plane_distance, plane_distance, plane_distance)
	glTexCoord2f(0, 1)
	glVertex3f(-plane_distance, plane_distance, plane_distance)
	glEnd()

	# Left Plane
	glColor3f(1,1,1)
	glBindTexture(GL_TEXTURE_2D, skybox["tex_lf"]["textureID"])
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex3f(-plane_distance, -plane_distance, -plane_distance)
	glTexCoord2f(1, 0)
	glVertex3f(-plane_distance, -plane_distance, plane_distance)
	glTexCoord2f(1, 1)
	glVertex3f(-plane_distance, plane_distance, plane_distance)
	glTexCoord2f(0, 1)
	glVertex3f(-plane_distance, plane_distance, -plane_distance)
	glEnd()

	# Front plane
	glColor3f(1,1,1)
	glBindTexture(GL_TEXTURE_2D, skybox["tex_ft"]["textureID"])
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex3f(-plane_distance, -plane_distance, plane_distance)
	glTexCoord2f(1, 0)
	glVertex3f(plane_distance, -plane_distance, plane_distance)
	glTexCoord2f(1, 1)
	glVertex3f(plane_distance, plane_distance, plane_distance)
	glTexCoord2f(0, 1)
	glVertex3f(-plane_distance, plane_distance, plane_distance)
	glEnd()

	# Right Plane
	glColor3f(1,1,1)
	glBindTexture(GL_TEXTURE_2D, skybox["tex_rt"]["textureID"])
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex3f(plane_distance, -plane_distance, plane_distance)
	glTexCoord2f(1, 0)
	glVertex3f(plane_distance, -plane_distance, -plane_distance)
	glTexCoord2f(1, 1)
	glVertex3f(plane_distance, plane_distance, -plane_distance)
	glTexCoord2f(0, 1)
	glVertex3f(plane_distance, plane_distance, plane_distance)
	glEnd()

	# Back Plane
	glColor3f(1,1,1)
	glBindTexture(GL_TEXTURE_2D, skybox["tex_bk"]["textureID"])
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex3f(-plane_distance, -plane_distance, -plane_distance)
	glTexCoord2f(1, 0)
	glVertex3f(plane_distance, -plane_distance, -plane_distance)
	glTexCoord2f(1, 1)
	glVertex3f(plane_distance, plane_distance, -plane_distance)
	glTexCoord2f(0, 1)
	glVertex3f(-plane_distance, plane_distance, -plane_distance)
	glEnd()

	# Bottom Plane
	glColor3f(1,1,1)
	glBindTexture(GL_TEXTURE_2D, skybox["tex_bt"]["textureID"])
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex3f(-plane_distance, -plane_distance, -plane_distance)
	glTexCoord2f(1, 0)
	glVertex3f(plane_distance, -plane_distance, -plane_distance)
	glTexCoord2f(1, 1)
	glVertex3f(plane_distance, -plane_distance, plane_distance)
	glTexCoord2f(0, 1)
	glVertex3f(-plane_distance, -plane_distance, plane_distance)
	glEnd()

	glBindTexture(GL_TEXTURE_2D, 0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)

"""
Initializes OpenGL
"""
def init_gl(width, height):
	# Flat Shading Mode
	glShadeModel(GL_FLAT)
	# Enables Depth Testing
	glEnable(GL_DEPTH_TEST)

	# Calculates perspective
	# Convert to Projection matrix
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	# Perspective Frustum FOV, Aspect Ratio, Near Clipping, Far Clipping
	gluPerspective(45, (width/height), 0.1, 1024.0)

	# Camera setup in Model View Matrix
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(
		-10,-30,-10,
		0,-35,0,
		0,1,0
		)

	# Lighting Setup
	glLightfv(GL_LIGHT0, GL_DIFFUSE, GLfloat_4(0.8, 0.8, 0.8, 1.0))
	glLightfv(GL_LIGHT0, GL_POSITION, GLfloat_4(100, 100, 100, 1.0))

	glLightfv(GL_LIGHT1, GL_DIFFUSE, GLfloat_4(0.9,0.9,0.9,1.0))
	glLightfv(GL_LIGHT1, GL_POSITION, GLfloat_4(0, 100, 0, 1.0))

	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, GLfloat_4(0.8, 0.8, 0.8, 1.0))

	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHT1)
	glEnable(GL_LIGHTING)

	glColorMaterial (GL_FRONT_AND_BACK, GL_DIFFUSE)
	glEnable (GL_COLOR_MATERIAL)

	load_skybox()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	
	# Initializing OpenGL
	init_gl(display[0],display[1])

	# Initializing Factory object
	factory = MountainFactory()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		pressed_keys = pygame.key.get_pressed()

		if pressed_keys[pygame.K_LEFT]:
			# Rotate the world with center at (35,0,35)
			# which is the center of the mountain
			# Retransform it back to origin
			glTranslate(35, 0, 35)
			glRotatef(-2, 0, 1, 0)
			glTranslate(-35, 0, -35)
		if pressed_keys[pygame.K_RIGHT]:
			# Similar to rotating to left
			glTranslate(35, 0, 35)
			glRotatef(2, 0, 1, 0)
			glTranslate(-35, 0, -35)

		# Clearing previous buffer
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		# Rendering Skybox
		draw_skybox()

		# Rendering the mountain in y=-80 as base location
		glTranslate(0,-80, 0)
		factory.render()
		glTranslate(0, 80, 0)

		# Flipping Display for new frame buffer rendering
		pygame.display.flip()

if __name__ == "__main__":
	main()