import pathlib

import fluigi

# Global Variables

DEVICE_X_DIM = 70000
DEVICE_Y_DIM = 70000

# Code Parameter

# Global Variables
FLUIGI_DIR = pathlib.Path(fluigi.__file__).parent.parent.absolute()
FLUIGI_JAVA_PNR_JAR_PATH = FLUIGI_DIR.joinpath("bin/Fluigi-jar-with-dependencies.jar")
OUTPUT_DIR = FLUIGI_DIR.joinpath("out")
