import pathlib
import fluigi

# Global Variables

DEVICE_X_DIM = 76200
DEVICE_Y_DIM = 76200
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
