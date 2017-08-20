from cx_Freeze import setup, Executable
import os

base = "Win32GUI"

executables = [Executable("app.py", base=base)]

packages = ["OpenGL","pygame","numpy","PIL"]
options = {
    'build_exe': {
        'packages':packages,
    	'include_files': [ 'heightmaps/', 'skybox/']
    },
}

os.environ['TCL_LIBRARY'] = r'C:\Users\amriterry\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\amriterry\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

setup(
    name = "LowPolyMountains",
    options = options,
    version = "1.0.0",
    description = 'Low Poly Art exploration using OpenGL flat shading',
    executables = executables
)