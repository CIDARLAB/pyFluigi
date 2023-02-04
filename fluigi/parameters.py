import os
import pathlib

import fluigi

# Draw constants
PT_TO_UM = 1 / 352.778
PT_TO_MM = 2.83464388369

# Global Variables
DEVICE_X_DIM = 76200
DEVICE_Y_DIM = 76200

DEVICE_PADDING = 20000

# Design Rule Variables
COMPONENT_SPACING = 9000
CONNECTION_SPACING = 1000


LAMBDA = 10


# SA Parameters
WIRE_PENALTY = 2
AREA_PENALTY = 0
OVERLAP_PENALTY = 500000

DEFAULT_MOVES_PER_TEMP = 50
DEFAULT_MOVES_PER_TEMP_PER_MODULE = 100
DEFAULT_COOL_RATE = 0.95

SIGMA_MULTIPLIER = 20

# SA GRID Parameters
SA_GRID_BLOCK_SIZE = 100

# Code Parameter

# Global Variables
FLUIGI_DIR = pathlib.Path(fluigi.__file__).parent.parent.absolute()
FLUIGI_JAVA_PNR_JAR_PATH = FLUIGI_DIR.joinpath("bin/Fluigi-jar-with-dependencies.jar")
OUTPUT_DIR = FLUIGI_DIR.joinpath("out")
# PRIMITIVE_SERVER_URI = "http://neptune.fluigicad.org:5555"
# PRIMITIVE_SERVER_URI = "https://primitives-server.herokuapp.com"
PRIMITIVE_SERVER_URI = os.getenv("PRIMITIVE_SERVER_URI", "http://localhost:6060")


# Semi-FullCustom Parameters
SPACER_THRESHOLD = 5000
