import jpype
import jpype.imports
from jpype.types import *

from fluigi.parameters import FLUIGI_JAVA_PNR_JAR_PATH

# jpype.startJVM(classpath=['./pnr/fluigi-java/Fluigi-jar-with-dependencies.jar'])
jar_path = FLUIGI_JAVA_PNR_JAR_PATH.resolve()
jpype.startJVM(classpath=[jar_path])

import java
from org.cidarlab.fluigi.fluigi import *

test = dict()
test['flowChannelWidth'] = int(100)
test['controlChannelWidth'] = int(50)
test['chamberLength'] = int(100)
test['chamberWidth'] = int(100)
test['portRadius'] = int(100)
# map = JObject(test , JClass('java.util.Map'))
# print(Fluigi.testME2(map))
mint = "LOGIC ARRAY"
print(Fluigi.getDimensions(mint, java.util.HashMap(test)))