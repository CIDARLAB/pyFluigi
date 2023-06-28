import jpype
from jpype.types import *

from fluigi.parameters import FLUIGI_JAVA_PNR_JAR_PATH

jar_path = FLUIGI_JAVA_PNR_JAR_PATH.resolve()
jpype.startJVM(classpath=[jar_path])

import java
from org.cidarlab.fluigi.fluigi import *

test = {}
test["flowChannelWidth"] = int(100)
test["controlChannelWidth"] = int(50)
test["chamberLength"] = int(100)
test["chamberWidth"] = int(100)
test["portRadius"] = int(100)
mint = "LOGIC ARRAY"
print(Fluigi.getDimensions(mint, java.util.HashMap(test)))
